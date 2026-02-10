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
            "What is John Bello's complaint about?",
            "How many customer complaints are pending?",
            "What should we do about Fatima Ibrahim's ATM card issue?",
            "Draft a response to Chidi Okafor about his loan application delay"
        ]
    },
    {
        "category": "💳 TRANSACTIONS",
        "questions": [
            "Show me account 0123456789's transaction summary for January",
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
            "What is the branch manager's approval limit for overdrafts?",
            "What should I do during system downtime?",
            "What are the month-end procedures?",
            "When is the internal audit scheduled?"
        ]
    }
]

def main():
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}WEMA BANK AI ASSISTANT - GUIDED DEMO")
    print(f"{Fore.CYAN}{'='*70}\n")

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
        print(f"{Fore.CYAN}{'='*70}\n")
        
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
            print(f"\n{Fore.CYAN}{'='*70}")
            print(f"{Fore.CYAN}{category_data['category']}")
            print(f"{Fore.CYAN}{'='*70}\n")
            
            for q in category_data['questions']:
                print(f"{Fore.YELLOW}Q: {q}")
                ask(q)
                time.sleep(1)  # Pause between questions

    elif mode == "2":
        # Category selection
        while True:
            print(f"\n{Fore.YELLOW}Select a category:\n")
            for i, cat in enumerate(DEMO_QUESTIONS, 1):
                print(f"{Fore.WHITE}{i}. {cat['category']}")
            print(f"{Fore.WHITE}0. Exit\n")
            
            choice = input(f"{Fore.YELLOW}Enter choice: {Style.RESET_ALL}")
            
            if choice == "0":
                break
                
            try:
                idx = int(choice) - 1
                category = DEMO_QUESTIONS[idx]
                
                print(f"\n{Fore.CYAN}{'='*70}")
                print(f"{Fore.CYAN}{category['category']}")
                print(f"{Fore.CYAN}{'='*70}\n")
                
                for i, q in enumerate(category['questions'], 1):
                    print(f"{Fore.WHITE}{i}. {q}")
                
                q_choice = input(f"\n{Fore.YELLOW}Select question (or 'all'): {Style.RESET_ALL}")
                
                if q_choice.lower() == "all":
                    for q in category['questions']:
                        print(f"\n{Fore.YELLOW}Q: {q}")
                        ask(q)
                else:
                    q_idx = int(q_choice) - 1
                    question = category['questions'][q_idx]
                    print(f"\n{Fore.YELLOW}Q: {question}")
                    ask(question)
                    
            except (ValueError, IndexError):
                print(f"{Fore.RED}Invalid choice!\n")

    else:
        # Free-form
        print(f"\n{Fore.GREEN}Free-form mode (type 'quit' to exit)\n")
        while True:
            try:
                question = input(f"{Fore.YELLOW}💬 Ask: {Style.RESET_ALL}")
                
                if question.lower() in ['quit', 'exit', 'q']:
                    break
                    
                if not question.strip():
                    continue
                    
                ask(question)
                
            except KeyboardInterrupt:
                break

    print(f"\n{Fore.GREEN}✓ Demo completed!\n")

if __name__ == "__main__":
    main()
