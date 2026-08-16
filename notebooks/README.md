# Notebook Execution Plan

The capstone requires numbered notebooks so the evaluator can reproduce the workflow in order.

1. `01_data_inventory.ipynb` - schema, counts, hashes, groups, ranges
2. `02_data_cleaning.ipynb` - Well_ID creation, QC log, processed export
3. `03_exploratory_analysis.ipynb` - distributions, class balance, correlations
4. `04_feature_lineage_audit.ipynb` - lineage table, proxy tests, ablations
5. `05_baseline_models.ipynb` - logistic and CART baselines
6. `06_grouped_classification.ipynb` - leave-one-well-out model comparison
7. `07_calibration_and_missingness.ipynb` - Brier, reliability, simulated blanks
8. `08_explainability.ipynb` - coefficients, permutation importance, thresholds, SHAP when used
9. `09_rt_reconstruction.ipynb` - grouped RT reconstruction and circularity audit
10. `10_final_exports_and_tool_screening.ipynb` - final tables, figures, model card, advisory gate

Each notebook should:

- declare inputs and outputs at the top;
- use relative paths;
- avoid manual edits to generated data;
- save evidence to `results/` and `figures/`;
- finish with a concise interpretation linked to the relevant research question.

## Included notebooks

All ten numbered notebooks are included in this repository package. Run them from the repository root or from the `notebooks/` directory.
