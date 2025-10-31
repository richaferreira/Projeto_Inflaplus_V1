
from datetime import datetime
from math import ceil
from sqlalchemy import func, or_
from backend.app.models import Report
from backend.app.extensions import db

class ReportRepository:
    @staticmethod
    def apply_filters(query, categoria=None, status=None, de=None, ate=None, qtext=None):
        if categoria:
            query = query.filter(Report.category == categoria)
        if status:
            query = query.filter(Report.status == status)
        if qtext:
            like = f"%{qtext.strip()}%"
            query = query.filter(or_(Report.title.ilike(like), Report.description.ilike(like)))
        def parse(s):
            try:
                return datetime.strptime(s, '%Y-%m-%d') if s else None
            except Exception:
                return None
        d0, d1 = parse(de), parse(ate)
        if d0:
            query = query.filter(Report.created_at >= d0)
        if d1:
            query = query.filter(Report.created_at < d1.replace(hour=23, minute=59, second=59))
        return query

    @staticmethod
    def paginate(query, page=1, per_page=9):
        page = max(1, int(page or 1))
        total = query.count()
        items = query.limit(per_page).offset((page-1)*per_page).all()
        pages = ceil(total / per_page) if per_page else 1
        return items, total, page, pages

    @staticmethod
    def daily_counts_7d():
        from datetime import datetime, timedelta
        today = datetime.utcnow().date()
        days = [(today - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
        counts = {d: 0 for d in days}
        rows = db.session.query(func.date(Report.created_at), func.count(Report.id)).group_by(func.date(Report.created_at)).all()
        for d, c in rows:
            ds = d if isinstance(d, str) else d.isoformat()
            if ds in counts:
                counts[ds] = c
        series7 = [counts[d] for d in days]
        return days, series7
