
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from backend.app.forms import ReportForm, CommentForm
from backend.app.models import Report, Comment, Company
from backend.app.extensions import db
from backend.app.services.report_service import ReportService
from backend.app.repositories.report_repository import ReportRepository

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def home():
    recent = Report.query.order_by(Report.created_at.desc()).limit(8).all()
    markers = []
    for r in Report.query.filter(Report.latitude.isnot(None), Report.longitude.isnot(None)).all():
        markers.append({'id': r.id, 'title': r.title, 'category': r.category, 'status': r.status, 'lat': r.latitude, 'lon': r.longitude})
    return render_template('public/home.html', recent=recent, markers=markers)

@public_bp.route('/denuncias/nova', methods=['GET','POST'])
@login_required
def report_new():
    form = ReportForm()
    # popula empresas (sem filtro por região por enquanto)
    try:
        companies = Company.query.order_by(Company.name.asc()).all()
        if hasattr(form, 'assigned_company_id'):
            form.assigned_company_id.choices = [(0, '— Selecionar —')] + [(c.id, c.name) for c in companies]
    except Exception:
        pass
    if form.validate_on_submit():
        service = ReportService()
        r = service.create_report(form, current_user, request.files)
        flash(f'Denúncia enviada com sucesso! Código #{r.id}', 'success')
        return redirect(url_for('public.report_detail', report_id=r.id))
    return render_template('public/report_new.html', form=form)

# Helper for list pages

def list_reports_filtered(title, base_query):
    repo = ReportRepository
    q = repo.apply_filters(
        base_query.order_by(Report.created_at.desc()),
        categoria=request.args.get('categoria'),
        status=request.args.get('status'),
        de=request.args.get('de'), ate=request.args.get('ate'),
        qtext=request.args.get('q')
    )
    items, total, page, pages = repo.paginate(q, request.args.get('page', 1), 9)
    return render_template('public/reports_list.html', title=title, reports=items, total=total, page=int(page), pages=pages)

@public_bp.route('/denuncias/abertas')
def reports_open():
    return list_reports_filtered('Denúncias Abertas', Report.query.filter_by(status='Aberta'))

@public_bp.route('/denuncias/andamento')
def reports_in_progress():
    return list_reports_filtered('Denúncias Em andamento', Report.query.filter_by(status='Em andamento'))

@public_bp.route('/denuncias/resolvidas')
def reports_resolved():
    return list_reports_filtered('Denúncias Resolvidas', Report.query.filter_by(status='Resolvida'))

@public_bp.route('/denuncias/<int:report_id>', methods=['GET','POST'])
def report_detail(report_id: int):
    r = Report.query.get_or_404(report_id)
    cform = CommentForm()
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Faça login para comentar.', 'warning')
            return redirect(url_for('auth.login', next=url_for('public.report_detail', report_id=report_id)))
        if cform.validate_on_submit():
            author_name = getattr(current_user, 'name', 'Usuário')
            c = Comment(author=author_name, text=cform.text.data.strip(), report=r)
            db.session.add(c)
            db.session.commit()
            flash('Comentário adicionado!', 'success')
            return redirect(url_for('public.report_detail', report_id=report_id))
    return render_template('public/report_detail.html', r=r, cform=cform)
