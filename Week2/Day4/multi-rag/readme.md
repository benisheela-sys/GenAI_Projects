# 📚 Multi-PDF RAG Assistant

## Setup Instructions

1. **Create and enter the project directory:**

   ```
   mkdir multi-rag
   cd multi-rag
   
   ```

2. **Create a virtual environment:**

   ```
   # For Windows
   py -3.13 -m venv venv
   
   # For macOS/Linux
   python3.13 -m venv venv
   
   ```

3. **Activate the virtual environment:**

   ```
   # For Windows
   venv\Scripts\activate
   
   # For macOS/Linux
   source venv/bin/activate
   
   ```

4. **Configure your API Key:**
   Create a file named `.env` in the root folder of your project and add your OpenAI API key:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   
   ```

## Dependencies

With your virtual environment activated, install the required packages by running:

```
pip install streamlit langchain-community langchain-openai langchain-text-splitters faiss-cpu sentence-transformers python-dotenv pypdf tiktoken

```

## How to Run the Application

1. Start the Streamlit server from your terminal:

   ```
   streamlit run rag_app.py
   
   ```

2. Open the URL provided in your terminal (usually `http://localhost:8501`) in your web browser.

3. Use the left sidebar to browse and upload your PDF files.

4. Click **"Process PDFs"** and wait for the success message indicating the chunks are indexed.

5. Use the chat box at the bottom of the screen to ask questions about the uploaded documents.