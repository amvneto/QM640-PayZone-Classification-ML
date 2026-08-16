# Model Card - Reduced Logistic Pay-Indicator Model

## Model details

- Model: Logistic regression
- Features: VSH and PHIT
- Preprocessing: StandardScaler fitted inside each training fold
- C: 1.0
- Classification threshold: 0.50
- Validation: Leave-one-well-out across W01-W06
- Positive class: NTG = 1, described as the available pay indicator

## Intended use

Academic and technical decision support for evaluating grouped generalization, calibration, explainability, and leakage risk.

## Not intended for

Economic pay certification, autonomous drilling, automatic tool selection, reserves estimation, production forecasting, or use outside the documented data range without external validation.

## Performance

- Pooled accuracy: 0.915
- Pooled balanced accuracy: 0.904
- Macro balanced accuracy: 0.836
- ROC-AUC: 0.959
- PR-AUC: 0.953
- Brier score: 0.069

## Known failure

W04: N = 99, pay share = 74.7%, balanced accuracy = 0.514, sensitivity = 0.027, Brier = 0.689.

## Feature interpretation

- PHIT has a stable positive association with the available pay indicator.
- VSH has a stable negative association.
- Approximate PHIT tree thresholds are dataset-specific and must not be treated as universal cutoffs.

## Risks

- NTG lineage is incomplete.
- K nearly encodes the target.
- Adjacent repeated states make random row validation optimistic.
- The six wells do not establish external field transferability.
- W04 demonstrates potential domain shift.

## Governance

The model is advisory only. Expert review is mandatory for any operational application.
