import streamlit as st
import requests
import pandas as pd

# --- CONFIGURATION (Loaded from secrets) ---
try:
    JETSON_IP = st.secrets["JETSON_IP"]
    FLOW_ID = st.secrets["FLOW_ID"]
    API_KEY = st.secrets["API_KEY"]
except FileNotFoundError:
    st.error("Secrets file not found. Please configure .streamlit/secrets.toml")
    st.stop()

BASE_API_URL = f"http://{JETSON_IP}:7860/api/v1/run/{FLOW_ID}"
CSV_FILE_PATH = "data/temp_file.csv"

st.set_page_config(page_title="Wood Quality Dashboard", page_icon="🪵", layout="wide")

# --- CUSTOM CSS FOR CHAT BUBBLES ---
st.markdown("""
<style>
    .user-bubble { background-color: #e0f7fa; color: #006064; padding: 10px; border-radius: 10px; margin-bottom: 10px; }
    .agent-bubble { background-color: #f1f8e9; color: #33691e; padding: 10px; border-radius: 10px; margin-bottom: 10px; }
    .stDataFrame { border: 1px solid #ccc; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

st.title("🪵 Wood Quality Control Center")
st.markdown("**Hardware:** Jetson Orin Nano (8GB) | **Model:** Granite-1B")

# --- LAYOUT: SPLIT INTO TWO COLUMNS ---
col1, col2 = st.columns([1, 1])

# --- COLUMN 1: RAW DATASET ---
with col1:
    st.subheader("📊 Live Scanner Data")
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        # Highlight high severity rows in the table
        def highlight_high(s):
            return ['background-color: #ffcccc' if v == 'High' else '' for v in s]
        
        st.dataframe(df.style.apply(highlight_high, subset=['Severity']), height=600, use_container_width=True)
        st.info(f"Showing {len(df)} recent scans from `{CSV_FILE_PATH}`")
    except Exception as e:
        st.error(f"Could not load CSV: {e}")

# --- COLUMN 2: AI ASSISTANT ---
with col2:
    st.subheader("🤖 Defect Analyst")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_container = st.container(height=500)
    
    with chat_container:
        for message in st.session_state.messages:
            role_class = "user-bubble" if message["role"] == "user" else "agent-bubble"
            st.markdown(f"<div class='{role_class}'><b>{'👤 You' if message['role'] == 'user' else '🤖 Agent'}:</b><br>{message['content']}</div>", unsafe_allow_html=True)

    if prompt := st.chat_input("Ask about knots, splits, or scanner confidence..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("Jetson is analyzing..."):
            try:
                payload = {"input_value": prompt, "output_type": "chat", "input_type": "chat"}
                headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
                
                response = requests.post(BASE_API_URL, json=payload, headers=headers)
                response.raise_for_status()
                result = response.json()
                
                try:
                    answer = result['outputs'][0]['outputs'][0]['results']['message']['text']
                except:
                    answer = "Error extracting response. Check Langflow logs."
                
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.rerun()

            except Exception as e:
                st.error(f"Connection Error: {e}")