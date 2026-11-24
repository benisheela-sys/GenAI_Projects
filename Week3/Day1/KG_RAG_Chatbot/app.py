import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="TN Schemes KG-RAG Bot", layout="centered")
st.title("Tamil Nadu Schemes KG-RAG Assistant")
st.caption("Powered by Neo4j Knowledge Graph, FastAPI, and Streamlit")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("cypher"):
            with st.expander("View Generated Cypher Query"):
                st.code(msg["cypher"], language="cypher")

# Handle user input
if prompt := st.chat_input("Ask about Tamil Nadu schemes, eligibility, or benefits..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Querying Knowledge Graph..."):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={"question": prompt},
                    timeout=30,
                )
                res.raise_for_status()
                data = res.json()
                answer = data["answer"]
                cypher = data.get("cypher_query", "")

                st.markdown(answer)
                if cypher:
                    with st.expander("View Generated Cypher Query"):
                        st.code(cypher, language="cypher")

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "cypher": cypher}
                )
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")