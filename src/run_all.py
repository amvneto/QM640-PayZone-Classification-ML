from pathlib import Path
from qm640_pipeline import run_all

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    summary = run_all(root, include_random_splits=False)
    print("Pipeline completed.")
    print(summary)
