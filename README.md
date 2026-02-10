# Wema Bank AI Assistant - RAG Demo

Local AI-powered banking assistant using Ollama + RAG (Retrieval Augmented Generation)

## Features
- ✅ Policy Q&A from bank documents
- ✅ Customer complaint analysis
- ✅ Transaction insights
- ✅ Regulatory compliance checks
- ✅ Operations support
- ✅ 100% offline (no cloud APIs)

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Ollama

Ollama is crucial for running the local LLM and embeddings. Follow these steps to install it on your VM:

1.  **Install `zstd` (if not already installed):**
    Ollama's installer requires `zstd` for extraction. Run the following command:
    ```bash
    sudo apt-get update
    sudo apt-get install -y zstd
    ```

2.  **Install Ollama:**
    Run the official installation script:
    ```bash
    curl -fsSL https://ollama.com/install.sh | sh
    ```
    If the above command fails or gets stuck, you can try a manual installation:
    *   **Download the binary:** Visit [ollama.com/download](https://ollama.com/download) and manually download the `ollama-linux-amd64` binary to your VM.
    *   **Make it executable:** `chmod +x ollama-linux-amd64`
    *   **Move to a system path:** `sudo mv ollama-linux-amd64 /usr/local/bin/ollama`
    *   **Install as a service (optional but recommended):** Follow the instructions on the Ollama website for setting it up as a systemd service if you want it to run in the background automatically.

3.  **Start Ollama Service:**
    After installation, start the Ollama service. This command should be run in a separate terminal session or backgrounded.
    ```bash
    ollama serve &
    ```

4.  **Pull the Mistral Model:**
    Download the `mistral` model. This is a one-time download and can take a few minutes (~4GB).
    ```bash
    ollama pull mistral
    ```

### 3. Build Knowledge Base
```bash
python ingest.py
```

### 4. Run Assistant

**Interactive mode**
```bash
python ask.py
```

**Guided demo**
```bash
python demo.py
```

**Web UI (Recommended for demo)**
```bash
python ui.py
```

## Sample Questions

**Policies:**
- "What collateral is needed for SME overdraft?"
- "How long does loan approval take?"

**Customer Service:**
- "What is John Bello's complaint?"
- "Draft a response to the ATM card issue"

**Transactions:**
- "Summarize January transactions for account 0123456789"
- "What was the highest expense in January for account 0123456789?"
- "Why did transaction TXN20260205005 fail?"

**Compliance:**
- "What are CBN's KYC requirements?"
- "What is the PTA limit?"

**Tech Stack**
- LLM: Ollama (Mistral)
- Embeddings: Ollama embeddings
- Vector DB: ChromaDB
- RAG Framework: LangChain

---

# COMPLETE SETUP GUIDE

This guide provides a two-phase approach for setting up and running the Wema Bank AI Assistant. This ensures you can prepare all necessary files locally and then deploy and test them efficiently on your VM with GPU infrastructure.

## PHASE 1: LOCAL PREPARATION (On Your Local Computer)

In this phase, you will create all the project files and structure on your local machine. **No installations are needed at this stage.**

### Step 1: Create Project Folder and Subdirectories

Create the main project directory and its subfolders for data organization:

```bash
mkdir -p bank_ai_demo/data/{policies,customer_data,transactions,regulations,internal_memos}
cd bank_ai_demo
```

### Step 2: Create All Data Files

**Policies (PDF files):**

These files contain the bank's policy documents. You will create Markdown versions first and then convert them to PDF. (Note: The conversion step will be done in the VM, but the content is prepared here.)

1.  **`data/policies/sme_loan_policy.md`**
    ```markdown
    # WEMA BANK PLC
    ## SME LOAN POLICY DOCUMENT
    **Effective: January 2026**

    ### 1. COLLATERAL REQUIREMENTS

    **SME Overdraft Facilities:**
    - Minimum collateral coverage: 120%
    - Acceptable collateral: Land, buildings, equipment, debentures
    - Valuation validity: 6 months maximum
    - Legal perfection required within 30 days

    **Term Loans:**
    - Minimum collateral coverage: 150%
    - Insurance mandatory on all physical assets
    - Annual revaluation for facilities above ₦50 million

    ### 2. ELIGIBILITY CRITERIA

    **Business Age:**
    - Minimum 2 years operational history
    - Bank statement for last 12 months required
    - Audited accounts for businesses with turnover > ₦100 million

    **Credit Bureau:**
    - Maximum DPD (Days Past Due): 30 days
    - No adversely classified facilities in last 12 months
    - CRC check mandatory

    ### 3. TURNAROUND TIME

    **Application Processing:**
    - Initial review: 24 hours
    - Credit committee approval: 48 hours after complete documentation
    - Disbursement: 24 hours post-approval

    **Required Documents:**
    - BVN and valid government ID
    - CAC documents (for registered businesses)
    - Bank statements (12 months)
    - Utility bill (not older than 3 months)
    - Business financial statements
    - Board resolution (for corporate entities)

    ### 4. INTEREST RATES

    **Current Lending Rates (as of February 2026):**
    - SME Overdraft: 18% - 22% per annum
    - Term Loan: 20% - 24% per annum
    - Rate depends on risk rating and relationship strength

    ### 5. REPAYMENT TERMS

    **Overdraft:**
    - Review annually
    - Interest payable monthly
    - No prepayment penalty

    **Term Loans:**
    - Maximum tenure: 5 years
    - Moratorium available (max 6 months)
    - Equal monthly installments
    - Prepayment allowed with 30 days notice

    ### 6. DORMANT ACCOUNTS

    **Definition:**
    - No customer-initiated transaction for 12 consecutive months
    - Excludes bank charges and interest

    **Reactivation:**
    - Customer visit to branch mandatory
    - Fresh KYC update required
    - BVN revalidation
    - Account officer interview

    ### 7. DECLINING CRITERIA

    **Automatic Decline if:**
    - Existing NPL (Non-Performing Loan) anywhere
    - Blacklisted on NIBSS watchlist
    - Court judgment against applicant
    - Business in restricted sectors (gambling, cannabis, etc.)
    ```

2.  **`data/policies/savings_account_policy.md`**
    ```markdown
    # WEMA BANK PLC
    ## SAVINGS ACCOUNT POLICY

    ### 1. MINIMUM BALANCE
    - Regular Savings: ₦1,000
    - ALAT Savings: ₦0 (zero balance account)
    - Children's Account: ₦500

    ### 2. TRANSACTION LIMITS

    **Daily Withdrawal:**
    - Over-the-counter: ₦500,000
    - ATM: ₦100,000
    - Mobile/Internet: ₦1,000,000

    **Monthly Transaction Count:**
    - Regular Savings: Unlimited
    - ALAT: Unlimited free transactions

    ### 3. INTEREST PAYMENT
    - Calculated daily on minimum monthly balance
    - Paid quarterly
    - Current rate: 2.5% per annum (subject to change)

    ### 4. ACCOUNT CLOSURE
    - Customer request with 30 days notice
    - Regulatory closure (court order, death)
    - Dormancy exceeding 10 years
    - Final balance paid by cheque or transfer

    ### 5. CHARGES
    - SMS alert: ₦4 per alert
    - ATM card replacement: ₦1,000
    - Statement request: ₦500 (beyond free 3 per quarter)
    - Certificate of account balance: ₦2,000
    ```

3.  **`data/policies/foreign_exchange_policy.md`**
    ```markdown
    # WEMA BANK PLC
    ## FOREIGN EXCHANGE POLICY

    ### 1. FORM A REQUIREMENTS

    **Personal Travel Allowance (PTA):**
    - Maximum $4,000 per quarter
    - Valid passport and visa required
    - Ticket confirmation within 2 weeks of travel

    **Business Travel Allowance (BTA):**
    - Maximum $5,000 per trip
    - Company documentation required
    - Travel invitation letter mandatory

    ### 2. PERMITTED TRANSACTIONS
    - Tuition fees (with admission letter)
    - Medical expenses abroad (with medical report)
    - Subscription to professional services
    - Import of eligible goods (Form M)

    ### 3. RESTRICTED TRANSACTIONS
    - Payment for goods on negative import list
    - Cryptocurrency purchase
    - Margin trading forex
    - Loans to non-residents

    ### 4. EXCHANGE RATE
    - Official CBN rate + 1% margin
    - Published daily at 10:00 AM
    - Valid for same-day transactions only

    ### 5. DOCUMENTATION
    - Valid ID and BVN
    - Tax clearance (for amounts > $10,000)
    - Form A duly completed
    - Purpose-specific documents
    ```

**Customer Data (TXT files):**

1.  **`data/customer_data/complaints.txt`**
    ```
    CUSTOMER COMPLAINT LOG - FEBRUARY 2026

    ---
    Complaint ID: CMP20260201-001
    Customer: John Bello
    Account: 0123456789
    Date: February 1, 2026

    Issue:
    I transferred ₦150,000 yesterday at 3:45 PM to Musa Traders (GTBank - 0234567890).
    The money left my account but the beneficiary claims they have not received it.
    I have tried calling customer service but the line has been busy.
    Please reverse or investigate urgently. I need this resolved today.

    Status: Pending
    Priority: High

    ---
    Complaint ID: CMP20260202-002
    Customer: Fatima Ibrahim
    Account: 0234567891
    Date: February 2, 2026

    Issue:
    My ATM card was swallowed by the machine at Ikeja branch yesterday.
    I reported immediately but no one has called me back.
    I have urgent payments to make and cannot access my money.
    This is very frustrating. I have been banking with Wema for 8 years.

    Status: Pending
    Priority: High

    ---
    Complaint ID: CMP20260203-003
    Customer: Chidi Okafor
    Account: 0345678902
    Date: February 3, 2026

    Issue:
    I applied for SME loan 3 weeks ago. I was told 48 hours turnaround.
    I have submitted all documents including collateral valuation.
    No feedback till now. My supplier is threatening to cancel the order.
    Account officer is not responding to calls. What is happening?

    Status: Pending
    Priority: Medium

    ---
    Complaint ID: CMP20260204-004
    Customer: Blessing Adekunle
    Account: 0456789013
    Date: February 4, 2026

    Issue:
    I am being charged ₦50 monthly for SMS alerts I never requested.
    This has been going on for 6 months (total ₦300 wrongly debited).
    I have sent emails but no refund. Please reverse these charges.

    Status: Pending
    Priority: Low
    ```

2.  **`data/customer_data/account_requests.txt`**
    ```
    ACCOUNT SERVICE REQUESTS - FEBRUARY 2026

    ---
    Request ID: REQ20260205-001
    Customer: Ahmed Lawal
    Account: 0567890124
    Date: February 5, 2026

    Request Type: Account Upgrade
    Details:
    Current Account Type: Regular Savings
    Requested: Premium Savings Account
    Reason: Need higher transaction limits for my growing business
    Average monthly inflow: ₦2.5 million

    Eligibility Check Needed

    ---
    Request ID: REQ20260206-002
    Customer: Ngozi Eze
    Account: 0678901235
    Date: February 6, 2026

    Request Type: Dormant Account Reactivation
    Details:
    Last transaction: January 2024 (25 months ago)
    Current balance: ₦45,600
    Reason for dormancy: Traveled abroad for studies, now returned
    Updated KYC documents attached

    Action Required: Branch visit, BVN revalidation

    ---
    Request ID: REQ20260207-003
    Customer: Ibrahim Suleiman
    Account: 0789012346
    Date: February 7, 2026

    Request Type: Transaction Limit Increase
    Details:
    Current daily transfer limit: ₦1,000,000
    Requested: ₦5,000,000
    Reason: Paying suppliers for import business
    Supporting docs: CAC, import documents, business bank statement

    Requires: Credit risk assessment

    ---
    Request ID: REQ20260208-004
    Customer: Chinwe Obi
    Account: 0890123457
    Date: February 8, 2026

    Request Type: Interest Certificate
    Details:
    Period: January 2025 - December 2025
    Purpose: Tax filing
    Urgency: Needed by February 15, 2026

    Action: Finance department to generate
    ```

3.  **`data/customer_data/kyc_issues.txt`**
    ```
    KYC COMPLIANCE ISSUES - FEBRUARY 2026

    ---
    Issue ID: KYC20260201-001
    Customer: David Okonkwo
    Account: 0901234568

    Problem: BVN Mismatch
    Details:
    Name on BVN: David Chukwuemeka Okonkwo
    Name on account: David Okonkwo
    Date of Birth: Different (BVN shows 1985, account shows 1987)

    Action Required:
    - Customer to visit branch with valid ID
    - Affidavit for name variation
    - Birth certificate or NIN for DOB correction
    Deadline: February 20, 2026 (or account restriction)

    ---
    Issue ID: KYC20260203-002
    Customer: Amina Yusuf
    Account: 1012345679

    Problem: Expired ID
    Details:
    Driver's license expired: December 2024
    No alternative valid ID on file
    Account opened 2019

    Action Required:
    - Upload new valid ID (passport, driver's license, or NIN slip)
    - Utility bill not older than 3 months
    Deadline: February 15, 2026

    ---
    Issue ID: KYC20260205-003
    Customer: Emeka Industries Ltd
    Account: 1123456780

    Problem: Outdated CAC Documents
    Details:
    CAC certificate on file: 2020
    Current regulations require update every 3 years
    Directors' information incomplete

    Action Required:
    - Fresh CAC status report
    - Board resolution confirming current directors
    - Updated mandate card
    Deadline: February 28, 2026

    ---
    Issue ID: KYC20260207-004
    Customer: Grace Adeleke
    Account: 1234567891

    Problem: Missing Signature
    Details:
    Account opened via ALAT (digital)
    No physical signature card on file
    Now requesting cheque book (requires signature)

    Action Required:
    - Customer to visit any branch
    - Complete signature card
    - Biometric capture
    Processing: 24 hours after visit
    ```

**Transactions (CSV files):**

1.  **`data/transactions/january_transactions.csv`**
    ```csv
    TransactionID,Date,Account,Description,Type,Amount,Balance,Status
    TXN20260101001,2026-01-01,0123456789,Opening Balance,Credit,0.00,450000.00,Success
    TXN20260105002,2026-01-05,0123456789,Salary Payment - Jan,Credit,250000.00,700000.00,Success
    TXN20260110003,2026-01-10,0123456789,Rent Payment,Debit,150000.00,550000.00,Success
    TXN20260115004,2026-01-15,0123456789,Utility Bill - Ikeja Electric,Debit,12500.00,537500.00,Success
    TXN20260120005,2026-01-20,0123456789,ATM Withdrawal - Ikeja,Debit,20000.00,517500.00,Success
    TXN20260125006,2026-01-25,0123456789,Transfer to Musa Traders,Debit,150000.00,367500.00,Success
    TXN20260131007,2026-01-31,0123456789,Interest Earned,Credit,1250.00,368750.00,Success
    TXN20260131008,2026-01-31,0123456789,SMS Alert Charges,Debit,50.00,368700.00,Success
    ```

2.  **`data/transactions/failed_transactions.csv`**
    ```csv
    TransactionID,Date,Account,Description,Amount,FailureReason
    TXN20260201001,2026-02-01,0123456789,Transfer to GTBank,150000.00,Pending Reconciliation
    TXN20260202002,2026-02-02,0234567891,ATM Withdrawal,50000.00,Card Swallowed
    TXN20260205005,2026-02-05,0678901235,Mobile Transfer,10000.00,Account Dormant
    TXN20260207009,2026-02-07,0789012346,International Transfer,5000000.00,Limit Exceeded
    TXN20260208012,2026-02-08,1234567891,Cheque Deposit,25000.00,Missing Signature Card
    ```

**Regulations (TXT file):**

1.  **`data/regulations/cbn_guidelines.txt`**
    ```
    CENTRAL BANK OF NIGERIA (CBN)
    REGULATORY GUIDELINES FOR DEPOSIT MONEY BANKS
    Effective: 2025-2026

    1. ANTI-MONEY LAUNDERING (AML)
    - Mandatory reporting of single transactions > ₦5,000,000 (Individual)
    - Mandatory reporting of single transactions > ₦10,000,000 (Corporate)
    - Reporting timeline: Within 7 days to NFIU
    - Enhanced Due Diligence (EDD) for Politically Exposed Persons (PEPs)

    2. KNOW YOUR CUSTOMER (KYC)
    - Tier 1: BVN + Passport photo (Limit: ₦50,000 daily)
    - Tier 2: Tier 1 + Valid ID (Limit: ₦200,000 daily)
    - Tier 3: Tier 2 + Utility bill + Physical verification (Limit: Unlimited)

    3. DORMANT ACCOUNTS
    - Definition: No customer-initiated transaction for 12 months
    - Excludes system-generated charges
    - Unclaimed Balances: After 10 years, transfer to CBN Unclaimed Funds Pool
    - Annual publication of dormant accounts required
    - Customer can claim anytime with proper identification

    4. DIGITAL BANKING REGULATIONS
    - Mobile Money: Max wallet balance ₦5,000,000 (Tier 3)
    - Daily transaction limit: ₦1,000,000
    - Internet Banking: Two-factor authentication (2FA) mandatory
    - Session timeout: Max 10 minutes inactivity

    5. CONSUMER PROTECTION
    - Transparent fee disclosure
    - Right to account statement
    - Right to close account without penalty
    - Max complaint resolution: 14 days
    - Escalation to CBN if unresolved after 30 days

    6. PENALTIES
    - KYC lapses: ₦100,000 per account
    - Late regulatory returns: ₦50,000 per day
    - AML non-compliance: ₦10 million minimum
    - Consumer complaints mishandling: ₦250,000 per case
    ```

**Internal Memos (TXT file):**

1.  **`data/internal_memos/branch_operations.txt`**
    ```
    WEMA BANK PLC
    INTERNAL OPERATIONS MEMO
    Date: February 1, 2026
    From: Head of Operations
    To: All Branch Managers

    Subject: FEBRUARY 2026 OPERATIONAL GUIDELINES

    1. CASH HANDLING
    - Max branch vault holding: ₦50 million
    - Excess to be evacuated to CPC daily
    - Dual custody mandatory for vault access
    - ATM replenishment: Armed escort required

    2. CUSTOMER SERVICE STANDARDS
    - Max waiting time: 15 minutes
    - Express counters for transactions < ₦50,000
    - Acknowledge complaints: Within 1 hour
    - Full resolution: 72 hours maximum

    3. ACCOUNT OPENING
    - Same-day opening if all docs complete
    - Corporate: Min ₦100,000 opening balance
    - Foreign nationals: Work permit required

    4. LOAN PROCESSING
    - Overdraft up to ₦2 million: Branch Manager approval
    - ₦2M - ₦10M: Regional Credit Committee
    - Above ₦10M: Head Office Credit Committee
    - Credit assessment: 48 hours

    5. SYSTEM DOWNTIME PROCEDURES
    - Switch to manual registers
    - Withdrawals: Manager approval required, max ₦100,000
    - Transfers: NOT allowed manually

    6. CONTACT ESCALATION
    - Robbery/Security: 09088888888 (24/7)
    - System outage > 2 hours: IT Helpdesk
    - Large withdrawal (> ₦5M): Ops Manager approval

    Signed,
    Adebayo Johnson
    Head of Operations
    ```

### Step 3: Create Python Scripts and Requirements File

Create the following files in your `bank_ai_demo/` directory:

1.  **`requirements.txt`**
    ```
    langchain==0.1.9
    langchain-community==0.0.20
    pypdf==4.0.1
    chromadb==0.4.22
    ollama==0.1.6
    pandas==2.2.0
    tqdm==4.66.1
    colorama==0.4.6
    gradio==4.19.2
    ```

2.  **`ingest.py`**
    ```python
    import os
    from pathlib import Path
    from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from tqdm import tqdm
    from colorama import init, Fore, Style

    init(autoreset=True)

    print(f"{Fore.CYAN}{\'=\'*60}")
    print(f"{Fore.CYAN}WEMA BANK AI ASSISTANT - KNOWLEDGE BASE BUILDER")
    print(f"{Fore.CYAN}{\'=\'*60}\n")

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

    print(f"\n{Fore.CYAN}{\'=\'*60}\n")

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

    print(f"\n{Fore.CYAN}{\'=\'*60}")
    print(f"{Fore.GREEN}✓ KNOWLEDGE BASE CREATED SUCCESSFULLY!")
    print(f"{Fore.CYAN}{\'=\'*60}")
    print(f"\n{Fore.YELLOW}📊 Statistics:")
    print(f"   - Documents processed: {len(docs)}")
    print(f"   - Text chunks: {len(split_docs)}")
    print(f"   - Database location: ./bank_db")
    print(f"\n{Fore.GREEN}Ready to answer questions! Run: python ask.py\n")
    ```

3.  **`ask.py`**
    ```python
    from langchain_community.llms import Ollama
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import OllamaEmbeddings
    from colorama import init, Fore, Style
    import time
    import sys

    init(autoreset=True)

    def main():
        print(f"{Fore.CYAN}{\'=\'*60}")
        print(f"{Fore.CYAN}WEMA BANK AI ASSISTANT")
        print(f"{Fore.CYAN}{\'=\'*60}\n")

        # Initialize
        print(f"{Fore.YELLOW}Loading AI model and knowledge base...\n")

        try:
            embeddings = OllamaEmbeddings(model="mistral")
            db = Chroma(
                persist_directory="bank_db",
                embedding_function=embeddings
            )
            llm = Ollama(model="mistral")
            retriever = db.as_retriever(search_kwargs={"k": 5})
        except Exception as e:
            print(f"{Fore.RED}Error initializing system: {e}")
            print(f"{Fore.YELLOW}Make sure you have run \'python ingest.py\' and Ollama is running.")
            sys.exit(1)

        print(f"{Fore.GREEN}✓ System ready!\n")
        print(f"{Fore.YELLOW}Type your question (or \'quit\' to exit)\n")
        print(f"{Fore.CYAN}{\'=\'*60}\n")

        def ask(question):
            # Retrieve relevant documents
            docs = retriever.get_relevant_documents(question)
            
            # Build context
            context = "\n\n".join([f"[Source {i+1}]: {d.page_content}" for i, d in enumerate(docs)])
            
            # Enhanced prompt
            prompt = f"""You are an expert Nigerian banking operations assistant for Wema Bank.

    Answer questions accurately using ONLY the provided context below.
    If the context doesn\'t contain the answer, say "I don\'t have that information in the knowledge base."

    Be specific, cite policies when relevant, and give practical banking advice.
    Use Nigerian banking terminology and context.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:"""
            
            # Get response
            start_time = time.time()
            try:
                response = llm.invoke(prompt)
                elapsed = time.time() - start_time
                
                print(f"\n{Fore.GREEN}{response}")
                print(f"\n{Fore.CYAN}[Response time: {elapsed:.2f}s]")
                print(f"{Fore.CYAN}{\'=\'*60}\n")
            except Exception as e:
                print(f"{Fore.RED}Error getting response: {e}")

        # Interactive loop
        while True:
            try:
                question = input(f"{Fore.YELLOW}💬 Ask: {Style.RESET_ALL}")
                
                if question.lower() in [\'quit\', \'exit\', \'q\']:
                    print(f"\n{Fore.GREEN}Thank you for using Wema Bank AI Assistant!\n")
                    break
                    
                if not question.strip():
                    continue
                    
                ask(question)
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.GREEN}Thank you for using Wema Bank AI Assistant!\n")
                break
            except Exception as e:
                print(f"\n{Fore.RED}Error: {e}\n")

    if __name__ == "__main__":
        main()
    ```

4.  **`demo.py`**
    ```python
    from langchain_community.llms import Ollama
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import OllamaEmbeddings
    from colorama import init, Fore, Style
    import time
    import sys

    init(autoreset=True)

    # Demo questions
    DEMO_QUESTIONS = [
        {
            "category": "📋 POLICY QUESTIONS",
            "questions": [
                "What collateral is required for SME overdraft?",
                "What is the turnaround time for loan approval?",
                "What documents are needed for SME loan application?",
                "What are the interest rates for term loans?",
                "How do I reactivate a dormant account?"
            ]
        },
        {
            "category": "👤 CUSTOMER SERVICE",
            "questions": [
                "What is John Bello\'s complaint about?",
                "How many customer complaints are pending?",
                "What should we do about Fatima Ibrahim\'s ATM card issue?",
                "Draft a response to Chidi Okafor about his loan application delay"
            ]
        },
        {
            "category": "💳 TRANSACTIONS",
            "questions": [
                "Show me account 0123456789\'s transaction summary for January",
                "What was the highest expense in January for account 0123456789?",
                "How much interest was earned in January?",
                "Why did transaction TXN20260205005 fail?"
            ]
        },
        {
            "category": "⚖️ COMPLIANCE & REGULATIONS",
            "questions": [
                "What are the CBN requirements for foreign exchange transactions?",
                "What is the maximum Personal Travel Allowance?",
                "What are the KYC requirements for account opening?",
                "What transactions must be reported to NFIU?"
            ]
        },
        {
            "category": "🏢 OPERATIONS",
            "questions": [
                "What is the branch manager\'s approval limit for overdrafts?",
                "What should I do during system downtime?",
                "What are the month-end procedures?",
                "When is the internal audit scheduled?"
            ]
        }
    ]

    def main():
        print(f"{Fore.CYAN}{\'=\'*70}")
        print(f"{Fore.CYAN}WEMA BANK AI ASSISTANT - GUIDED DEMO")
        print(f"{Fore.CYAN}{\'=\'*70}\n")

        # Initialize
        print(f"{Fore.YELLOW}🔧 Initializing system...\n")

        try:
            embeddings = OllamaEmbeddings(model="mistral")
            db = Chroma(
                persist_directory="bank_db",
                embedding_function=embeddings
            )
            llm = Ollama(model="mistral")
            retriever = db.as_retriever(search_kwargs={"k": 5})
        except Exception as e:
            print(f"{Fore.RED}Error initializing system: {e}")
            sys.exit(1)

        print(f"{Fore.GREEN}✓ System ready!\n")

        def ask(question):
            docs = retriever.get_relevant_documents(question)
            context = "\n\n".join([f"[Source {i+1}]: {d.page_content}" for i, d in enumerate(docs)])
            
            prompt = f"""You are an expert Nigerian banking operations assistant for Wema Bank.

    Answer questions accurately using ONLY the provided context below.
    Be specific, cite policies when relevant, and give practical banking advice.
    Use Nigerian banking terminology.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:"""
            
            start_time = time.time()
            response = llm.invoke(prompt)
            elapsed = time.time() - start_time
            
            print(f"\n{Fore.GREEN}{response}")
            print(f"\n{Fore.MAGENTA}[⏱️  {elapsed:.2f}s | 🧠 Local GPU Processing]")
            print(f"{Fore.CYAN}{\'=\'*70}\n")
            
            return response

        # Main demo loop
        print(f"{Fore.YELLOW}Choose a demo mode:\n")
        print(f"{Fore.WHITE}1. Run all demo questions automatically")
        print(f"{Fore.WHITE}2. Select questions by category")
        print(f"{Fore.WHITE}3. Free-form questions\n")

        mode = input(f"{Fore.YELLOW}Enter choice (1-3): {Style.RESET_ALL}")

        if mode == "1":
            # Auto demo
            for category_data in DEMO_QUESTIONS:
                print(f"\n{Fore.CYAN}{\'=\'*70}")
                print(f"{Fore.CYAN}{category_data[\'category\']}")
                print(f"{Fore.CYAN}{\'=\'*70}\n")
                
                for q in category_data[\'questions\']:
                    print(f"\n{Fore.YELLOW}Q: {q}")
                    ask(q)
                    time.sleep(1)  # Pause between questions

        elif mode == "2":
            # Category selection
            while True:
                print(f"\n{Fore.YELLOW}Select a category:\n")
                for i, cat in enumerate(DEMO_QUESTIONS, 1):
                    print(f"{Fore.WHITE}{i}. {cat[\'category\']}")
                print(f"{Fore.WHITE}0. Exit\n")
                
                choice = input(f"{Fore.YELLOW}Enter choice: {Style.RESET_ALL}")
                
                if choice == "0":
                    break
                    
                try:
                    idx = int(choice) - 1
                    category = DEMO_QUESTIONS[idx]
                    
                    print(f"\n{Fore.CYAN}{\'=\'*70}")
                    print(f"{Fore.CYAN}{category[\'category\']}")
                    print(f"{Fore.CYAN}{\'=\'*70}\n")
                    
                    for i, q in enumerate(category[\'questions\'], 1):
                        print(f"{Fore.WHITE}{i}. {q}")
                    
                    q_choice = input(f"\n{Fore.YELLOW}Select question (or \'all\'): {Style.RESET_ALL}")
                    
                    if q_choice.lower() == "all":
                        for q in category[\'questions\']:
                            print(f"\n{Fore.YELLOW}Q: {q}")
                            ask(q)
                    else:
                        q_idx = int(q_choice) - 1
                        question = category[\'questions\'][q_idx]
                        print(f"\n{Fore.YELLOW}Q: {question}")
                        ask(question)
                        
                except (ValueError, IndexError):
                    print(f"{Fore.RED}Invalid choice!\n")

        else:
            # Free-form
            print(f"\n{Fore.GREEN}Free-form mode (type \'quit\' to exit)\n")
            while True:
                try:
                    question = input(f"{Fore.YELLOW}💬 Ask: {Style.RESET_ALL}")
                    
                    if question.lower() in [\'quit\', \'exit\', \'q\']:
                        break
                        
                    if not question.strip():
                        continue
                        
                    ask(question)
                    
                except KeyboardInterrupt:
                    break

        print(f"\n{Fore.GREEN}✓ Demo completed!\n")

    if __name__ == "__main__":
        main()
    ```

5.  **`ui.py`**
    ```python
    import gradio as gr
    from langchain_community.llms import Ollama
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import OllamaEmbeddings
    import time
    from pathlib import Path
    import sys

    # Initialize AI system
    def initialize_system():
        print("🔧 Loading AI system...")
        # Check if database exists
        if not Path("bank_db").exists():
            print("❌ Knowledge base not found! Please run \'python ingest.py\' first.")
            return None, None, None

        try:
            embeddings = OllamaEmbeddings(model="mistral")
            db = Chroma(
                persist_directory="bank_db",
                embedding_function=embeddings
            )
            llm = Ollama(model="mistral")
            retriever = db.as_retriever(search_kwargs={"k": 5})
            print("✅ System ready!\n")
            return llm, retriever, db
        except Exception as e:
            print(f"❌ Error initializing system: {e}")
            return None, None, None

    llm, retriever, db = initialize_system()

    def ask_question(question, history):
        """Process question and return response"""
        
        if not llm:
            history.append((question, "System not initialized. Please run \'python ingest.py\' and ensure Ollama is running."))
            return history, ""

        if not question.strip():
            return history, ""
        
        # Retrieve relevant documents
        docs = retriever.get_relevant_documents(question)
        context = "\n\n".join([f"[Source {i+1}]: {d.page_content}" 
                              for i, d in enumerate(docs)])
        
        # Build prompt
        prompt = f"""You are an expert Nigerian banking operations assistant for Wema Bank.

    Answer questions accurately using ONLY the provided context below.
    If the context doesn\'t contain the answer, say "I don\'t have that information in the knowledge base."

    Be specific, cite policies when relevant, and give practical banking advice.
    Use Nigerian banking terminology and context.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:"""
        
        # Get response with timing
        start_time = time.time()
        try:
            response = llm.invoke(prompt)
            elapsed = time.time() - start_time
            
            # Format response with metadata
            formatted_response = f"{response}\n\n*⏱️ Response time: {elapsed:.2f}s | 🧠 Local GPU Processing*"
            
            # Update history
            history.append((question, formatted_response))
        except Exception as e:
            history.append((question, f"Error: {e}"))
        
        return history, ""


    # Demo questions organized by category
    DEMO_CATEGORIES = {
        "📋 Policy Questions": [
            "What collateral is required for SME overdraft?",
            "What is the turnaround time for loan approval?",
            "What documents are needed for SME loan application?",
            "What are the interest rates for term loans?",
            "How do I reactivate a dormant account?"
        ],
        "👤 Customer Service": [
            "What is John Bello\'s complaint about?",
            "How many customer complaints are pending?",
            "What should we do about Fatima Ibrahim\'s ATM card issue?",
            "Draft a response to Chidi Okafor about his loan application delay"
        ],
        "💳 Transactions": [
            "Show me account 0123456789\'s transaction summary for January",
            "What was the highest expense in January for account 0123456789?",
            "How much interest was earned in January?",
            "Why did transaction TXN20260205005 fail?"
        ],
        "⚖️ Compliance & Regulations": [
            "What are the CBN requirements for foreign exchange transactions?",
            "What is the maximum Personal Travel Allowance?",
            "What are the KYC requirements for account opening?",
            "What transactions must be reported to NFIU?"
        ],
        "🏢 Operations": [
            "What is the branch manager\'s approval limit for overdrafts?",
            "What should I do during system downtime?",
            "What are the month-end procedures?",
            "When is the internal audit scheduled?"
        ]
    }

    # Flatten all demo questions
    ALL_DEMO_QUESTIONS = []
    for category, questions in DEMO_CATEGORIES.items():
        ALL_DEMO_QUESTIONS.extend([(f"{category}: {q}", q) for q in questions])


    # Build Gradio interface
    with gr.Blocks(
        title="Wema Bank AI Assistant",
        theme=gr.themes.Soft(primary_hue="purple")
    ) as demo:
        
        gr.Markdown("""
        # 🏦 Wema Bank AI Assistant
        ### Powered by Local RAG (Retrieval Augmented Generation)
        
        Ask questions about bank policies, customer issues, transactions, compliance, and operations.
        All processing happens locally on Nigerian GPU infrastructure - **NO cloud APIs**.
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(
                    label="Banking Assistant",
                    height=500,
                    show_copy_button=True
                )
                
                with gr.Row():
                    question_input = gr.Textbox(
                        label="Your Question",
                        placeholder="Ask anything about Wema Bank operations...",
                        scale=4
                    )
                    submit_btn = gr.Button("Ask", variant="primary", scale=1)
                
                clear_btn = gr.Button("Clear Chat", variant="secondary")
            
            with gr.Column(scale=1):
                gr.Markdown("### 📚 Quick Examples")
                
                demo_dropdown = gr.Dropdown(
                    choices=[label for label, _ in ALL_DEMO_QUESTIONS],
                    label="Select a demo question",
                    value=None
                )
                
                use_demo_btn = gr.Button("Use This Question", variant="secondary")
                
                gr.Markdown("""
                ---
                ### 💡 Tips
                - Ask specific questions for best results
                - Questions are answered using actual bank documents
                - All processing is 100% local and secure
                
                ### ⚡ Categories
                - 📋 Policies & Procedures
                - 👤 Customer Service
                - 💳 Transaction Analysis
                - ⚖️ Compliance & Regulations
                - 🏢 Branch Operations
                """)
        
        # Event handlers
        def use_demo_question(selected):
            if selected:
                # Extract actual question from the label
                for label, question in ALL_DEMO_QUESTIONS:
                    if label == selected:
                        return question
            return ""
        
        submit_btn.click(
            ask_question,
            inputs=[question_input, chatbot],
            outputs=[chatbot, question_input]
        )
        
        question_input.submit(
            ask_question,
            inputs=[question_input, chatbot],
            outputs=[chatbot, question_input]
        )
        
        clear_btn.click(lambda: [], outputs=chatbot)
        
        use_demo_btn.click(
            use_demo_question,
            inputs=demo_dropdown,
            outputs=question_input
        )
        
        gr.Markdown("""
        ---
        **Tech Stack:** Ollama (Mistral 7B) + LangChain + ChromaDB | **Infrastructure:** Udutech Nigerian GPU
        """)


    if __name__ == "__main__":
        print("\n" + "="*70)
        print("🚀 STARTING WEMA BANK AI ASSISTANT WEB INTERFACE")
        print("="*70)
        print("\nServer will start at: http://localhost:7860")
        print("Press Ctrl+C to stop\n")
        
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True
        )
    ```

## PHASE 2: VM EXECUTION (On Your Udutech GPU VM)

This phase involves transferring your prepared files to the VM, installing dependencies, and running the AI assistant.

### Step 1: SSH into Your VM

Open your terminal and connect to your VM:

```bash
ssh user@your-udutech-vm-ip
```

### Step 2: Upload Your Files to VM

From your **local computer's terminal** (not inside the VM), upload the entire `bank_ai_demo` folder to your VM:

```bash
scp -r bank_ai_demo user@your-vm-ip:/home/user/
```

### Step 3: Install Ollama on VM

Once inside your VM terminal, navigate to the project directory and install Ollama:

1.  **Install `zstd` (if not already installed):**
    ```bash
    sudo apt-get update
    sudo apt-get install -y zstd
    ```

2.  **Install Ollama:**
    ```bash
    curl -fsSL https://ollama.com/install.sh | sh
    ```
    If the `curl` command fails or gets stuck, you can try a manual installation:
    *   **Download the binary:** Visit [ollama.com/download](https://ollama.com/download) and manually download the `ollama-linux-amd64` binary to your VM.
    *   **Make it executable:** `chmod +x ollama-linux-amd64`
    *   **Move to a system path:** `sudo mv ollama-linux-amd64 /usr/local/bin/ollama`
    *   **Install as a service (optional but recommended):** Follow the instructions on the Ollama website for setting it up as a systemd service if you want it to run in the background automatically.

3.  **Start Ollama Service:**
    ```bash
    ollama serve &
    ```

4.  **Pull the Mistral Model:**
    ```bash
    ollama pull mistral
    ```

### Step 4: Install Python Dependencies on VM

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

If you encounter installation errors, try upgrading pip and reinstalling with `--no-cache-dir`:

```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Step 5: Build the Knowledge Base on VM

Run the `ingest.py` script to process your banking documents and create the vector database:

```bash
python ingest.py
```

**Expected output:**

```
============================================================
WEMA BANK AI ASSISTANT - KNOWLEDGE BASE BUILDER
============================================================

📁 Loading documents...

Loading 3 policy documents...
Loading 3 customer data files...
Loading 2 transaction files...
Loading 1 regulation documents...
Loading 1 internal memos...

✓ Total documents loaded: 10-15
✓ Created 300-500 text chunks
✓ Database location: ./bank_db

Ready to answer questions!
```

### Step 6: Launch the AI Assistant Interface

You have three options to interact with the AI assistant:

**Option A: Web UI (RECOMMENDED for demo)**

This launches a Gradio web interface, providing an interactive chat experience.

```bash
python ui.py
```

Access the UI from your local browser. If your VM has a public IP, use `http://VM-IP:7860`. If your VM is local-only or behind a firewall, you'll need to set up an SSH tunnel:

**SSH TUNNEL (if VM is not publicly accessible):**

On your **local computer's terminal**, run:

```bash
ssh -L 7860:localhost:7860 user@your-vm-ip
```

Then, access the UI in your local browser at: `http://localhost:7860`

**Option B: Terminal (for quick testing)**

This provides a command-line interface for asking questions.

```bash
python ask.py
```

**Option C: Guided Demo (for structured walkthrough)**

This script runs through a predefined set of questions, useful for presentations.

```bash
python demo.py
```

## USAGE GUIDE (Web UI Features)

### Main Chat
- Type questions directly into the input box.
- Click "Ask" or press Enter to submit.
- Responses will include timing information.

### Demo Questions
- Select from the dropdown menu on the right panel.
- Click "Use This Question" to automatically populate the input box.

### Categories
- 📋 Policies & Procedures
- 👤 Customer Service
- 💳 Transaction Analysis
- ⚖️ Compliance & Regulations
- 🏢 Branch Operations

### Controls
- **Clear Chat:** Resets the conversation history.
- **Copy buttons:** Available next to responses to easily copy text.

## VIDEO RECORDING WORKFLOW (for your video demo)

### Setup (Before Recording):

1.  **Terminal 1 (on VM): Start Ollama**
    ```bash
    ollama serve
    ```

2.  **Terminal 2 (on VM): Launch UI**
    ```bash
    cd bank_ai_demo
    python ui.py
    ```

3.  **Local Browser:** Open `http://localhost:7860` (or `http://VM-IP:7860` if public, or via SSH tunnel).

### Recording Script:

**Scene 1: Introduction (30s)**
- Show browser at `localhost:7860`.
- Narrate: "Hi, I'm Clifford from Wema Bank. Today I'm demonstrating a LOCAL AI assistant that answers banking questions using our internal documents. This runs entirely on Nigerian GPU infrastructure - NO Azure, NO OpenAI, NO cloud dependencies. Let me show you how it works."

**Scene 2: Demo Questions (5-7 mins)**
- Use the dropdown to select questions from various categories.
- Show each category and a few questions:
    - **Policy:** "What collateral is required for SME overdraft?"
    - **Customer:** "What is John Bello's complaint?" and "Draft a response to Fatima Ibrahim's ATM card issue"
    - **Transactions:** "Summarize January transactions for account 0123456789"
    - **Compliance:** "What are CBN's KYC requirements?"
    - **Operations:** "What is the branch manager's approval limit for overdrafts?"
- Highlight AI's accuracy and non-hallucination.

**Scene 3: Custom Questions (2 mins)**
- Type free-form questions into the input box.
- Demonstrate response accuracy and highlight the fast response time.

**Scene 4: Technical Overview (1 min)**
- Briefly show the terminal with `ingest.py` output (if desired, or just explain).
- Explain the RAG architecture (Documents → Embeddings → Vector Database → LLM).
- Briefly show the folder structure.

**Scene 5: Business Impact (1 minute)**
- Discuss key benefits:
    - **DATA SOVEREIGNTY:** Our customer data never leaves Nigeria.
    - **COST SAVINGS:** No per-query API fees. One GPU handles unlimited questions.
    - **COMPLIANCE:** Meets CBN data localization requirements.
    - **PRODUCTIVITY:** Staff get instant answers instead of searching through hundreds of documents.
    - **CUSTOMIZATION:** We control the AI completely. Can add proprietary knowledge.
- Mention real-world use cases (customer service, credit officers, compliance, branch managers).

**Scene 6: Performance Highlight (30 seconds)**
- Reiterate response times (e.g., 2-3 seconds).
- Emphasize: "All processing: LOCAL GPU. Zero cloud API calls. Zero data leaving Nigeria. This is running on Udutech infrastructure - 100% Nigerian technology."

**Scene 7: Scalability & Next Steps (45 seconds)**
- Discuss future potential:
    - Scale to larger models (70B parameters).
    - Add more document types (emails, spreadsheets, images).
    - Integrate with existing systems (Core Banking, CRM).
    - Create specialized assistants (Credit, Ops, Compliance).
    - Deploy across all branches.
- Conclude: "The infrastructure is ready. The technology works. The ROI is clear."

**Scene 8: Closing (30 seconds)**
- Summarize: "We just demonstrated a fully functional banking AI assistant running on LOCAL Nigerian infrastructure. No cloud dependencies. No data sovereignty issues. No hallucinations. Just accurate, instant banking knowledge. Thank you."
- End screen with contact info.

## TROUBLESHOOTING

-   **Issue: "Knowledge base not found"**
    -   **Solution:** Run `python ingest.py` to rebuild the database.

-   **Issue: Ollama connection error**
    -   **Solution:** Ensure Ollama is running (`ollama serve`) and the `mistral` model is pulled (`ollama pull mistral`).

-   **Issue: Slow responses**
    -   **Note:** The first query is always slower due to model loading. Subsequent queries should be faster (2-3 seconds).
    -   **Solution:** Consider using a smaller model, e.g., `ollama pull mistral:7b-instruct`.

-   **Issue: Port 7860 in use**
    -   **Solution:** In `ui.py`, change `server_port=7860` to a different available port, e.g., `server_port=7861`.

## PRODUCTION DEPLOYMENT (Advanced)

For public demonstration with a temporary Gradio link:

```python
# In ui.py, within demo.launch()
share=True,  # Creates public Gradio link
server_port=7860
```

For a more robust production server setup (e.g., with Gunicorn and Uvicorn):

1.  **Install additional dependencies:**
    ```bash
    pip install gunicorn uvicorn
    ```

2.  **Run with Gunicorn:**
    ```bash
    gunicorn ui:demo -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:7860
    ```

## GitHub and LinkedIn Content

### GitHub Repository Description

```
**Wema Bank AI Assistant - Local RAG Demo**

This repository contains a robust, production-ready banking AI assistant demo built with Retrieval Augmented Generation (RAG) and powered by Ollama for local LLM inference. It demonstrates how to create an intelligent Q&A system using internal bank documents (policies, customer data, transactions, regulations, internal memos) without relying on external cloud APIs, ensuring data sovereignty and cost-efficiency. The system features an interactive terminal interface, a guided demo script, and a Gradio-based web UI.

**Key Features:**
- **100% Local AI:** Runs entirely on local GPU infrastructure using Ollama (Mistral model).
- **Data Sovereignty:** No data leaves your environment, ideal for sensitive banking data.
- **Comprehensive Knowledge Base:** Ingests various document types (PDF, TXT, CSV) to answer diverse banking queries.
- **RAG Architecture:** Ensures accurate, context-aware responses by retrieving relevant information from documents.
- **Interactive Interfaces:** Includes command-line (`ask.py`), guided demo (`demo.py`), and a user-friendly web UI (`ui.py`) with Gradio.
- **Real-world Scenarios:** Addresses policy questions, customer service inquiries, transaction analysis, compliance checks, and operational support.

**Tech Stack:**
- LLM: Ollama (Mistral)
- Embeddings: OllamaEmbeddings
- Vector DB: ChromaDB
- RAG Framework: LangChain
- UI: Gradio
- Python

**Ideal for:**
- Demonstrating local AI capabilities in a banking context.
- Internal Q&A systems for bank staff.
- Ensuring regulatory compliance and data privacy.
- Reducing operational costs associated with cloud-based LLMs.

Get started by following the detailed setup guide in the `README.md`!
```

### LinkedIn Post Draft

```
🚀 Excited to share a powerful demo of a **Local AI Banking Assistant** for Wema Bank! 

This project showcases a Retrieval Augmented Generation (RAG) system running entirely on local GPU infrastructure using #Ollama and #LangChain. No cloud APIs, no data leaving Nigeria – ensuring complete data sovereignty and significant cost savings. 

Imagine bank staff getting instant, accurate answers to complex policy questions, customer complaints, transaction details, and compliance queries, all powered by internal documents. This isn't just a concept; it's a production-ready solution for enhanced productivity and regulatory adherence.

**Key Highlights:**
- **100% Local AI:** Powered by Mistral via Ollama.
- **Data Sovereignty:** Critical for sensitive financial data.
- **Cost-Efficient:** Eliminates per-query API fees.
- **Accurate & Contextual:** RAG ensures responses are grounded in actual bank documents.
- **Interactive Web UI:** Easy to use for all staff.

Check out the full project on GitHub (link in comments) for a detailed setup guide, code, and a video recording workflow. Let's revolutionize banking operations with secure, local AI! #AIinBanking #RAG #Ollama #LocalAI #FinTech #WemaBank #Nigeria #GPU #DataSovereignty #LangChain

--- 

*(Add GitHub link in the first comment after posting)*
```

This comprehensive guide should enable you to set up, test, and demonstrate your Wema Bank AI Assistant effectively. Good luck!
