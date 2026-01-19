# 📅 Gerador de Calendário

Aplicação web desenvolvida em FastAPI para geração de calendários anuais em PDF com feriados nacionais e estaduais brasileiros. Permite personalizar o início da semana, orientação do calendário (vertical ou horizontal), exibir fases da lua e incluir contagens de semanas e dias do ano.

**🌐 Aplicação em produção:** [https://gerador-calendario.onrender.com](https://gerador-calendario.onrender.com)

## ✨ Funcionalidades

- Geração de calendários anuais em PDF
- Feriados nacionais brasileiros calculados automaticamente
- Feriados estaduais por UF
- Fases da lua (opcional)
- Contagem de semanas e dias do ano (opcional)
- Personalização do início da semana (domingo ou segunda-feira)
- Orientação vertical ou horizontal do PDF
- Middlewares de segurança (headers de segurança, rate limiting)
- Suporte a CORS configurável

## 🛠️ Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **Uvicorn** - Servidor ASGI
- **WeasyPrint** - Geração de PDF a partir de HTML/CSS
- **Jinja2** - Template engine
- **PyEphem** - Cálculo das fases da lua
- **Python-dotenv** - Gerenciamento de variáveis de ambiente

## 📋 Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd Gerador-Calendario
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.env` na raiz do projeto:
```bash
cp .env.example .env
```

Edite o `.env` e configure as variáveis de ambiente (veja seção abaixo).

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

- **ENVIRONMENT**: Ambiente de execução (`development` ou `production`)
- **ALLOWED_ORIGINS**: Origens permitidas para CORS (separadas por vírgula)

## ▶️ Como Executar

### Desenvolvimento

Execute o servidor com auto-reload:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A aplicação estará disponível em:
- Interface web: `http://localhost:8000`

### Produção

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## 📡 Rotas/Endpoints

### GET `/`
Página principal com formulário para gerar calendário.

**Parâmetros de query:**
- `ano` (int, opcional): Ano do calendário (padrão: ano atual)
- `inicio_semana` (str, opcional): `domingo` ou `segunda` (padrão: `domingo`)
- `uf` (str, opcional): Sigla do estado para incluir feriados estaduais
- `mostrar_fases_lua` (bool, opcional): Exibir fases da lua
- `mostrar_contagem_semanas` (bool, opcional): Exibir contagem de semanas
- `mostrar_contagem_dias_ano` (bool, opcional): Exibir contagem de dias do ano
- `orientacao` (str, opcional): `vertical` ou `horizontal` (padrão: `vertical`)

### GET `/calendario/pdf`
Gera o calendário em PDF.

**Parâmetros de query:**
- `ano` (int, obrigatório): Ano do calendário
- `inicio_semana` (str, opcional): `domingo` ou `segunda` (padrão: `domingo`)
- `uf` (str, opcional): Sigla do estado
- `mostrar_fases_lua` (str, opcional): `1` para ativar
- `mostrar_contagem_semanas` (str, opcional): `1` para ativar
- `mostrar_contagem_dias_ano` (str, opcional): `1` para ativar
- `orientacao` (str, opcional): `vertical` ou `horizontal` (padrão: `vertical`)

**Exemplo:**
```
GET /calendario/pdf?ano=2024&uf=SP&mostrar_fases_lua=1&orientacao=horizontal
```

### GET `/sobre`
Página sobre o projeto.

## 🚢 Deploy

O projeto está configurado para deploy no Render através do arquivo `render.yaml`.

## 📁 Estrutura do Projeto

```
Gerador-Calendario/
├── app/
│   ├── core/           # Enums e validações
│   ├── data/           # Dados estáticos (feriados estaduais e nacionais)
│   ├── middleware/     # Middlewares de segurança
│   ├── routes/         # Rotas da aplicação
│   ├── services/       # Lógica de negócio
│   ├── static/         # Arquivos estáticos (CSS, imagens)
│   ├── templates/      # Templates Jinja2
│   └── main.py         # Aplicação FastAPI
├── .env                # Variáveis de ambiente (não commitado)
├── .gitignore
├── README.md
├── requirements.txt    # Dependências Python
└── render.yaml         # Configuração de deploy no Render
```

## 🔒 Segurança

A aplicação inclui:

- **Security Headers**: Headers de segurança configurados (CSP, X-Frame-Options, etc.)
- **Rate Limiting**: Limite de 30 requisições por minuto por IP
- **CORS**: Configurável via variáveis de ambiente
- **Validação de Entrada**: Validação rigorosa de parâmetros de entrada
- **Tratamento de Erros**: Tratamento seguro de erros sem expor detalhes sensíveis em produção

