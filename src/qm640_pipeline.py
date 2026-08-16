from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from joblib import dump
from sklearn.calibration import calibration_curve
from sklearn.ensemble import (
    GradientBoostingClassifier,
    GradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import LeaveOneGroupOut, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.tree import DecisionTreeClassifier

SEED = 640
PRIMARY_FEATURES = ["VSH", "PHIT"]
STATE_COLUMNS = ["ZONE", "VSH", "SW", "RT", "PHIT", "NTG", "K"]


def repo_root(start: str | Path | None = None) -> Path:
    path = Path(start or Path.cwd()).resolve()
    for candidate in [path, *path.parents]:
        if (candidate / "data").exists() and (candidate / "README.md").exists():
            return candidate
    raise FileNotFoundError("Repository root not found. Run from inside the repository.")


def load_processed(root: str | Path | None = None) -> pd.DataFrame:
    root = repo_root(root)
    path = root / "data" / "processed" / "All_Wells_with_Well_ID.txt"
    df = pd.read_csv(path, sep="\t")
    required = ["Well_ID", "MD", "TVDSS", "ZONE", "VSH", "SW", "RT", "PHIT", "NTG", "K"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df


def load_raw(root: str | Path | None = None) -> pd.DataFrame:
    root = repo_root(root)
    return pd.read_csv(root / "data" / "raw" / "All_Wells.txt", sep="\t")


def assign_well_ids(raw: pd.DataFrame) -> pd.DataFrame:
    if "MD" not in raw:
        raise ValueError("MD is required to reconstruct anonymous groups.")
    out = raw.copy()
    resets = out["MD"].diff().lt(0).fillna(False)
    group_num = resets.cumsum() + 1
    out.insert(0, "Well_ID", group_num.map(lambda n: f"W{int(n):02d}"))
    return out


def data_inventory(df: pd.DataFrame) -> dict[str, Any]:
    return {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "well_counts": df["Well_ID"].value_counts().sort_index().to_dict(),
        "target_counts": df["NTG"].value_counts().sort_index().to_dict(),
        "missing_values": df.isna().sum().to_dict(),
        "exact_duplicate_rows": int(df.duplicated().sum()),
        "duplicate_well_md": int(df.duplicated(["Well_ID", "MD"]).sum()),
    }


def cleaning_summary(df: pd.DataFrame) -> pd.DataFrame:
    adjacent = df.groupby("Well_ID", group_keys=False)[STATE_COLUMNS].apply(
        lambda g: g.eq(g.shift()).all(axis=1)
    )
    rows = [
        ["Source missingness", int(df.isna().sum().sum()), "No raw imputation"],
        ["Anonymous well groups", int(df["Well_ID"].nunique()), "Retain W01-W06 for grouping only"],
        ["Exact duplicate rows", int(df.duplicated().sum()), "No removal"],
        ["Duplicate Well_ID-MD keys", int(df.duplicated(["Well_ID", "MD"]).sum()), "No removal"],
        ["Adjacent repeated states", int(adjacent.sum()), "Retain and disclose"],
        ["Consecutive state blocks", int(len(df) - adjacent.sum()), "Use as dependence evidence"],
    ]
    return pd.DataFrame(rows, columns=["Check", "Count", "Treatment"])


def classification_metrics(y_true: pd.Series | np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray) -> dict[str, float]:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Balanced_Accuracy": balanced_accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, zero_division=0),
        "Sensitivity": recall_score(y_true, y_pred, zero_division=0),
        "Specificity": tn / (tn + fp) if (tn + fp) else np.nan,
        "F1": f1_score(y_true, y_pred, zero_division=0),
        "MCC": matthews_corrcoef(y_true, y_pred) if len(np.unique(y_true)) > 1 else np.nan,
        "ROC_AUC": roc_auc_score(y_true, y_prob) if len(np.unique(y_true)) > 1 else np.nan,
        "PR_AUC": average_precision_score(y_true, y_prob) if len(np.unique(y_true)) > 1 else np.nan,
        "Brier": brier_score_loss(y_true, y_prob),
        "TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp),
    }


def classifier_models() -> dict[str, Any]:
    return {
        "Logistic regression": Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(C=1.0, max_iter=1000, solver="lbfgs")),
        ]),
        "Pruned CART": DecisionTreeClassifier(max_depth=4, min_samples_leaf=50, random_state=SEED),
        "Random forest": RandomForestClassifier(
            n_estimators=200, max_depth=8, min_samples_leaf=25,
            random_state=SEED, n_jobs=1,
        ),
        "Gradient boosting": GradientBoostingClassifier(
            n_estimators=150, learning_rate=0.05, max_depth=2,
            min_samples_leaf=20, random_state=SEED,
        ),
    }


