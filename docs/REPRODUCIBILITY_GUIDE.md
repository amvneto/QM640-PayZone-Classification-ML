# Reproducibility Guide

## Required environment

Install the exact versions in `requirements.txt`.

## Required run order

1. `01_data_inventory.ipynb`
2. `02_data_cleaning.ipynb`
3. `03_exploratory_analysis.ipynb`
4. `04_feature_lineage_audit.ipynb`
5. `05_baseline_models.ipynb`
6. `06_grouped_classification.ipynb`
7. `07_calibration_and_missingness.ipynb`
8. `08_explainability.ipynb`
9. `09_rt_reconstruction.ipynb`
10. `10_final_exports_and_tool_screening.ipynb`

## Verification requirements

- Confirm raw-file checksum and 8,468 rows.
- Confirm six groups W01-W06 in the processed copy.
- Confirm no source missing values and no exact duplicates.
- Confirm all preprocessing is fitted inside training folds.
- Confirm `Well_ID`, `MD`, and `TVDSS` do not enter the selected predictor matrix.
- Confirm every held-out row receives exactly one prediction.
- Compare regenerated CSV outputs with the versioned files in `results/`.
- Confirm reports contain no identifying names or metadata.

## Minimum reproducibility evidence

`split_manifest.csv`, `predictions_by_well.csv`, `metrics_by_well.csv`, `calibration_results.csv`, coefficient and importance tables, model configuration, environment file, model card, and final figure exports.
