import sys, os, sqlite3
sys.path.insert(0, r"C:\Users\PC1\Desktop\gfgffg")
from backend.app import create_app

app = create_app()
uri = app.config.get("SQLALCHEMY_DATABASE_URI")
print("DB URI:", uri)

if not (isinstance(uri, str) and uri.lower().startswith("sqlite")):
    raise SystemExit("Este script é só para SQLite. URI atual: " + str(uri))

db_path = uri.split("///",1)[1] if "///" in uri else uri.replace("sqlite:///", "")
print("DB PATH:", db_path)

con = sqlite3.connect(db_path)
cur = con.cursor()

cur.execute("PRAGMA table_info(report)")
cols = [r[1] for r in cur.fetchall()]
print("COLS ANTES:", cols)

if "assigned_company_id" not in cols:
    cur.execute("ALTER TABLE report ADD COLUMN assigned_company_id INTEGER")
    try:
        cur.execute("CREATE INDEX ix_report_assigned_company_id ON report (assigned_company_id)")
    except sqlite3.OperationalError:
        pass
    con.commit()
    print(">> Coluna/índice criados.")

cur.execute("PRAGMA table_info(report)")
print("COLS DEPOIS:", [r[1] for r in cur.fetchall()])

con.close()
