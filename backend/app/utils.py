
import os
import uuid
from functools import wraps
from flask import current_app, abort
from flask_login import current_user
from werkzeug.utils import secure_filename


def allowed_file(filename: str) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    return ext in current_app.config['ALLOWED_EXTENSIONS']


def save_uploaded_image(file_storage) -> str:
    if not file_storage or file_storage.filename == '':
        return None
    ext = os.path.splitext(file_storage.filename)[1].lower()
    if ext not in current_app.config['ALLOWED_EXTENSIONS']:
        return None
    name = secure_filename(os.path.splitext(file_storage.filename)[0]) or 'imagem'
    unique = uuid.uuid4().hex[:10]
    filename = f"{name}-{unique}{ext}"
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_storage.save(path)
    return filename


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
            abort(403)
        return f(*args, **kwargs)
    return wrapper

def company_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # precisa estar logado, não ser admin, e ter empresa vinculada
        if (not current_user.is_authenticated 
            or getattr(current_user, 'is_admin', False) 
            or not getattr(current_user, 'company', None)):
            abort(403)
        return f(*args, **kwargs)
    return wrapper
