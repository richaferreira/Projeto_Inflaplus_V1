
from datetime import datetime
from backend.app.extensions import db

class Report(db.Model):

    # Empresa responsável atribuída a esta denúncia
    assigned_company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True, nullable=True)
    assigned_company = db.relationship('Company', backref=db.backref('reports', lazy='dynamic'))

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Aberta', nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    address = db.Column(db.String(200))
    image_filename = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    comments = db.relationship('Comment', backref='report', lazy=True, cascade='all, delete-orphan')
    images = db.relationship('ReportImage', backref='report', lazy=True, cascade='all, delete-orphan')