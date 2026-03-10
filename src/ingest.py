import os 
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector
load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")

if not PDF_PATH:
    raise ValueError("Missing environment variable: PDF_PATH")


for k in ("OPENAI_MODEL", "GOOGLE_MODEL", "PGVECTOR_URL", "PGVECTOR_COLLECTION"):
    if not os.getenv(k):
        raise ValueError(f"Missing environment variable: {k}")

docs = PyPDFLoader(str(PDF_PATH)).load()

splits = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=150,
    add_start_index=False).split_documents(docs)

if not splits:
    raise SystemExit("No documents to process")

enriched = [
    Document(
        page_content=d.page_content, 
        metadata={k: v for k, v in d.metadata.items() if v not in ("", None)},
    ) for d in splits
]   

ids = [f"doc-{i}" for i in range(len(enriched))]

# Create embeddings with OpenAI
embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL", "text-embedding-3-small"))

# Create embeddings with Google Gemini
#embeddings = OpenAIEmbeddings(model=os.getenv("GOOGLE_MODEL", "models/embedding-001"))

store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PGVECTOR_COLLECTION"),
    connection=os.getenv("PGVECTOR_URL"),
    use_jsonb=True
)

store.add_documents(documents=enriched, ids=ids)