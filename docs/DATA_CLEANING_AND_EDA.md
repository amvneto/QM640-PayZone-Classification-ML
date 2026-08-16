# Data Cleaning and Exploratory Analysis

## Final cleaning evidence

| Check | Result | Treatment |
|---|---:|---|
| Source missing values | 0 | No raw imputation |
| Anonymous well groups | 6 | W01-W06 in processed copy |
| Exact duplicate rows | 0 | No removal |
| Duplicate Well_ID-MD keys | 0 | No removal |
| Adjacent repeated states | 6,711 | Retain and disclose |
| Consecutive state blocks | 1,757 | Use as dependence evidence |
| Controlled simulated blanks | 2,538 cells | Fold-only median imputation for VSH/PHIT |

## EDA insights

1. Target prevalence varies materially by well; W04 is approximately 74.7% pay, while W03 is approximately 21.3% pay.
2. MD and TVDSS are redundant location signals and are excluded from the transportable model.
3. VSH and RT are essentially perfect inverse ranks, indicating that RT reconstruction is circular or rule recovery rather than independent physical prediction.
4. K is strongly aligned with NTG and yields near-perfect classification by itself, so it is excluded as a target proxy.
5. Repeated adjacent states mean random row splitting can place nearly identical records in both training and testing data.

Corresponding figures are available under `figures/`.
