# 🌾 Farmer Government Schemes Assistant

**A Buildathon Submission**

An AI-powered conversational assistant designed to help farmers and agricultural stakeholders easily understand, query, and access government agricultural schemes. Built using a modern RAG (Retrieval-Augmented Generation) pipeline, this tool ensures users only get accurate information backed by official documents.

---

## 🚀 Key Features

*   **Intelligent Document Validation:** Features an LLM-powered gatekeeper that strictly analyzes uploaded PDFs, automatically rejecting documents that aren't related to agricultural government schemes or farming policies.
*   **Conversational RAG:** Chat with official documents using a Retrieval-Augmented Generation pipeline (LangChain, FAISS, and OpenAI) that remembers chat history for contextual follow-up questions.
*   **Dynamic Follow-up Suggestions:** Context-aware suggested prompts (e.g., PM-KISAN, PMFBY) help guide users who might not know what to ask.
*   **Observability Mode:** Built-in toggles for LangSmith trace tracking to monitor LLM performance and token usage.
*   **Multilingual Support (UI):** Foundation laid for localized querying (English and Tamil).
*   **Seamless Document Management:** Upload, view, and download approved official PDFs directly from the UI.
*   **Exportable Chat History:** Users can download their consultation histories as `.txt` files for offline reference.

---

## 🛠️ Tech Stack

### Frontend
*   **Streamlit:** For a responsive, interactive, and custom-styled web interface.
*   **Streamlit Option Menu:** For modern sidebar navigation.

### Backend
*   **FastAPI:** High-performance API server handling document processing and chat endpoints.
*   **LangChain:** Orchestrating the RAG pipeline, document chunking, and conversational chains.
*   **OpenAI (`gpt-4o-mini`):** Used for both document validation and generating conversational responses.
*   **HuggingFace Embeddings (`all-MiniLM-L6-v2`):** Efficient, local open-source embedding model.
*   **FAISS:** Local vector database for fast similarity search.

---

## 🏗️ Architecture / Pipelines

1.  **Document Ingestion Pipeline:** 
    `PDF Upload -> PyPDFLoader -> LLM Content Validation -> Text Splitting (Recursive) -> HuggingFace Embeddings -> FAISS VectorDB`
2.  **Conversational RAG Pipeline:**
    `User Query -> FAISS Retrieval (Top 4 chunks) -> ChatOpenAI (gpt-4o-mini) + Chat History -> Answer & Sources -> Streamlit UI`

---

## ⚙️ Setup and Installation

### Prerequisites
*   Python 3.9+
*   OpenAI API Key

### 1. Clone the repository and install dependencies
Create a virtual environment and install the required Python packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies (You can place these in a requirements.txt)
pip install fastapi uvicorn streamlit langchain langchain-openai langchain-community langchain-huggingface sentence-transformers faiss-cpu pydantic python-dotenv python-multipart streamlit-option-menu
```

### 2. Environment Variables
Create a `.env` file in the root directory and add your OpenAI API key (and optionally LangSmith tracking keys):

```env
OPENAI_API_KEY=your_openai_api_key_here

# Optional: LangSmith Observability
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=your_langchain_api_key
# LANGCHAIN_PROJECT=farmer_schemes_project
```

### 3. Run the Backend Server
Start the FastAPI server. It will run on `http://localhost:8000`.

```bash
python -m uvicorn backend:app --reload --port 8000
```

### 4. Run the Frontend Application
In a new terminal window (with the virtual environment activated), start the Streamlit app:

```bash
streamlit run frontend.py
```

---

## 💡 How to Use

1.  **Upload Schemes:** Navigate to the "Manage Schemes" tab in the sidebar and upload official agricultural PDFs. (Test the validation by trying to upload a non-agricultural PDF!).
2.  **Chat:** Go to the main chat interface and ask questions like *"What are the eligibility criteria for PM-KISAN?"*
3.  **Trace:** Turn on "Observability Mode" in "Chat Settings" to view simulated/actual LangSmith trace IDs.
4.  **Export:** Go to "Export History" to download your session's Q&A.

---
*Created for the Buildathon.*