def leave_one_well_out_predictions(df: pd.DataFrame, model: Any, features: list[str]) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, float]]:
    X = df[features]
    y = df["NTG"].astype(int)
    groups = df["Well_ID"]
    pred = np.zeros(len(df), dtype=int)
    prob = np.zeros(len(df), dtype=float)
    fold_rows: list[dict[str, Any]] = []

    for train_idx, test_idx in LeaveOneGroupOut().split(X, y, groups):
        held = groups.iloc[test_idx].iloc[0]
        fitted = deepcopy(model)
        fitted.fit(X.iloc[train_idx], y.iloc[train_idx])
        fold_prob = fitted.predict_proba(X.iloc[test_idx])[:, 1]
        fold_pred = (fold_prob >= 0.5).astype(int)
        pred[test_idx] = fold_pred
        prob[test_idx] = fold_prob
        row = {"Well_ID": held, "N": len(test_idx), "Pay_Share": y.iloc[test_idx].mean()}
        row.update(classification_metrics(y.iloc[test_idx], fold_pred, fold_prob))
        fold_rows.append(row)

    pooled = classification_metrics(y, pred, prob)
    fold_df = pd.DataFrame(fold_rows).sort_values("Well_ID")
    pooled["Macro_Balanced_Accuracy"] = fold_df["Balanced_Accuracy"].mean()
    predictions = pd.DataFrame({
        "Well_ID": df["Well_ID"], "MD": df["MD"], "Actual_NTG": y,
        "Predicted_NTG": pred, "Pay_Probability": prob,
    })
    return predictions, fold_df, pooled


