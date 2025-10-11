import sys
from pathlib import Path

# Ensure src/ is on sys.path for tests (robust against editable install issues)
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
