import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm
from colorama import init, Fore, Style

init(autoreset=True)

print(f"{Fore.CYAN}{'='*60}")
print(f"{Fore.CYAN}WEMA BANK AI ASSISTANT - KNOWLEDGE BASE BUILDER")
print(f"{Fore.CYAN}{'='*60}\n")

# Initialize
docs = []
data_dir = Path("data")

# Text splitter for better chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
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
        docs.extend(loader.load())
    except Exception as e:
        print(f"{Fore.RED}Error loading {pdf_file.name}: {e}")

# Customer data (TXT)
customer_files = list(data_dir.glob("customer_data/*.txt"))
print(f"\n{Fore.GREEN}Loading {len(customer_files)} customer data files...")
for txt_file in tqdm(customer_files, desc="Customer Data"):
    try:
        loader = TextLoader(str(txt_file))
        docs.extend(loader.load())
    except Exception as e:
        print(f"{Fore.RED}Error loading {txt_file.name}: {e}")

# Transactions (CSV)
transaction_files = list(data_dir.glob("transactions/*.csv"))
print(f"\n{Fore.GREEN}Loading {len(transaction_files)} transaction files...")
for csv_file in tqdm(transaction_files, desc="Transactions"):
    try:
        loader = CSVLoader(str(csv_file))
        docs.extend(loader.load())
    except Exception as e:
        print(f"{Fore.RED}Error loading {csv_file.name}: {e}")

# Regulations (TXT)
regulation_files = list(data_dir.glob("regulations/*.txt"))
print(f"\n{Fore.GREEN}Loading {len(regulation_files)} regulation documents...")
for txt_file in tqdm(regulation_files, desc="Regulations"):
    try:
        loader = TextLoader(str(txt_file))
        docs.extend(loader.load())
    except Exception as e:
        print(f"{Fore.RED}Error loading {txt_file.name}: {e}")

# Internal memos (TXT)
memo_files = list(data_dir.glob("internal_memos/*.txt"))
print(f"\n{Fore.GREEN}Loading {len(memo_files)} internal memos...")
for txt_file in tqdm(memo_files, desc="Memos"):
    try:
        loader = TextLoader(str(txt_file))
        docs.extend(loader.load())
    except Exception as e:
        print(f"{Fore.RED}Error loading {txt_file.name}: {e}")

print(f"\n{Fore.CYAN}{'='*60}\n")

# Split documents
print(f"{Fore.YELLOW}✂️  Splitting documents into chunks...")
split_docs = text_splitter.split_documents(docs)
print(f"{Fore.GREEN}✓ Created {len(split_docs)} text chunks\n")

# Create embeddings
print(f"{Fore.YELLOW}🧠 Creating embeddings (this may take a few minutes)...")
# Note: Ensure Ollama is running and mistral model is pulled
embeddings = OllamaEmbeddings(model="mistral")

# Create vector database
print(f"{Fore.YELLOW}💾 Building vector database...")
db = Chroma.from_documents(
    split_docs,
    embeddings,
    persist_directory="bank_db"
)

print(f"\n{Fore.CYAN}{'='*60}")
print(f"{Fore.GREEN}✓ KNOWLEDGE BASE CREATED SUCCESSFULLY!")
print(f"{Fore.CYAN}{'='*60}")
print(f"\n{Fore.YELLOW}📊 Statistics:")
print(f"   - Documents processed: {len(docs)}")
print(f"   - Text chunks: {len(split_docs)}")
print(f"   - Database location: ./bank_db")
print(f"\n{Fore.GREEN}Ready to answer questions! Run: python ask.py\n")
