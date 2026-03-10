# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema de RAG (Retrieval-Augmented Generation) desenvolvido com LangChain para ingestão, busca e chat sobre documentos PDF utilizando banco de dados vetorial PostgreSQL com extensão pgVector.

## 📋 Sobre o Projeto

Este projeto implementa um sistema completo de processamento e consulta de documentos PDF, permitindo:

- **Ingestão**: Carregar arquivos PDF, processar o conteúdo e armazenar em um banco de dados vetorial (PostgreSQL com pgVector)
- **Busca**: Realizar buscas semânticas no conteúdo do documento armazenado
- **Chat**: Interagir via linha de comando (CLI) fazendo perguntas e recebendo respostas baseadas exclusivamente no conteúdo do PDF

## 🛠️ Tecnologias e Frameworks

- **Python 3.13** - Linguagem de programação
- **LangChain** - Framework para desenvolvimento de aplicações com LLMs
- **PostgreSQL** - Banco de dados relacional
- **pgVector** - Extensão do PostgreSQL para armazenamento e busca de vetores
- **OpenAI API** - Modelos de embeddings e chat
- **Google Gemini** - Alternativa para embeddings
- **pypdf** - Biblioteca para leitura de arquivos PDF
- **python-dotenv** - Gerenciamento de variáveis de ambiente

## 🔄 Fluxo do Sistema

```mermaid
flowchart TD
    A[📄 Arquivo PDF] --> B[Ingestão - ingest.py]
    B --> C[Carregamento com PyPDFLoader]
    C --> D[Divisão em Chunks]
    D --> E[Geração de Embeddings]
    E --> F[(PostgreSQL + pgVector)]
    
    G[👤 Usuário] --> H[Query via CLI]
    H --> I[Busca - search.py]
    I --> F
    F --> J[Recuperação de Documentos Relevantes]
    J --> K[Chat - chat.py]
    K --> L[LLM processa contexto + query]
    L --> M[📝 Resposta ao Usuário]
    M --> G
    
    style A fill:#e1f5ff
    style F fill:#ffe1e1
    style G fill:#e1ffe1
    style M fill:#ffe1ff
```

## 📁 Estrutura do Projeto

```
mba-ia-desafio-ingestao-busca/
├── src/
│   ├── ingest.py    # Script de ingestão do PDF
│   ├── search.py    # Busca semântica no banco vetorial
│   └── chat.py      # Interface de chat CLI
├── .env             # Variáveis de ambiente (não versionado)
├── .env.example     # Exemplo de configuração
├── requirements.txt # Dependências Python
├── docker-compose.yml # Configuração do PostgreSQL
└── README.md        # Documentação
```

## 🚀 Como Executar

### 1. Pré-requisitos

- Python 3.13+
- Docker e Docker Compose
- Chaves de API (OpenAI e/ou Google Gemini)

### 2. Configuração do Ambiente

Clone o repositório e navegue até o diretório:

```bash
cd mba-ia-desafio-ingestao-busca
```

Crie e ative o ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### 3. Configuração das Variáveis de Ambiente

Copie o arquivo de exemplo e configure suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas chaves de API:

```env
# OpenAI API Key
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=text-embedding-3-small

# Google Gemini API Key
GOOGLE_API_KEY=sua_chave_aqui
GOOGLE_MODEL=models/embedding-001

# PGVector Configuration
PGVECTOR_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PGVECTOR_COLLECTION=gpt5_collection

# PDF Path
PDF_PATH=./document.pdf
```

### 4. Iniciar o Banco de Dados

Suba o container do PostgreSQL com pgVector:

```bash
docker-compose up -d
```

### 5. Executar a Ingestão

Coloque seu arquivo PDF no diretório raiz do projeto com o nome `document.pdf` (ou ajuste o caminho no `.env`).

Execute o script de ingestão:

```bash
python src/ingest.py
```

Este comando irá:
- Carregar o PDF
- Dividir em chunks de 500 caracteres
- Gerar embeddings
- Armazenar no PostgreSQL com pgVector

### 6. Utilizar o Chat

Execute o script de chat para interagir via CLI:

```bash
python src/chat.py
```

O chat **automaticamente busca** o contexto relevante no banco vetorial e gera respostas baseadas no conteúdo do PDF.

> **Nota**: O arquivo `search.py` contém a lógica de busca vetorial que é chamada internamente pelo chat. Você pode executá-lo standalone (`python src/search.py`) apenas para fins de teste e debug, mas não é necessário no fluxo normal.

## 📝 Funcionalidades Detalhadas

### Ingestão (`ingest.py`)
- Carrega arquivos PDF usando `PyPDFLoader`
- Divide o documento em chunks menores usando `RecursiveCharacterTextSplitter`
- Gera embeddings vetoriais do conteúdo
- Armazena os vetores no PostgreSQL com pgVector para busca eficiente

### Busca (`search.py`)
- Módulo responsável pela busca semântica no banco de dados vetorial
- Retorna os documentos mais relevantes baseados em similaridade vetorial
- Utiliza embeddings para encontrar contexto relacionado à query
- Pode ser executado standalone para testes (opcional)

### Chat (`chat.py`)
- Interface CLI principal para interação com o usuário
- Processa queries em linguagem natural
- **Integra automaticamente a busca** no banco vetorial via `search.py`
- Recupera contexto relevante e envia para o LLM
- Gera respostas baseadas exclusivamente no contexto recuperado
- Respostas limitadas ao conteúdo do PDF processado
- Segue regras rígidas para evitar alucinações

## 🧪 Exemplo de Uso

```bash
# 1. Subir o banco de dados
docker-compose up -d

# 2. Ingerir o PDF
python src/ingest.py

# 3. Iniciar o chat (busca é automática)
python src/chat.py
> Qual é o tema principal do documento?
[O chat busca automaticamente no banco vetorial e responde]

> Quais são os principais tópicos abordados?
[Busca e responde baseado no PDF]
```

### Teste de Busca Standalone (Opcional)

Para testar apenas a funcionalidade de busca vetorial:

```bash
python src/search.py
```

## 🔒 Segurança

- Nunca versione o arquivo `.env` com suas credenciais
- Use o `.env.example` como referência
- Mantenha suas chaves de API seguras
- O `.gitignore` já está configurado para proteger informações sensíveis

## 📄 Licença

Projeto desenvolvido como parte do MBA em Engenharia de Software com IA - Full Cycle.