def grouped_model_comparison(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, model in classifier_models().items():
        _, folds, pooled = leave_one_well_out_predictions(df, model, PRIMARY_FEATURES)
        rows.append({
            "Model": name,
            "Grouped_Pooled_Balanced_Accuracy": pooled["Balanced_Accuracy"],
            "Grouped_Macro_Balanced_Accuracy": folds["Balanced_Accuracy"].mean(),
            "Brier": pooled["Brier"],
            "ROC_AUC": pooled["ROC_AUC"],
        })
    return pd.DataFrame(rows)


def random_split_comparison(df: pd.DataFrame, seeds: list[int] | None = None) -> pd.DataFrame:
    seeds = seeds or list(range(SEED, SEED + 20))
    X = df[PRIMARY_FEATURES]
    y = df["NTG"].astype(int)
    grouped = grouped_model_comparison(df).set_index("Model")
    rows = []
    for name, model in classifier_models().items():
        scores = []
        for seed in seeds:
            train_idx, test_idx = train_test_split(
                np.arange(len(df)), test_size=0.30, stratify=y, random_state=seed
            )
            fitted = deepcopy(model)
            fitted.fit(X.iloc[train_idx], y.iloc[train_idx])
            scores.append(balanced_accuracy_score(y.iloc[test_idx], fitted.predict(X.iloc[test_idx])))
        gp = grouped.loc[name, "Grouped_Pooled_Balanced_Accuracy"]
        rows.append({
            "Model": name,
            "Seed_Set": "|".join(map(str, seeds)),
            "Random_70_30_Mean_Balanced_Accuracy": np.mean(scores),
            "Random_70_30_SD": np.std(scores, ddof=1),
            "Grouped_Pooled_Balanced_Accuracy": gp,
            "Random_Minus_Grouped": np.mean(scores) - gp,
        })
    return pd.DataFrame(rows)


def selected_model_details(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    X = df[PRIMARY_FEATURES]
    y = df["NTG"].astype(int)
    groups = df["Well_ID"]
    coef_rows, perm_rows, cart_rows, split_rows = [], [], [], []

    for train_idx, test_idx in LeaveOneGroupOut().split(X, y, groups):
        held = groups.iloc[test_idx].iloc[0]
        split_rows.append({
            "fold": held,
            "held_out_well": held,
            "training_wells": "|".join(sorted(groups.iloc[train_idx].unique())),
            "train_rows": len(train_idx), "test_rows": len(test_idx),
            "test_pay_rows": int(y.iloc[test_idx].sum()),
            "test_nonpay_rows": int((1 - y.iloc[test_idx]).sum()),
        })
        pipe = classifier_models()["Logistic regression"]
        pipe.fit(X.iloc[train_idx], y.iloc[train_idx])
        clf = pipe.named_steps["classifier"]
        coef_rows.append({
            "Held_Out_Well": held,
            "VSH_Coefficient": clf.coef_[0][0],
            "PHIT_Coefficient": clf.coef_[0][1],
            "Intercept": clf.intercept_[0],
        })
        perm = permutation_importance(
            pipe, X.iloc[test_idx], y.iloc[test_idx],
            scoring="balanced_accuracy", n_repeats=20, random_state=SEED,
        )
        for feat, mean, sd in zip(PRIMARY_FEATURES, perm.importances_mean, perm.importances_std):
            perm_rows.append({"Held_Out_Well": held, "Feature": feat, "Importance_Mean": mean, "Importance_SD": sd})
        cart = classifier_models()["Pruned CART"]
        cart.fit(X.iloc[train_idx], y.iloc[train_idx])
        for node_id, feat_idx in enumerate(cart.tree_.feature):
            if feat_idx >= 0:
                cart_rows.append({
                    "Held_Out_Well": held, "Node_ID": node_id,
                    "Feature": PRIMARY_FEATURES[feat_idx],
                    "Threshold": cart.tree_.threshold[node_id], "Is_Root": node_id == 0,
                })
    return (
        pd.DataFrame(coef_rows), pd.DataFrame(perm_rows),
        pd.DataFrame(cart_rows), pd.DataFrame(split_rows),
    )


def k_proxy_audit(df: pd.DataFrame) -> dict[str, float]:
    model = DecisionTreeClassifier(max_depth=4, min_samples_leaf=50, random_state=SEED)
    _, _, pooled = leave_one_well_out_predictions(df, model, ["K"])
    return pooled


def missingness_sensitivity(root: str | Path | None = None) -> tuple[pd.DataFrame, dict[str, float]]:
    root = repo_root(root)
    df = pd.read_csv(root / "data" / "simulated" / "All_Wells_with_Well_ID_missing_values.txt", sep="\t")
    X = df[PRIMARY_FEATURES]
    y = df["NTG"].astype(int)
    groups = df["Well_ID"]
    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(C=1.0, max_iter=1000, solver="lbfgs")),
    ])
    return leave_one_well_out_predictions(df, model, PRIMARY_FEATURES)[0], leave_one_well_out_predictions(df, model, PRIMARY_FEATURES)[2]


