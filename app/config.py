from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


REQUIREMENTS_FILE = (
    PROJECT_ROOT / "requirements_input.txt"
)

REPORT_FILE = (
    PROJECT_ROOT / "reports" / "reqlens_report.txt"
)

PDF_REPORT_FILE = (
    PROJECT_ROOT / "reports" / "reqlens_report.pdf"
)

LOG_FILE = (
    PROJECT_ROOT / "logs" / "reqlens.log"
)

AUTOMATION_INTERVAL = 2

MODEL_FILE = (
    PROJECT_ROOT / "models" / "model.pkl"
)

VECTORIZER_FILE = (
    PROJECT_ROOT / "models" / "vectorizer.pkl"
)

DATASET_FILE = (
    PROJECT_ROOT / "data" / "dataset.csv"
)