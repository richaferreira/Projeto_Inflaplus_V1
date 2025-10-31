
# InfraPlus — Águas Seguras (MVP v3 • monorepo organizado)

Organizado por **camadas e pastas**: `backend/` (Flask, modelos, serviços, rotas) e `frontend/` (templates, css, js e uploads). Comentários usam **automaticamente** o nome do usuário logado; há **busca**, **filtros/paginação**, **uploads múltiplos**, **.env** e **e‑mail opcional** no update de status.

## Estrutura
```
InfraPlus_AguasSeguras/
├─ run.py                    # ponto de entrada
├─ requirements.txt
├─ .env.example             # copie para .env
├─ backend/
│  └─ app/
│     ├─ __init__.py        # cria app com templates/static apontando para frontend/
│     ├─ config.py          # paths & configs
│     ├─ extensions.py      # db, mail
│     ├─ models/            # User, Report, Comment, ReportImage
│     ├─ forms/             # Login, Register, Report, Status, Comment (sem author)
│     ├─ services/          # ReportService (create + notify)
│     ├─ repositories/      # filtros, paginação, contagens
│     ├─ blueprints/        # public, auth, admin
│     └─ utils.py           # uploads, admin_required
└─ frontend/
   ├─ templates/            # Jinja (base, shared, public, auth, admin, errors)
   └─ static/
      ├─ css/styles.css
      ├─ js/*.js
      └─ uploads/           # gerada em runtime
```

## Como rodar
```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# Linux/macOS
# source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

# crie .env a partir de .env.example (opcional para e-mail)
python run.py
```
Acesse `http://127.0.0.1:5000/` — Admin seed: `admin@infra.plus` / `123`.

## Observações
- Uploads: `frontend/static/uploads/`
- Validação de e‑mail depende do pacote `email-validator` (já no requirements).
- Se configurar e‑mail no `.env`, ao mudar o status no admin o autor recebe notificação.
```
MAIL_SERVER=smtp.seuprovedor.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=seu_usuario
MAIL_PASSWORD=sua_senha
MAIL_DEFAULT_SENDER=infra.plus@seuprojeto.com
```

## Roadmap sugerido
- Alembic (migrações), pytest + coverage, CI (GitHub Actions), geocodificação real (Nominatim) com limite de taxa.
```
