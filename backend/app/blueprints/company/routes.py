from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from backend.app.extensions import db
from backend.app.models import Report, Comment
from sqlalchemy import String, Text
from sqlalchemy import inspect as sqla_inspect

company_bp = Blueprint('company', __name__, url_prefix='/empresa')

def _comment_text_field_name():
    """Detecta o nome do campo de texto do modelo Comment."""
    try:
        mapper = sqla_inspect(Comment)
        cols = {c.key: c for c in mapper.columns}
        for name in ['content','text','message','body','descricao','comentario','comment','reply','resposta']:
            if name in cols:
                return name
        skip = {'id','report_id','user_id','company_id','created_at','updated_at','status','author'}
        for name, col in cols.items():
            if name in skip: 
                continue
            if isinstance(col.type, (String, Text)):
                return name
    except Exception:
        pass
    return 'content'

def _comment_author_field_name():
    """Tenta descobrir o campo de autor. Padrão: 'author'."""
    try:
        mapper = sqla_inspect(Comment)
        cols = {c.key: c for c in mapper.columns}
        for name in ['author','author_name','nome_autor','from','by']:
            if name in cols:
                return name
    except Exception:
        pass
    return 'author'

@company_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    if not getattr(current_user, 'company', None):
        flash('Usuário não possui empresa vinculada.', 'warning')
        return render_template('company/dashboard.html', reports=[], total=0, by_status={}, by_category={})

    q = (Report.query
         .filter(Report.assigned_company_id == current_user.company.id)
         .order_by(Report.created_at.desc()))

    reports = q.limit(50).all()
    total = q.count()

    by_status_rows = (db.session.query(Report.status, db.func.count(Report.id))
                      .filter(Report.assigned_company_id == current_user.company.id)
                      .group_by(Report.status).all())
    by_category_rows = (db.session.query(Report.category, db.func.count(Report.id))
                        .filter(Report.assigned_company_id == current_user.company.id)
                        .group_by(Report.category).all())

    by_status = {k or '—': v for k, v in by_status_rows}
    by_category = {k or '—': v for k, v in by_category_rows}

    return render_template('company/dashboard.html',
                           reports=reports, total=total,
                           by_status=by_status, by_category=by_category)

@company_bp.route('/reports/<int:report_id>', methods=['GET', 'POST'])
@login_required
def report_detail(report_id):
    r = (Report.query
         .filter(Report.assigned_company_id == current_user.company.id,
                 Report.id == report_id)
         .first_or_404())

    if request.method == 'POST':
        text_field = _comment_text_field_name()
        author_field = _comment_author_field_name()

        content_val = (request.form.get('content') or '').strip()
        status_val  = (request.form.get('status') or '').strip()

        changed = False
        if content_val:
            c = Comment()

            # vincula à denúncia
            if hasattr(c, 'report_id'):
                setattr(c, 'report_id', r.id)
            else:
                try:
                    setattr(c, 'report', r)
                except Exception:
                    pass

            # define texto
            try:
                setattr(c, text_field, content_val)
            except Exception:
                for alt in ['content','text','message','body','descricao','comentario','comment','reply','resposta']:
                    if hasattr(c, alt):
                        setattr(c, alt, content_val)
                        break

            # define autor obrigatório (NOT NULL) se houver esse campo
            author_val = None
            try:
                company = getattr(current_user, 'company', None)
                author_val = (getattr(company, 'name', None)
                              or getattr(current_user, 'name', None)
                              or getattr(current_user, 'username', None)
                              or getattr(current_user, 'email', None)
                              or 'Empresa')
            except Exception:
                author_val = 'Empresa'

            if hasattr(c, author_field):
                setattr(c, author_field, author_val)

            # define user/company ids se existirem
            if hasattr(c, 'user_id'):
                try:
                    c.user_id = getattr(current_user, 'id', None)
                except Exception:
                    pass
            if hasattr(c, 'company_id') and getattr(current_user, 'company', None):
                try:
                    c.company_id = current_user.company.id
                except Exception:
                    pass

            db.session.add(c)
            changed = True

        if status_val:
            r.status = status_val
            changed = True

        if changed:
            db.session.commit()
            flash('Resposta registrada.', 'success')
        else:
            flash('Nada para salvar.', 'warning')

        return redirect(url_for('company.report_detail', report_id=r.id))

    if hasattr(Comment, 'created_at'):
        comments = (Comment.query
                    .filter_by(report_id=r.id)
                    .order_by(Comment.created_at.asc())
                    .all())
    else:
        comments = (Comment.query
                    .filter_by(report_id=r.id)
                    .order_by(Comment.id.asc())
                    .all())

    return render_template('company/report_detail.html', report=r, comments=comments)