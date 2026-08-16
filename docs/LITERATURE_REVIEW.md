# Literature Review and Relevance Matrix

The literature review was organized around directional-resistivity decision value, machine learning for well-log interpretation, structured validation, probability calibration, explainability, and uncertainty.

| Source | Context/method | Key contribution | Project use |
|---|---|---|---|
| Vianna (2025) | Laminated-reservoir case; pseudo-RT and CART | Establishes the published benchmark and operational motivation | Baseline for all RQs |
| Hartmann et al. (2014) | Directional-resistivity verification | Sensitivity depends on contrast and measurement design | Physical basis and RQ4 limits |
| Larsen et al. (2015) | Complex-reservoir navigation | Deeper measurements can change navigation decisions | Business context and expert review |
| Brazell et al. (2019) | Assistive well-log correlation | ML can scale interpretation when validation matches intended use | Multiwell analytics |
| Breiman et al. (1984) | CART | Trees expose rules but may overfit | Interpretable benchmark |
| Breiman (2001) | Random forest | Bagging reduces single-tree variance | Nonlinear benchmark |
| Chen and Guestrin (2016) | Gradient boosting | Efficient nonlinear tabular learning | Nonlinear benchmark |
| Roberts et al. (2017) | Structured cross-validation | Random CV is optimistic under dependence | Leave-one-well-out design |
| Varma and Simon (2006) | Model-selection bias | Tuning and final testing must remain separate | Frozen outer-fold evaluation |
| Brier (1950) | Probabilistic forecasts | Squared probability error measures probability quality | Brier score |
| Niculescu-Mizil and Caruana (2005) | Classifier calibration | Good discrimination does not ensure calibrated probabilities | Reliability assessment |
| Lundberg and Lee (2017) | Explainability | Consistent local/global feature attribution | Explainability framework |
| Angelopoulos and Bates (2023) | Conformal prediction | Distribution-light uncertainty framework | Grouped interval design |

The review does not treat performance from other reservoirs or domains as direct evidence of transferability to the six anonymous wells.
