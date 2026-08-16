# Feature-Lineage Audit

A feature-lineage audit records where every variable came from, whether it was available at the intended decision time, whether it shares inputs with the target, and how it is permitted to enter the model.

The machine-readable register is `data/dictionary/feature_lineage_register.csv`.

## Final classification controls

- `Well_ID`: grouping only
- `MD`, `TVDSS`: quality control and ordering only
- `ZONE`: diagnostic ablation only
- `VSH`: retained cautiously
- `SW`: excluded from primary model
- `RT`: excluded from primary classifier; RQ4 target only
- `PHIT`: retained and tested across wells
- `NTG`: target only
- `K`: excluded due severe target-proxy evidence

## Key conclusion

Separate columns are not automatically independent. The K-only result demonstrates why high accuracy cannot be accepted before the data-generating lineage is audited.
