import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def create_vector_db(uploaded_files):
    """Processes multiple uploaded PDFs, maps correct metadata, and creates a FAISS DB."""
    all_documents = []
    
    for uploaded_file in uploaded_files:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name
            
        loader = PyPDFLoader(temp_file_path)
        documents = loader.load()
        
        # Overwrite the temporary file path with the actual uploaded filename
        for doc in documents:
            doc.metadata["source"] = uploaded_file.name
            # PyPDFLoader pages are 0-indexed; add 1 for human-readable page numbers
            if "page" in doc.metadata:
                doc.metadata["page"] += 1
                
        all_documents.extend(documents)
        os.remove(temp_file_path)

    if not all_documents:
        return None, 0

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(all_documents)

    embeddings = get_embeddings()
    vector_db = FAISS.from_documents(chunks, embeddings)
    
    return vector_db, len(chunks)

def ask_question(question, vector_db):
    """Retrieves context, generates an answer, and appends the source files/pages."""
    # 1. Retrieve the matching chunks
    docs = vector_db.similarity_search(question, k=3)
    context = "\n\n".join(doc.page_content for doc in docs)

    # 2. Generate the answer
    prompt = ChatPromptTemplate.from_template("""
You are a helpful RAG assistant.

Answer the user's question only using the given context.
If the answer is not available in the context, say:
"I don't know from the provided document."

Context:
{context}

Question:
{question}

Answer:
""")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    chain = prompt | llm
    response = chain.invoke({
        "context": context,
        "question": question
    })

    # 3. Extract and format the sources from the retrieved chunks
    source_list = []
    for doc in docs:
        source_name = doc.metadata.get("source", "Unknown")
        page_num = doc.metadata.get("page", "Unknown")
        source_list.append(f"{source_name} - page {page_num}")
    
    # Remove exact duplicates while preserving order
    unique_sources = list(dict.fromkeys(source_list))
    sources_formatted = " | ".join(unique_sources)

    # Combine the final output
    final_output = f"{response.content}\n\n**Sources:** {sources_formatted}"
    
    return final_output

def main():
    st.set_page_config(page_title="Multi-PDF RAG Assistant", page_icon="📚")
    st.title("📚 Multi-PDF RAG Assistant")

    if "vector_db" not in st.session_state:
        st.session_state.vector_db = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "upload_status" not in st.session_state:
        st.session_state.upload_status = ""

    # Sidebar
    with st.sidebar:
        st.header("Document Upload")
        uploaded_files = st.file_uploader(
            "Upload your PDF files", 
            type=["pdf"], 
            accept_multiple_files=True
        )
        
        if st.button("Process PDFs"):
            if uploaded_files:
                with st.spinner("Processing documents..."):
                    vector_db, num_chunks = create_vector_db(uploaded_files)
                    st.session_state.vector_db = vector_db
                    
                    # Format the successful upload message exactly as requested
                    file_names = ", ".join([f.name for f in uploaded_files])
                    st.session_state.upload_status = f"**Uploaded:** {file_names}  \n**Indexed {num_chunks} chunks.**"
                    st.success("Ready!")
            else:
                st.warning("Please upload at least one PDF first.")

    # Display upload status at the top of the chat if documents are processed
    if st.session_state.upload_status:
        st.info(st.session_state.upload_status)

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your documents"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if st.session_state.vector_db is None:
                response = "Please upload and process your PDFs first using the sidebar."
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                with st.spinner("Retrieving answers..."):
                    # The ask_question function now returns the answer + formatted sources
                    response = ask_question(prompt, st.session_state.vector_db)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()