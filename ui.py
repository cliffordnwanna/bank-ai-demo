import gradio as gr
from langchain_ollama import OllamaLLM, OllamaEmbeddings  # Updated imports
from langchain_chroma import Chroma  # Updated import
import time
from pathlib import Path
import sys

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

# Initialize AI system
def initialize_system():
    print("🔧 Loading AI system...")
    # Check if database exists
    if not Path("bank_db").exists():
        print("❌ Knowledge base not found! Please run 'python ingest.py' first.")
        return None, None, None

    try:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        db = Chroma(
            persist_directory="bank_db",
            embedding_function=embeddings,
            collection_name="wema_knowledge"
        )
        llm = OllamaLLM(model="mistral")
        retriever = db.as_retriever(search_kwargs={"k": 5})
        print("✅ System ready!\n")
        return llm, retriever, db
    except Exception as e:
        print(f"❌ Error initializing system: {e}")
        return None, None, None

llm, retriever, db = initialize_system()

def detect_scope(query: str):
    q = query.lower()
    if any(w in q for w in ["policy", "procedure", "guideline"]):
        return {"type": "policy"}
    if any(w in q for w in ["regulation", "cbn", "compliance"]):
        return {"type": "regulation"}
    if any(w in q for w in ["memo", "circular", "announcement"]):
        return {"type": "memo"}
    return None

def ask_question(question, history):
    """Process question and return response"""
    
    if not llm:
        history.append((question, "System not initialized. Please run 'python ingest.py' and ensure Ollama is running."))
        return history, ""

    if not question.strip():
        return history, ""
    
    # Optional metadata filtering based on query intent
    filter_meta = detect_scope(question)

    # Retrieve relevant documents with dynamic metadata filter
    if filter_meta:
        docs = db.similarity_search(question, k=5, filter=filter_meta)
    else:
        docs = db.similarity_search(question, k=5)

    # Build strict grounded context
    context = "\n\n".join([d.page_content for d in docs])
    
    # Build prompt
    prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question: {question}

Answer:
"""
    
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
        "What is John Bello's complaint about?",
        "How many customer complaints are pending?",
        "What should we do about Fatima Ibrahim's ATM card issue?",
        "Draft a response to Chidi Okafor about his loan application delay"
    ],
    "💳 Transactions": [
        "Show me account 0123456789's transaction summary for January",
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
        "What is the branch manager's approval limit for overdrafts?",
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
    title="Wema Bank AI Assistant"
) as demo:  # Removed theme from here
    
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
                buttons=["copy"]  # Replaced show_copy_button with this
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
        show_error=True,
        theme=gr.themes.Soft(primary_hue="purple")  # Moved theme here
    )