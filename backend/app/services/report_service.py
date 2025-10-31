
from backend.app.extensions import db, mail
from backend.app.models import Report, ReportImage
from backend.app.utils import save_uploaded_image
from flask_mail import Message
from flask import current_app

class ReportService:
    def create_report(self, form, user, files):
        first_filename = save_uploaded_image(form.image.data)
        r = Report(
            title=form.title.data.strip(),
            assigned_company_id=(form.assigned_company_id.data if hasattr(form, 'assigned_company_id') and form.assigned_company_id.data else None),
            description=form.description.data.strip(),
            category=form.category.data,
            status='Aberta',
            address=(form.address.data or '').strip(),
            latitude=form.latitude.data,
            longitude=form.longitude.data,
            image_filename=first_filename,
            author=user,
        )
        db.session.add(r)
        db.session.flush()
        for fs in files.getlist('images'):
            fname = save_uploaded_image(fs)
            if fname:
                db.session.add(ReportImage(report_id=r.id, filename=fname))
        db.session.commit()
        return r

    def notify_status_change(self, report: Report):
        try:
            sender = current_app.config.get('MAIL_DEFAULT_SENDER')
            if not sender:
                return
            msg = Message(subject=f"[InfraPlus] Denúncia #{report.id} agora está '{report.status}'",
                          recipients=[report.author.email],
                          body=f"Olá, {report.author.name}! Sua denúncia #{report.id} teve o status atualizado para '{report.status}'.")
            mail.send(msg)
        except Exception:
            pass