def rt_model_comparison(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, np.ndarray]]:
    X = df[["VSH"]]
    y = df["RT"].astype(float)
    groups = df["Well_ID"]
    models = {
        "Linear VSH": (LinearRegression(), True),
        "Quadratic VSH": (Pipeline([("poly", PolynomialFeatures(2, include_bias=False)), ("reg", LinearRegression())]), True),
        "Random forest VSH": (RandomForestRegressor(n_estimators=200, random_state=SEED, n_jobs=1), True),
        "Gradient boosting VSH": (GradientBoostingRegressor(n_estimators=150, learning_rate=0.05, max_depth=2, min_samples_leaf=20, random_state=SEED), False),
    }
    rows, prediction_map = [], {}
    for name, (model, log_target) in models.items():
        pred = np.zeros(len(df), dtype=float)
        per_well = []
        target = np.log10(y) if log_target else y
        for train_idx, test_idx in LeaveOneGroupOut().split(X, target, groups):
            fitted = deepcopy(model)
            fitted.fit(X.iloc[train_idx], target.iloc[train_idx])
            fold = fitted.predict(X.iloc[test_idx])
            if log_target:
                fold = 10 ** fold
            pred[test_idx] = fold
            per_well.append({
                "MAE": mean_absolute_error(y.iloc[test_idx], fold),
                "RMSE": mean_squared_error(y.iloc[test_idx], fold) ** 0.5,
                "R2": r2_score(y.iloc[test_idx], fold),
            })
        prediction_map[name] = pred
        rows.append({
            "Model": name,
            "Pooled_MAE_ohm_m": mean_absolute_error(y, pred),
            "Pooled_RMSE_ohm_m": mean_squared_error(y, pred) ** 0.5,
            "Pooled_R2": r2_score(y, pred),
            "Macro_MAE_ohm_m": np.mean([r["MAE"] for r in per_well]),
            "Macro_R2": np.mean([r["R2"] for r in per_well]),
        })
    return pd.DataFrame(rows), prediction_map


def export_figures(df: pd.DataFrame, metrics_by_well: pd.DataFrame, pooled: dict[str, float], predictions: pd.DataFrame, root: Path) -> None:
    figdir = root / "figures"
    figdir.mkdir(exist_ok=True)

    pay = df.groupby("Well_ID")["NTG"].mean()
    fig, ax = plt.subplots(figsize=(7.5, 4.5)); ax.bar(pay.index, pay.values); ax.set_ylim(0, 1)
    ax.set_xlabel("Anonymous well group"); ax.set_ylabel("Pay-indicator share"); ax.set_title("Pay-Indicator Prevalence by Well")
    for i, value in enumerate(pay): ax.text(i, value + .025, f"{value:.1%}", ha="center", fontsize=9)
    fig.tight_layout(); fig.savefig(figdir / "pay_share_by_well.png", dpi=200); plt.close(fig)

    corr = df[["MD","TVDSS","ZONE","VSH","SW","RT","PHIT","NTG","K"]].corr(method="spearman")
    fig, ax = plt.subplots(figsize=(7.5, 6.2)); im = ax.imshow(corr.values, vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right"); ax.set_yticks(range(len(corr.columns)), corr.columns)
    ax.set_title("Spearman Correlation Matrix")
    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)): ax.text(j, i, f"{corr.iloc[i,j]:.2f}", ha="center", va="center", fontsize=7)
    fig.colorbar(im, ax=ax, fraction=.046, pad=.04); fig.tight_layout(); fig.savefig(figdir / "spearman_correlation_matrix.png", dpi=200); plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.5,4.5)); ax.bar(metrics_by_well["Well_ID"], metrics_by_well["Balanced_Accuracy"])
    ax.axhline(pooled["Balanced_Accuracy"], linestyle="--", label="Pooled balanced accuracy"); ax.set_ylim(0,1)
    ax.set_xlabel("Held-out well"); ax.set_ylabel("Balanced accuracy"); ax.set_title("Leave-One-Well-Out Performance"); ax.legend()
    fig.tight_layout(); fig.savefig(figdir / "balanced_accuracy_by_well.png", dpi=200); plt.close(fig)

    y_true = predictions["Actual_NTG"].astype(int); y_pred = predictions["Predicted_NTG"].astype(int)
    cm = confusion_matrix(y_true, y_pred, labels=[0,1])
    fig, ax = plt.subplots(figsize=(5.5,4.8)); im=ax.imshow(cm); ax.set_xticks([0,1],["Predicted non-pay","Predicted pay"]); ax.set_yticks([0,1],["Actual non-pay","Actual pay"])
    ax.set_title("Pooled Leave-One-Well-Out Confusion Matrix")
    for i in range(2):
        for j in range(2): ax.text(j,i,str(cm[i,j]),ha="center",va="center",fontsize=13)
    fig.colorbar(im,ax=ax,fraction=.046,pad=.04); fig.tight_layout(); fig.savefig(figdir / "pooled_confusion_matrix.png", dpi=200); plt.close(fig)

    obs, mean_prob = calibration_curve(y_true, predictions["Pay_Probability"], n_bins=10, strategy="quantile")
    fig, ax=plt.subplots(figsize=(5.8,5)); ax.plot([0,1],[0,1],linestyle="--",label="Perfect calibration"); ax.plot(mean_prob,obs,marker="o",label="Selected model")
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_xlabel("Mean predicted pay probability"); ax.set_ylabel("Observed pay frequency"); ax.set_title("Probability Calibration"); ax.legend()
    fig.tight_layout(); fig.savefig(figdir / "calibration_curve.png", dpi=200); plt.close(fig)


