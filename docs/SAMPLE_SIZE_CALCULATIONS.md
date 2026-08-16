# Sample-Size Calculations

The final nominal sample size is the maximum of the minimum values calculated for all research questions.

## RQ1 - Confidence interval for classification accuracy

\[
n = \frac{z^2 p(1-p)}{e^2}
\]

Using \(z=1.96\), \(p=0.50\), and margin \(e=0.03\):

\[
n = \frac{1.96^2(0.50)(0.50)}{0.03^2}=1067.11 \Rightarrow 1,068
\]

## RQ2 - Green's rule for multivariable modeling

\[
n \geq 50 + 8m
\]

For five candidate predictors:

\[
n \geq 50 + 8(5)=90
\]

## RQ3 - Power for a correlation

Using Fisher's z transformation with \(\alpha=.05\), power \(=.80\), and expected \(r=.30\):

\[
n = \left[\frac{z_{1-\alpha/2}+z_{1-\beta}}{\tanh^{-1}(r)}\right]^2 + 3 \approx 85
\]

## RQ4 - Confidence interval for category agreement

Using \(z=1.96\), \(p=0.50\), and margin \(e=0.05\):

\[
n = \frac{1.96^2(0.50)(0.50)}{0.05^2}=384.16 \Rightarrow 385
\]

## Final nominal requirement

\[
N_{min}=\max(1068,90,85,385)=1068
\]

The dataset exceeds the row-level requirement with 8,468 observations. However, rows within a well are strongly dependent, so the number of wells, per-well performance, and grouped uncertainty are more important than row count alone.
