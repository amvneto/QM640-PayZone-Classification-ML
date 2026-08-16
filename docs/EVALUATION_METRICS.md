# Evaluation Metrics

For pay as the positive class:

\[
Accuracy = \frac{TP+TN}{TP+TN+FP+FN}
\]

\[
Precision = \frac{TP}{TP+FP}
\]

\[
Sensitivity = \frac{TP}{TP+FN}
\]

\[
Specificity = \frac{TN}{TN+FP}
\]

\[
F_1 = 2\frac{Precision\times Sensitivity}{Precision+Sensitivity}
\]

\[
Balanced\ Accuracy = \frac{Sensitivity+Specificity}{2}
\]

\[
Brier = \frac{1}{n}\sum_{i=1}^{n}(p_i-y_i)^2
\]

Lower Brier values indicate more accurate probabilities. ROC-AUC measures ranking, while precision-recall AUC is informative under class imbalance. Matthews correlation coefficient summarizes all four confusion-matrix cells.

For RT reconstruction:

\[
MAE = \frac{1}{n}\sum_{i=1}^{n}|y_i-\hat y_i|
\]

\[
RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat y_i)^2}
\]

\[
R^2 = 1-\frac{\sum(y_i-\hat y_i)^2}{\sum(y_i-\bar y)^2}
\]

Pooled metrics summarize all held-out rows. Macro metrics are unweighted means across held-out wells and prevent large wells from dominating the conclusion.
