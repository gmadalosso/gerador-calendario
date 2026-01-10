import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from mangum import Mangum
from app.main import app

handler = Mangum(app, lifespan="off")