def run_all(root: str | Path | None = None, include_random_splits: bool = True) -> dict[str, Any]:
    root = repo_root(root)
    results = root / "results"; results.mkdir(exist_ok=True)
    models_dir = root / "models"; models_dir.mkdir(exist_ok=True)
    df = load_processed(root)

    predictions, well_metrics, pooled = leave_one_well_out_predictions(
        df, classifier_models()["Logistic regression"], PRIMARY_FEATURES
    )
    predictions.to_csv(results / "predictions_by_well.csv", index=False)
    well_metrics.to_csv(results / "metrics_by_well.csv", index=False)
    pd.DataFrame([{"Metric": k, "Value": v} for k, v in pooled.items()]).to_csv(results / "pooled_classification_metrics.csv", index=False)

    comparison = grouped_model_comparison(df)
    comparison.to_csv(results / "model_comparison_grouped_computed.csv", index=False)
    if include_random_splits:
        random_split_comparison(df).to_csv(results / "random_vs_grouped_validation_computed.csv", index=False)

    coef, perm, cart, splits = selected_model_details(df)
    coef.to_csv(results / "logistic_coefficients_by_fold.csv", index=False)
    perm.to_csv(results / "permutation_importance_by_fold.csv", index=False)
    cart.to_csv(results / "cart_thresholds_by_fold.csv", index=False)
    splits.to_csv(results / "split_manifest.csv", index=False)

    k = k_proxy_audit(df)
    pd.DataFrame([{"Feature": "K", **k}]).to_csv(results / "single_feature_proxy_audit_computed.csv", index=False)

    missing_predictions, missing = missingness_sensitivity(root)
    pd.DataFrame([missing]).to_csv(results / "missingness_sensitivity_computed.csv", index=False)

    rt_table, _ = rt_model_comparison(df)
    rt_table.to_csv(results / "rt_model_comparison_computed.csv", index=False)

    selected = classifier_models()["Logistic regression"]
    selected.fit(df[PRIMARY_FEATURES], df["NTG"].astype(int))
    dump(selected, models_dir / "final_logistic_vsh_phit.joblib")

    export_figures(df, well_metrics, pooled, predictions, root)
    summary = {
        "selected_model": "Standardized logistic regression using VSH and PHIT",
        "pooled_metrics": pooled,
        "k_proxy_metrics": k,
        "missingness_metrics": missing,
    }
    (results / "pipeline_run_summary.json").write_text(json.dumps(summary, indent=2, default=float), encoding="utf-8")
    return summary
