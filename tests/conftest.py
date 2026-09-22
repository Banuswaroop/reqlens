import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

APP_DIRECTORY = PROJECT_ROOT / "app"


sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

sys.path.insert(
    0,
    str(APP_DIRECTORY)
)