from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from colorama import init, Fore, Style
import time
import sys

init(autoreset=True)

def main():
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}WEMA BANK AI ASSISTANT")
    print(f"{Fore.CYAN}{'='*60}\n")

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
        print(f"{Fore.YELLOW}Make sure you have run 'python ingest.py' and Ollama is running.")
        sys.exit(1)

    print(f"{Fore.GREEN}✓ System ready!\n")
    print(f"{Fore.YELLOW}Type your question (or 'quit' to exit)\n")
    print(f"{Fore.CYAN}{'='*60}\n")

    def ask(question):
        # Retrieve relevant documents
        docs = retriever.get_relevant_documents(question)
        
        # Build context
        context = "\n\n".join([f"[Source {i+1}]: {d.page_content}" for i, d in enumerate(docs)])
        
        # Enhanced prompt
        prompt = f"""You are an expert Nigerian banking operations assistant for Wema Bank.

Answer questions accurately using ONLY the provided context below.
If the context doesn't contain the answer, say "I don't have that information in the knowledge base."

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
