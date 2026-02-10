import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tqdm import tqdm
from colorama import init, Fore, Style

init(autoreset=True)

print(f"{Fore.CYAN}{'='*60}")
print(f"{Fore.CYAN}WEMA BANK AI ASSISTANT - KNOWLEDGE BASE BUILDER")
print(f"{Fore.CYAN}{'='*60}\n")

# Initialize
docs = []
data_dir = Path("data")

# Text splitter with semantic-aware separators for policy/legal docs
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120,
    separators=[
        "\n\nSECTION",
        "\n\nSection",
        "\n\nCHAPTER",
        "\n\n",
        "\n",
        ". "
    ],
    length_function=len,
)

# Load all documents
print(f"{Fore.YELLOW}📁 Loading documents...\n")

# Policies (PDFs)
policy_files = list(data_dir.glob("policies/*.pdf"))
print(f"{Fore.GREEN}Loading {len(policy_files)} policy documents...")
for pdf_file in tqdm(policy_files, desc="Policies"):
    try:
        loader = PyPDFLoader(str(pdf_file))
        loaded = loader.load()
        for d in loaded:
            d.metadata["type"] = "policy"
        docs.extend(loaded)
    except Exception as e:
        print(f"{Fore.RED}Error loading {pdf_file.name}: {e}")

# NOTE: Do not embed customer master data (PII) or transactional tables.
print(f"\n{Fore.YELLOW}Skipping customer_data/ and transactions/ for embeddings (structured data handled via SQL/API).")

# (Removed transactional CSV ingestion) — keep transactional data in SQL/data warehouse.

# Regulations (TXT)
regulation_files = list(data_dir.glob("regulations/*.txt"))
print(f"\n{Fore.GREEN}Loading {len(regulation_files)} regulation documents...")
for txt_file in tqdm(regulation_files, desc="Regulations"):
    try:
        loader = TextLoader(str(txt_file))
        loaded = loader.load()
        for d in loaded:
            d.metadata["type"] = "regulation"
        docs.extend(loaded)
    except Exception as e:
        print(f"{Fore.RED}Error loading {txt_file.name}: {e}")

# Internal memos (TXT)
memo_files = list(data_dir.glob("internal_memos/*.txt"))
print(f"\n{Fore.GREEN}Loading {len(memo_files)} internal memos...")
for txt_file in tqdm(memo_files, desc="Memos"):
    try:
        loader = TextLoader(str(txt_file))
        loaded = loader.load()
        for d in loaded:
            d.metadata["type"] = "memo"
        docs.extend(loaded)
    except Exception as e:
        print(f"{Fore.RED}Error loading {txt_file.name}: {e}")

print(f"\n{Fore.CYAN}{'='*60}\n")

# Split documents
print(f"{Fore.YELLOW}✂️  Splitting documents into chunks...")
split_docs = text_splitter.split_documents(docs)
print(f"{Fore.GREEN}✓ Created {len(split_docs)} text chunks\n")

# Create embeddings
print(f"{Fore.YELLOW}🧠 Creating embeddings (this may take a few minutes)...")
# Note: Ensure Ollama is running and 'nomic-embed-text' model is pulled
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Create vector database with explicit collection and persist
print(f"{Fore.YELLOW}💾 Building vector database...")
db = Chroma.from_documents(
    documents=split_docs,
    embedding=embeddings,
    persist_directory="bank_db",
    collection_name="wema_knowledge"
)
db.persist()

print(f"\n{Fore.CYAN}{'='*60}")
print(f"{Fore.GREEN}✓ KNOWLEDGE BASE CREATED SUCCESSFULLY!")
print(f"{Fore.CYAN}{'='*60}")
print(f"\n{Fore.YELLOW}📊 Statistics:")
print(f"   - Documents processed: {len(docs)}")
print(f"   - Text chunks: {len(split_docs)}")
print(f"   - Database location: ./bank_db")
print(f"\n{Fore.GREEN}Ready to answer questions! Run: python ask.py\n")
