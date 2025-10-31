from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from backend.app import create_app
from backend.app.extensions import db

app = create_app()
with app.app_context():
    try:
        db.session.execute("ALTER TABLE report ADD COLUMN assigned_company_id INTEGER;")
    except Exception:
        pass
    try:
        db.session.execute("CREATE INDEX ix_report_assigned_company_id ON report (assigned_company_id);")
    except Exception:
        pass
    db.session.commit()
    print("OK: coluna assigned_company_id pronta.")