
from datetime import datetime
from backend.app.extensions import db

class ReportImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
