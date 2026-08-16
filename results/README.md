# Results

This folder contains the machine-readable evidence cited by the final report.

## Required files

- `pooled_classification_metrics.csv`
- `metrics_by_well.csv`
- `predictions_by_well.csv`
- `split_manifest.csv`
- `calibration_results.csv`
- `logistic_coefficients_by_fold.csv`
- `permutation_importance_by_fold.csv`
- `cart_thresholds_by_fold.csv`
- `single_feature_proxy_audit.csv`
- `model_comparison_grouped.csv`
- `random_vs_grouped_validation.csv`
- `missingness_sensitivity.csv`
- `rt_model_comparison.csv`
- `final_results_summary.json`

Reported metrics must remain traceable to a frozen data version and a documented validation design. Do not replace per-well evidence with pooled results alone.

## Regenerated outputs

Running `python src/run_all.py` also creates files suffixed `_computed.csv` and `pipeline_run_summary.json`. These are environment-verified outputs from the included source implementation. The unsuffixed CSVs preserve the result tables cited in the submitted final report.
