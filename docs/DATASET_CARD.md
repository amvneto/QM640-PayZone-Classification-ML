# Dataset Card

## Dataset name

QM640 Anonymized Multiwell Pay-Indicator Dataset

## Composition

- 8,468 depth-indexed rows
- Six anonymous well groups: W01-W06
- Source variables: MD, TVDSS, ZONE, VSH, SW, RT, PHIT, NTG, K
- Analysis copy adds Well_ID
- Target: NTG, interpreted as the available pay/non-pay indicator
- Pay rows: 3336 (39.4%)
- Non-pay rows: 5132 (60.6%)

## Intended use

Academic analysis of grouped validation, feature-lineage risk, explainability, calibration, and sensitivity to missing predictor values.

## Not intended for

- independent certification of economic pay;
- autonomous drilling decisions;
- selecting a deep or extra-deep tool without physics-based feasibility work;
- estimating reserves or production;
- re-identifying any company, field, or well.

## Quality characteristics

- No source missing values detected
- No exact duplicate rows
- No duplicate Well_ID-MD pairs
- 6,711 adjacent repeated petrophysical states
- 1,757 consecutive state blocks
- Strongly uneven per-well target prevalence
- Near-deterministic inverse rank relationship between VSH and RT

## Known limitations

Well_ID groups were reconstructed from measured-depth resets, not supplied as original identifiers. The smallest holdout, W04, has only 99 rows and is pay-dominant. Target lineage is incomplete, and K nearly encodes NTG.
