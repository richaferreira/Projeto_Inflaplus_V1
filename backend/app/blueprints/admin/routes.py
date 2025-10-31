from backend.app.forms import CompanyForm
from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from flask_login import login_required
from sqlalchemy import func
from backend.app.models import Report, Company, User
from backend.app.extensions import db
from backend.app.utils import admin_required
from backend.app.services.report_service import ReportService
import csv
from io import StringIO
from datetime import datetime, timedelta
import math

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
@admin_required
def dashboard():
    status = request.args.get('status')
    categoria = request.args.get('categoria')
    de = request.args.get('de')
    ate = request.args.get('ate')

    q = Report.query
    if status:
        q = q.filter(Report.status == status)
    if categoria:
        q = q.filter(Report.category == categoria)
    def parse_date(s):
        try:
            return datetime.strptime(s, '%Y-%m-%d')
        except Exception:
            return None
    d0 = parse_date(de)
    d1 = parse_date(ate)
    if d0:
        q = q.filter(Report.created_at >= d0)
    if d1:
        q = q.filter(Report.created_at < d1.replace(hour=23, minute=59, second=59))

    q = q.order_by(Report.created_at.desc())

    try:
        page = max(1, int(request.args.get('page', '1')))
    except Exception:
        page = 1
    per_page = 12
    total = q.count()
    reports = q.limit(per_page).offset((page-1)*per_page).all()
    pages = math.ceil(total / per_page) if per_page else 1

    total_all = Report.query.count()
    by_status = dict(db.session.query(Report.status, func.count(Report.id)).group_by(Report.status).all())
    by_category = dict(db.session.query(Report.category, func.count(Report.id)).group_by(Report.category).all())

    today = datetime.utcnow().date()
    days = [(today - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
    counts = {d: 0 for d in days}
    rows = db.session.query(func.date(Report.created_at), func.count(Report.id)).group_by(func.date(Report.created_at)).all()
    for d, c in rows:
        ds = d if isinstance(d, str) else d.isoformat()
        if ds in counts:
            counts[ds] = c
    series7 = [counts[d] for d in days]

    stats = {'total': total_all, 'by_status': by_status, 'by_category': by_category, 'days': days, 'series7': series7}

    return render_template('admin/dashboard.html', reports=reports, stats=stats, page=page, pages=pages, total=total)

@admin_bp.route('/admin/denuncia/<int:report_id>', methods=['GET','POST'])
@login_required
@admin_required
def report_manage(report_id: int):
    from backend.app.forms import StatusForm
    r = Report.query.get_or_404(report_id)
    form = StatusForm()
    if form.validate_on_submit():
        r.status = form.status.data
        db.session.commit()
        ReportService().notify_status_change(r)
        flash('Status atualizado!', 'success')
        return redirect(url_for('admin.report_manage', report_id=report_id))
    form.status.data = r.status
    return render_template('admin/report_detail.html', r=r, sform=form)

@admin_bp.route('/admin/denuncia/<int:report_id>/remover', methods=['POST'])
@login_required
@admin_required
def report_delete(report_id: int):
    r = Report.query.get_or_404(report_id)
    db.session.delete(r)
    db.session.commit()
    flash('Denúncia removida.', 'info')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/export.csv')
@login_required
@admin_required
def export_csv():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['id','titulo','categoria','status','criado_em','endereco','latitude','longitude'])
    for r in Report.query.order_by(Report.created_at.desc()).all():
        writer.writerow([r.id, r.title, r.category, r.status, r.created_at.isoformat(sep=' '), r.address or '', r.latitude or '', r.longitude or ''])
    csv_data = output.getvalue()
    return Response(csv_data, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=denuncias.csv'})

from backend.app.forms import CompanyForm


@admin_bp.route('/admin/terceirizadas')
@login_required
@admin_required
def companies_list():
    page = int(request.args.get('page', 1))
    per_page = 10
    pagination = Company.query.order_by(Company.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admin/companies_list.html', pagination=pagination, companies=pagination.items)

@admin_bp.route('/admin/terceirizadas/nova', methods=['GET','POST'])
@login_required
@admin_required
def companies_new():
    form = CompanyForm()
    if form.validate_on_submit():
        # checagens de unicidade
        if Company.query.filter_by(cnpj=form.cnpj.data).first():
            flash('Já existe uma empresa com este CNPJ.', 'warning')
        else:
            # checar email já em uso
            email = form.email.data.strip().lower()
            if User.query.filter_by(email=email).first():
                flash('E-mail já está em uso.', 'warning')
            else:
                # cria usuário para login
                u = User(name=form.name.data, email=email, is_admin=False)
                u.set_password(form.password.data)
                db.session.add(u)
                db.session.flush()  # garante u.id
                # cria empresa vinculada ao usuário
                c = Company(name=form.name.data, cnpj=form.cnpj.data, phone=form.phone.data or None, email=email, address=form.address.data or None, user_id=u.id)
                db.session.add(c)
                db.session.commit()
                flash('Empresa cadastrada e conta criada com sucesso.', 'success')
            return redirect(url_for('admin.companies_list'))
    return render_template('admin/companies_new.html', form=form)

@admin_bp.route('/admin/terceirizadas/<int:company_id>/excluir', methods=['POST'])
@login_required
@admin_required
def companies_delete(company_id):
    c = Company.query.get_or_404(company_id)
    db.session.delete(c)
    db.session.commit()
    flash('Empresa excluída.', 'info')
    return redirect(url_for('admin.companies_list'))

