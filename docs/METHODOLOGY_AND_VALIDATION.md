# Methodology and Validation Protocol

## Primary feature set

`VSH` and `PHIT` only.

## Candidate classifiers

- Standardized logistic regression: C = 1, probability threshold = 0.50
- Pruned CART: max depth = 4, minimum leaf = 50
- Random forest: 200 trees, max depth = 8, minimum leaf = 25
- Gradient boosting: 150 trees, learning rate = 0.05, max depth = 2, minimum leaf = 20

## Outer validation

Leave one complete `Well_ID` out. The held-out well contributes no rows to fitting, preprocessing, model selection, or probability calibration.

## Required validation sequence

1. Freeze the input file, schema, row counts, and hashes.
2. Hold out one complete well.
3. Fit preprocessing only on the remaining wells.
4. Fit the model with frozen settings.
5. Score the held-out well once.
6. Save probabilities, classes, confusion counts, and metrics.
7. Repeat for W01-W06.
8. Report pooled and unweighted macro results.

## Diagnostic random split

Repeated stratified 70/30 row splits are used only to quantify optimism. They are not the primary evidence.

## Missingness sensitivity

The controlled missingness file is evaluated with training-fold median imputation for VSH and PHIT, followed by the same scaling and grouped logistic model.

## RQ4

RT is modeled from VSH as a lineage test. High numerical performance is interpreted cautiously because VSH and RT are essentially rank-equivalent in the released data.
