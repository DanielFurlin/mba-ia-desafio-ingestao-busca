# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema de RAG (Retrieval-Augmented Generation) que ingere um PDF em um banco de dados vetorial (PostgreSQL + pgvector) e permite fazer perguntas sobre o conteúdo via terminal.

## Pré-requisitos

- Python 3.11 – 3.13.7
- Docker e Docker Compose

## Configuração do ambiente

### 1. Ambiente virtual

Crie e ative o ambiente virtual:

```bash
# Criar
python -m venv venv

# Ativar (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Ativar (Windows CMD)
.\venv\Scripts\activate.bat

# Ativar (Linux/macOS)
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### 2. Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com base no exemplo abaixo:

```env
# Caminho para o PDF a ser ingerido
PDF_PATH=document.pdf

# --- Provedor Google Gemini (escolha um provedor) ---
GOOGLE_API_KEY=sua_chave_aqui
GOOGLE_EMBEDDING_MODEL=models/text-embedding-004
GOOGLE_CHATBOT_MODEL=gemini-2.0-flash

# --- Provedor OpenAI (escolha um provedor) ---
# OPENAI_API_KEY=sua_chave_aqui
# OPENAI_EMBEDDING_MODEL=text-embedding-3-small
# OPENAI_CHATBOT_MODEL=gpt-4o-mini

# Conexão com o banco (valores padrão do docker-compose)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=rag
DB_USER=postgres
DB_PASSWORD=postgres

# Configurações de chunking (opcionais)
CHUNK_SIZE=1000
CHUNK_OVERLAP=150
```

> Preencha apenas um dos provedores (Google **ou** OpenAI). O sistema utiliza o primeiro que estiver configurado.

### 3. Subir o banco de dados

```bash
docker compose up -d
```

Isso irá iniciar o PostgreSQL com a extensão `pgvector` já habilitada. Aguarde alguns segundos até o container ficar saudável antes de prosseguir.

Para verificar se está rodando:

```bash
docker compose ps
```

## Execução

Os scripts devem ser executados a partir do diretório `src/`:

```bash
cd src
```

### Ingestão do PDF

Processa o PDF definido em `PDF_PATH`, divide em chunks e armazena os embeddings no banco vetorial:

```bash
python ingest.py
```

Este comando apaga a coleção anterior e reingere do zero a cada execução.

### Chat com o documento

Inicia um loop de perguntas e respostas sobre o conteúdo ingerido:

```bash
python chat.py
```

Digite sua pergunta e pressione Enter. Para encerrar, digite `sair`, `exit` ou `fim`.

## Estrutura do projeto

```
.
├── docker-compose.yml
├── requirements.txt
├── document.pdf
├── .env
└── src/
    ├── ingest.py       # Carrega e indexa o PDF
    ├── chat.py         # Interface de perguntas e respostas
    ├── search.py       # Prompt RAG
    ├── vector_store.py # Configuração do PGVector
    ├── database.py     # String de conexão
    └── settings.py     # Leitura das variáveis de ambiente
```

## Encerrando os serviços

```bash
docker compose down
```

Para também remover o volume com os dados:

```bash
docker compose down -v
```
