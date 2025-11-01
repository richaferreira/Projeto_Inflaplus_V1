
# InfraPlus — Águas Seguras (MVP)

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
# Crie o ambiente virtual
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# Linux/macOS
# source .venv/bin/activate

# Instale as dependências
python -m pip install --upgrade pip
pip install -r requirements.txt

# Crie o .env com as variáveis de ambiente
cp .env.example .env

# Suba a aplicação
python run.py
```

Acesse a aplicação em `http://127.0.0.1:5000/`.  
**Admin seed**:  
- E-mail: `admin@infra.plus`  
- Senha: `123`

## Variáveis de ambiente

Crie o arquivo `.env` baseado no arquivo `.env.example` e configure as variáveis:

```ini
# Flask/InfraPlus environment
FLASK_ENV=development
SECRET_KEY=troque-por-um-valor-bem-aleatorio-e-seguro
DATABASE_URL=sqlite:///infra_plus.db  # ou Postgres, etc.
MAIL_SERVER=smtp.seuprovedor.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=seu_usuario
MAIL_PASSWORD=sua_senha
MAIL_DEFAULT_SENDER=infra.plus@seuprojeto.com
```

### Observações
- **Uploads**: Armazenados em `frontend/static/uploads/`
- **Validação de e-mail**: O pacote `email-validator` é utilizado para validação de e-mails.
- **Notificação por e-mail**: Caso configure o e-mail no `.env`, o autor recebe uma notificação quando o status da denúncia for alterado.

## Roadmap sugerido

- **Alembic (migrações)**: Substituir script manual por **Alembic** para gerenciar o banco de dados de forma mais eficiente.
- **Testes**: Adicionar **pytest + coverage**, configurar CI para executar os testes automaticamente.
- **CI/CD**: GitHub Actions para lint, testes e deploy automatizado.
- **Geocodificação real**: Implementar geocodificação real para o campo de localização de denúncias (Nominatim, com limitação de taxa).

## Estrutura de arquivos do projeto

### Backend
- **Arquivos principais**:  
  - `run.py`: Ponto de entrada.
  - `config.py`: Configurações gerais do Flask e do banco de dados.
  - `extensions.py`: Extensões como DB, Mail.
  - `models/`: Modelos de dados (`User`, `Report`, `Company`, etc.).
  - `forms/`: Formulários para criação de usuários, relatórios, login, etc.
  - `services/`: Lógica de serviços (criação de relatórios, envio de e-mails).
  - `blueprints/`: Diferentes rotas/funcionalidades divididas em Blueprints (ex.: `auth`, `admin`, `public`).
  - `utils.py`: Funções utilitárias como upload de arquivos.

- **Migração de banco de dados**:  
  Para SQLite, você pode rodar o script `migrate_assigned_company_id.py` para adicionar a coluna de `assigned_company_id` na tabela `report`.

### Frontend
- **Templates Jinja**:  
  - `templates/`: Contém todos os templates HTML para as páginas públicas, de administração e de empresas.
  - **Arquivos estáticos**:  
    - `css/`: Arquivos de estilo (`styles.css`).
    - `js/`: Scripts JavaScript (ex.: `map_home.js`, `report_modal.js`).
    - `uploads/`: Armazenamento de uploads em tempo de execução.

### Arquivos de configuração
- **`.env.example`**: Exemplo de configuração para ambiente.
- **`requirements.txt`**: Dependências do projeto.
    