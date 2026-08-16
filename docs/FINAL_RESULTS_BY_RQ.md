# Final Results by Research Question

## RQ1 - Classification on unseen wells

The selected standardized logistic model using VSH and PHIT achieved:

| Metric | Pooled result |
|---|---:|
| Accuracy | 0.915 |
| Balanced accuracy | 0.904 |
| Precision | 0.925 |
| Sensitivity | 0.854 |
| Specificity | 0.955 |
| F1 | 0.888 |
| MCC | 0.821 |
| ROC-AUC | 0.959 |
| PR-AUC | 0.953 |
| Brier | 0.069 |
| Macro balanced accuracy | 0.836 |

W04 failed with accuracy 0.273, balanced accuracy 0.514, ROC-AUC 0.369, and Brier 0.689. The model therefore supports conditional advisory use, not universal transfer.

## RQ2 - Validation and proxy effects

Random row splits were more optimistic for nonlinear models. More importantly, K alone achieved balanced accuracy 0.996, ROC-AUC 0.998, and Brier 0.003. K is treated as a severe target proxy and excluded.

## RQ3 - Stable drivers

Mean standardized coefficients across the six grouped folds:

- PHIT: +4.041 (SD 0.509)
- VSH: -1.525 (SD 0.129)

CART selected PHIT at the root in every fold with thresholds from 0.16105 to 0.17110. These are dataset-specific hypotheses, not universal petrophysical cutoffs.

## RQ4 - RT reconstruction

The reported random-forest result was MAE 0.038 ohm-m, RMSE 0.714 ohm-m, and R-squared 0.983. However, VSH and RT are essentially perfect inverse ranks. This is reconstruction of a supplied relationship, not independent physical validation. The dataset lacks boundary geometry, depth-of-detection labels, service costs, and expert tool-selection outcomes.

## Controlled missingness

With the simulated missingness file, pooled balanced accuracy changed from 0.904 to 0.895, and Brier changed from 0.069 to 0.076. This is a limited missing-at-random stress test, not evidence about structured acquisition failure.
