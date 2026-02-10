from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from colorama import init, Fore, Style
import time
import sys
from router import classify_query

init(autoreset=True)

SYSTEM_PROMPT = """
You are a commercial Bank Internal AI Assistant.

Rules:
- Answer ONLY using the provided context
- If the answer is not in the context say:
    "I could not find this information in the bank knowledge base."
- Never guess banking policies
- Never fabricate procedures
- Do not use general world knowledge for bank rules
- Keep answers concise and professional
"""

def main():
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}WEMA BANK AI ASSISTANT")
    print(f"{Fore.CYAN}{'='*60}\n")

    # Initialize
    print(f"{Fore.YELLOW}Loading AI model and knowledge base...\n")

    try:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        db = Chroma(
            persist_directory="bank_db",
            embedding_function=embeddings,
            collection_name="wema_knowledge"
        )
        llm = Ollama(model="mistral")
        retriever = db.as_retriever(search_kwargs={"k": 5})
    except Exception as e:
        print(f"{Fore.RED}Error initializing system: {e}")
        print(f"{Fore.YELLOW}Make sure you have run 'python ingest.py' and Ollama is running.")
        sys.exit(1)

    print(f"{Fore.GREEN}✓ System ready!\n")
    print(f"{Fore.YELLOW}Type your question (or 'quit' to exit)\n")
    print(f"{Fore.CYAN}{'='*60}\n")

    def detect_scope(query: str):
        q = query.lower()
        if any(w in q for w in ["policy", "procedure", "guideline"]):
            return {"type": "policy"}
        if any(w in q for w in ["regulation", "cbn", "compliance"]):
            return {"type": "regulation"}
        if any(w in q for w in ["memo", "circular", "announcement"]):
            return {"type": "memo"}
        return None

    def ask(question):
        # Routing: decide query type
        query_type = classify_query(question)

        if query_type == "DATA":
            print(f"\n{Fore.MAGENTA}🔒 This question requires access to live banking data.")
            print(f"{Fore.MAGENTA}Connect the assistant to the Core Banking/EDW system to enable this feature.\n")
            return

        if query_type == "ACTION":
            print(f"\n{Fore.MAGENTA}🛠 This is an action request (messaging/automation).")
            print(f"{Fore.MAGENTA}Action tools are not enabled yet.\n")
            return

        # Knowledge retrieval only
        filter_meta = detect_scope(question)

        # Retrieve relevant documents with dynamic metadata filter
        if filter_meta:
            docs = db.similarity_search(question, k=4, filter=filter_meta)
        else:
            docs = db.similarity_search(question, k=4)

        # Build strict, grounded context
        context = "\n\n".join([d.page_content for d in docs])

        # Grounded system prompt
        prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question: {question}

Answer:
"""

        # Get response
        start_time = time.time()
        try:
            response = llm.invoke(prompt)
            elapsed = time.time() - start_time
            
            print(f"\n{Fore.GREEN}{response}")
            print(f"\n{Fore.CYAN}[Response time: {elapsed:.2f}s]")
            print(f"{Fore.CYAN}{'='*60}\n")
        except Exception as e:
            print(f"{Fore.RED}Error getting response: {e}")

    # Interactive loop
    while True:
        try:
            question = input(f"{Fore.YELLOW}💬 Ask: {Style.RESET_ALL}")
            
            if question.lower() in ['quit', 'exit', 'q']:
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
