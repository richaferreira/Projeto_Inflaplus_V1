
from datetime import datetime
from backend.app.extensions import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
