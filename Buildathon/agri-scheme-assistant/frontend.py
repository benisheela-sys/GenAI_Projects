import streamlit as st
import requests
import time
from streamlit_option_menu import option_menu

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Farmer Government Schemes", layout="wide", page_icon="🌾")

# Custom CSS for background and improved UI
# Custom CSS for background and improved UI
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f2; }
    [data-testid="stSidebar"] { background-color: #e8f0e5; border-right: 1px solid #d1e0cc; }
    h1, h2, h3 { color: #2e5339 !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stChatMessage { background-color: #ffffff; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 8px; border: none; padding: 10px 20px; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: #45a049; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    .stDownloadButton>button { background-color: #f0f0f0; color: #333; padding: 5px 10px; }
    .stDownloadButton>button:hover { background-color: #e0e0e0; }
    [data-testid="stFileUploadDropzone"] { background-color: #ffffff; border: 2px dashed #4CAF50; border-radius: 10px; }
    
    /* --- New: Feedback Thumbs Styling --- */
    /* Thumbs Up (First Button) Selected State */
    [data-testid="stFeedback"] button:nth-of-type(1)[aria-pressed="true"] svg {
        fill: #4CAF50 !important; /* Green */
        color: #4CAF50 !important;
    }
    
    /* Thumbs Down (Second Button) Selected State */
    [data-testid="stFeedback"] button:nth-of-type(2)[aria-pressed="true"] svg {
        fill: #f44336 !important; /* Red */
        color: #f44336 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌾 Farmer Government Schemes Assistant")
st.markdown("Welcome! Upload scheme documents and ask questions to get instant, accurate information.")

# Initialize Session State Variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "observability" not in st.session_state:
    st.session_state.observability = False
if "selected_lang" not in st.session_state:
    st.session_state.selected_lang = "English"

# --- SIDEBAR: Modern Navigation Menu ---
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",  
        options=["Chat Settings", "Manage Schemes", "Export History"], 
        icons=["chat-dots", "folder2-open", "download"], 
        menu_icon="cast", 
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "transparent"},
            "icon": {"color": "#4CAF50", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#d1e3cb"},
            "nav-link-selected": {"background-color": "#4CAF50", "color": "white"},
        }
    )

    st.divider()

    # --- TAB 1: Chat Settings ---
    if selected == "Chat Settings":
        st.header("⚙️ Settings & Tools")
        
        st.session_state.observability = st.checkbox(
            "🐞 Enable Observability Mode (LangSmith Traces)", 
            value=st.session_state.observability
        )
        
        if st.button("🗑️ Clear Conversation"):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.rerun()

        st.divider()
        st.header("🌍 Language / மொழி")
        
        lang_options = ["English", "தமிழ் (Tamil)"]
        default_index = lang_options.index(st.session_state.selected_lang) if st.session_state.selected_lang in lang_options else 0
        
        st.session_state.selected_lang = st.selectbox(
            "Choose your preferred language:",
            lang_options,
            index=default_index
        )

    # --- TAB 2: Manage Schemes ---
    elif selected == "Manage Schemes":
        st.header("📂 Manage Schemes")
        st.markdown("Upload official PDF documents here.")
        
        uploaded_files = st.file_uploader(
            "Upload Agricultural Schemes:", 
            type=["pdf"], 
            accept_multiple_files=True,
            help="Only PDF files are supported."
        )
        
        if st.button("Upload PDFs") and uploaded_files:
            with st.spinner("Validating and Embedding PDFs..."):
                files_data = [("files", (file.name, file.getvalue(), "application/pdf")) for file in uploaded_files]
                response = requests.post(f"{API_URL}/upload", files=files_data)
                
                if response.status_code == 200:
                    results = response.json().get("results", [])
                    for res in results:
                        if "Success" in res["status"]:
                            st.toast(f"✅ {res['filename']} - {res['status']}")
                        else:
                            st.toast(f"❌ {res['filename']} - {res['status']}")
                else:
                    st.toast("⚠️ Failed to connect to the backend.")

        st.divider()
        st.header("📄 Available Documents")
        try:
            files_response = requests.get(f"{API_URL}/list_files").json()
            available_files = files_response.get("files", [])
            
            if available_files:
                for file_name in available_files:
                    with st.expander(f"📎 {file_name}"):
                        st.markdown("**Key Beneficiaries:** Small and Marginal Farmers")
                        st.markdown("**Status:** Active / Ongoing")
                        
                        file_data = requests.get(f"{API_URL}/download/{file_name}")
                        if file_data.status_code == 200:
                            st.download_button(
                                label="⬇️ Download Full PDF",
                                data=file_data.content,
                                file_name=file_name,
                                mime="application/pdf",
                                key=f"dl_{file_name}",
                                help=f"Download {file_name}"
                            )
            else:
                st.info("No approved schemes available yet.")
        except Exception:
            st.warning("Backend server not running.")

    # --- TAB 3: Export History ---
    elif selected == "Export History":
        st.header("💾 Export History")
        
        if st.session_state.messages:
            chat_export = "Farmer Government Schemes - Chat History\n"
            chat_export += "="*40 + "\n\n"
            for msg in st.session_state.messages:
                role = "User" if msg["role"] == "user" else "Assistant"
                chat_export += f"{role}:\n{msg['content']}\n\n"
                if msg.get("sources"):
                    chat_export += f"Sources: {', '.join(msg['sources'])}\n\n"
            
            st.download_button(
                label="📥 Download Chat (.txt)",
                data=chat_export,
                file_name="scheme_chat_history.txt",
                mime="text/plain",
                help="Save this conversation for offline reference"
            )
        else:
            st.info("No chat history to download yet.")

# Main Body: Chatbot Pipeline (Always Visible)
st.header("💬 Scheme Query Assistant")

# Display chat messages from history with Feedback
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Display sources, trace ID, and feedback if available in history
        if msg["role"] == "assistant":
            if st.session_state.observability and msg.get("trace_id"):
                st.caption(f"🔧 LangSmith Trace ID: `{msg['trace_id']}`")
            if msg.get("sources"):
                with st.expander("🔍 View Source Documents"):
                    for source in msg["sources"]:
                        st.info(source)
            
            # Answer Feedback Mechanism
            feedback = st.feedback("thumbs", key=f"feedback_{idx}")
            if feedback is not None:
                pass

# Dynamic Follow-up Suggestions
def get_dynamic_suggestions(last_response_text):
    text = last_response_text.lower()
    if "kisan" in text:
        return ["How do I apply for PM-KISAN?", "What documents are required?"]
    elif "insurance" in text or "pmfby" in text:
        return ["How do I check my claim status?", "What are the premium rates?"]
    else:
        return ["What are the eligibility criteria?", "Are there any subsidies for this?"]

# Show relevant follow-ups if the last message was from the assistant
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    last_msg = st.session_state.messages[-1]["content"]
    suggestions = get_dynamic_suggestions(last_msg)
    
    st.markdown("**Suggested Follow-ups:**")
    cols = st.columns(len(suggestions))
    
    for i, suggestion in enumerate(suggestions):
        if cols[i].button(suggestion, key=f"sugg_{len(st.session_state.messages)}_{i}"):
            st.session_state.trigger_prompt = suggestion
            st.rerun()

# Initial suggested prompts if chat is empty
elif not st.session_state.messages:
    st.markdown("**Suggested Queries:**")
    cols = st.columns(3)
    if cols[0].button("PM-KISAN Eligibility"):
        st.session_state.trigger_prompt = "What are the eligibility criteria for PM-KISAN?"
        st.rerun()
    if cols[1].button("Organic Farming Subsidies"):
        st.session_state.trigger_prompt = "Are there any subsidies for organic farming?"
        st.rerun()
    if cols[2].button("Crop Insurance"):
        st.session_state.trigger_prompt = "How do I claim crop insurance under PMFBY?"
        st.rerun()

# Chat Input Handling
prompt = st.chat_input("E.g., What are the eligibility criteria for PM-KISAN?")

# Intercept prompt if a dynamic/suggested button was clicked
if "trigger_prompt" in st.session_state:
    prompt = st.session_state.trigger_prompt
    del st.session_state.trigger_prompt

if prompt:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call Backend API
    with st.chat_message("assistant"):
        with st.spinner("Searching vector database..."):
            payload = {
                "question": prompt,
                "chat_history": st.session_state.chat_history,
                "language": st.session_state.selected_lang
            }
            try:
                res = requests.post(f"{API_URL}/chat", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    answer = data.get("answer", "No answer found.")
                    sources = data.get("sources", [])  
                    trace_id = data.get("trace_id", "N/A") 
                    
                    def stream_text(text):
                        for word in text.split(" "):
                            yield word + " "
                            time.sleep(0.03)
                            
                    st.write_stream(stream_text(answer))
                    
                    if st.session_state.observability and trace_id != "N/A":
                        st.caption(f"🔧 LangSmith Trace ID: `{trace_id}`")
                        
                    if sources:
                        with st.expander("🔍 View Source Documents"):
                            for source in sources:
                                st.info(source)[cite: 2]
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer,
                        "sources": sources,
                        "trace_id": trace_id
                    })
                    st.session_state.chat_history.append([prompt, answer])
                    
                    st.rerun()
                else:
                    error_msg = res.json().get("detail", "Error querying the database.")
                    st.error(f"⚠️ {error_msg}")
            except Exception as e:
                st.error("⚠️ Failed to connect to the API. Ensure FastAPI is running.")[cite: 2]