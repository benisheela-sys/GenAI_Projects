import os
import shutil
from typing import List, Tuple
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_classic.chains import ConversationalRetrievalChain

load_dotenv()

app = FastAPI(title="Farmer Government Schemes API")

# Directories
STORAGE_DIR = "uploaded_schemes"
FAISS_INDEX_PATH = "faiss_index"
os.makedirs(STORAGE_DIR, exist_ok=True)

# Initialize Embeddings and LLM
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class ChatRequest(BaseModel):
    question: str
    chat_history: List[Tuple[str, str]] = []

def get_vectorstore():
    """Loads existing FAISS index or returns None if it doesn't exist yet."""
    # Check if the actual index file exists, not just the directory
    index_file = os.path.join(FAISS_INDEX_PATH, "index.faiss")
    if os.path.exists(index_file):
        return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    return None

def validate_agricultural_scheme(text: str) -> bool:
    """LLM-powered document validation to restrict uploads strictly to ag schemes."""
    prompt = f"""
    Analyze the following text extract from a PDF. 
    Is this document strictly about agricultural government schemes, farming policies, or farmer subsidies?
    Answer ONLY with 'YES' or 'NO'.
    
    Text Extract: {text[:2000]}
    """
    response = llm.invoke(prompt)
    return "YES" in response.content.upper()

@app.post("/upload")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    results = []
    vectorstore = get_vectorstore()
    
    for file in files:
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
            
        try:
            # Extract text for validation
            loader = PyPDFLoader(temp_path)
            documents = loader.load()
            full_text = " ".join([doc.page_content for doc in documents])
            
            # Pipeline 1: Validate content
            if not validate_agricultural_scheme(full_text):
                results.append({"filename": file.filename, "status": "Rejected: Not an agricultural government scheme."})
                os.remove(temp_path)
                continue
                
            # Split and Embed
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(documents)
            
            if vectorstore is None:
                vectorstore = FAISS.from_documents(chunks, embeddings)
            else:
                vectorstore.add_documents(chunks)
            
            vectorstore.save_local(FAISS_INDEX_PATH)
            
            # Save approved file for user download
            final_path = os.path.join(STORAGE_DIR, file.filename)
            shutil.move(temp_path, final_path)
            results.append({"filename": file.filename, "status": "Success: Stored in VectorDB."})
            
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            results.append({"filename": file.filename, "status": f"Error: {str(e)}"})
            
    return {"results": results}

@app.get("/list_files")
async def list_files():
    """Returns a list of approved and stored scheme PDFs."""
    if not os.path.exists(STORAGE_DIR):
        return {"files": []}
    return {"files": os.listdir(STORAGE_DIR)}

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Serves the PDF file for download."""
    file_path = os.path.join(STORAGE_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/pdf', filename=filename)
    raise HTTPException(status_code=404, detail="File not found")

@app.post("/chat")
async def chat_with_schemes(request: ChatRequest):
    """Pipeline 2: Chatbot querying the VectorDB with chat history."""
    vectorstore = get_vectorstore()
    if not vectorstore:
        raise HTTPException(status_code=400, detail="VectorDB is empty. Upload PDFs first.")
        
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    
    response = qa_chain.invoke({
        "question": request.question,
        "chat_history": request.chat_history
    })
    
    return {"answer": response["answer"]}