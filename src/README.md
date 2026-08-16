# Source Code Requirements

Reusable code should be separated from notebook narration. Recommended modules:

- `data_io.py` - loading, schema checks, path handling
- `preprocessing.py` - grouped transformations and missing-value handling
- `validation.py` - leave-one-well-out and split manifests
- `metrics.py` - classification, calibration, regression, and aggregation
- `modeling.py` - frozen model configurations
- `explainability.py` - coefficients, permutation importance, thresholds, SHAP
- `plotting.py` - non-identifying figures
- `export.py` - result files and manifest generation

No preprocessing step may learn from a held-out well. All code should use relative repository paths and fixed random seeds where randomness is involved.

## Included implementation

- `qm640_pipeline.py` - reusable analysis functions.
- `run_all.py` - command-line pipeline that regenerates core result files, figures, and a serialized full-data demonstration model.
- `__init__.py` - package exports.
