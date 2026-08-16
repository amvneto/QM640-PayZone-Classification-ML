# GitHub Upload Checklist

## Root

- [ ] README.md
- [ ] requirements.txt
- [ ] CITATION.cff
- [ ] DATA_USE_NOTICE.md
- [ ] CHANGELOG.md
- [ ] PROJECT_MANIFEST.csv
- [ ] .gitignore

## Data

- [ ] Raw file unchanged in `data/raw/`
- [ ] Processed Well_ID file in `data/processed/`
- [ ] Simulated missingness files in `data/simulated/`
- [ ] Dictionary, lineage, cleaning, and anonymization CSVs in `data/dictionary/`

## Documentation

- [ ] All files listed in `docs/README.md`

## Results and figures

- [ ] Per-well predictions and metrics
- [ ] Split manifest
- [ ] Calibration output
- [ ] Explainability tables
- [ ] Proxy audit
- [ ] RT comparison
- [ ] Non-identifying figure files

## Reports

- [ ] Interim report PDF
- [ ] Final report PDF
- [ ] Mentor presentation
- [ ] Target-leakage explainer

## Security and anonymity

- [ ] No secrets or tokens
- [ ] No original names, maps, coordinates, or identifying screenshots
- [ ] No copyrighted paper PDFs unless redistribution is permitted
- [ ] No temporary files or duplicate archives

## Final repository test

Clone into a clean directory, install `requirements.txt`, execute the numbered notebooks, and compare regenerated outputs with the committed result files.
