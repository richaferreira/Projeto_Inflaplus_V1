
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email(message='E-mail inválido')])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=3, message='Senha muito curta')])
    submit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    name = StringField('Nome completo', validators=[DataRequired(), Length(max=100)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('password', message='Senhas não conferem')])
    submit = SubmitField('Criar conta')

class ReportForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Descrição', validators=[DataRequired(), Length(max=2000)])
    category = SelectField('Categoria', choices=[
        ('Vazamento', 'Vazamento'),
        ('Falta de água', 'Falta de água'),
        ('Água suja', 'Água suja'),
        ('Outros', 'Outros')
    ], validators=[DataRequired()])
    address = StringField('Endereço (opcional)', validators=[Optional(), Length(max=200)])
    latitude = FloatField('Latitude (opcional)', validators=[Optional()])
    longitude = FloatField('Longitude (opcional)', validators=[Optional()])
    image = FileField('Foto principal (opcional)', validators=[FileAllowed(['jpg','jpeg','png','gif'], 'Formatos permitidos: JPG, PNG, GIF')])
    assigned_company_id = SelectField('Empresa responsável na região', coerce=int, choices=[(0, '— Selecionar —')])
    submit = SubmitField('Enviar denúncia')

class StatusForm(FlaskForm):
    status = SelectField('Status', choices=[('Aberta','Aberta'), ('Em andamento','Em andamento'), ('Resolvida','Resolvida')], validators=[DataRequired()])
    submit = SubmitField('Atualizar status')

class CommentForm(FlaskForm):
    text = TextAreaField('Comentário', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Adicionar comentário')


class CompanyForm(FlaskForm):
    name = StringField('Nome da empresa', validators=[DataRequired(), Length(max=120)])
    cnpj = StringField('CNPJ', validators=[DataRequired(), Length(max=18)])
    phone = StringField('Telefone', validators=[Optional(), Length(max=20)])
    email = StringField('E-mail', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Senha de acesso', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('password', message='Senhas não conferem')])
    address = StringField('Endereço', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Salvar')
