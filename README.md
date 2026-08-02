# QM640 PayZone Classification ML

## Project overview

This repository contains the code, notebooks, data artifacts (anonymized), and documentation for the QM640 Data Analytics Capstone project: PayZone classification using well-level data and machine learning. The project includes data loading and cleaning, exploratory data analysis, model development and validation, explainability, and final exports for downstream use.

## Research questions

- Can well-level features be used to accurately classify PayZone presence? 
- Which features are most predictive of PayZone? 
- How well do the models generalize across different wells/regions and what are their uncertainty characteristics? 

## Data-use statement

- Only anonymized, non-identifying data are stored in this repository. No personal, proprietary, or geospatial-identifying information (names, maps, coordinates, proprietary reports) is included.
- Original anonymized source files are placed in data/raw/ and must not be modified by hand. All cleaning and transformations are performed by code that writes into data/processed/.
- Any external datasets used must be cited in the notebooks and accompanied by usage rights and license information in docs/.

## Installation

1. Create a Python virtual environment (recommended):

   python -m venv .venv
   source .venv/bin/activate  # macOS / Linux
   .venv\Scripts\activate     # Windows (PowerShell)

2. Install dependencies:

   pip install -r requirements.txt

3. (Optional) If you prefer conda:

   conda create -n qm640 python=3.10
   conda activate qm640
   pip install -r requirements.txt

## Run order

The notebooks follow a numbered order to reproduce the analysis from data ingestion through model exports. Example run order:

1. notebooks/01_data_loading_and_exploration.ipynb — load data from data/raw/, basic checks.
2. notebooks/02_data_cleaning_and_feature_engineering.ipynb — generate cleaned tables and save to data/processed/.
3. notebooks/03_exploratory_data_analysis.ipynb — EDA and feature inspection.
4. notebooks/04_modeling_and_training.ipynb — model training and cross-validation.
5. notebooks/05_model_evaluation_and_explainability.ipynb — evaluation metrics, calibration, explainability (SHAP, feature importance).
6. notebooks/06_final_exports_and_results.ipynb — produce per-well predictions, results tables, and figures saved to results/ and figures/.

If scripts are provided in src/, they can be used to run steps programmatically (see src/ README or function docstrings).

## Citation

If you use this work in publications, please cite as:

- Author: A. M. Neto (2026). QM640 PayZone Classification ML. GitHub repository, https://github.com/amvneto/QM640-PayZone-Classification-ML

Suggested BibTeX:

@misc{amvneto2026qm640,
  author = {A. M. Neto},
  title = {QM640 PayZone Classification ML},
  year = {2026},
  howpublished = {GitHub repository},
  note = {\url{https://github.com/amvneto/QM640-PayZone-Classification-ML}}
}
