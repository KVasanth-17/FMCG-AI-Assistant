import streamlit as st
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# 1. Page Configuration
st.set_page_config(page_title="FMCG AI Assistant", layout="wide")
st.title("📊 FMCG AI Assistant")

# 2. Access your API key securely from Streamlit Secrets
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("API Key not found. Please set it in Streamlit Cloud Secrets.")
    st.stop()

# 3. Load your data
@st.cache_data
def load_data():
    df_sales = pd.read_csv("sales_and_promotions.csv") 
    df_inventory = pd.read_csv("inventory.csv")
    return df_sales, df_inventory

# Load the data
df_sales, df_inventory = load_data()

# 4. Initialize the LLM and Agent
# Updated to gemini-3.5-flash (the current stable model for June 2026)
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", google_api_key=api_key)

# Added allow_dangerous_code=True for agent initialization
agent = create_pandas_dataframe_agent(
    llm, 
    [df_sales, df_inventory], 
    verbose=True,
    max_iterations=4,           
    handle_parsing_errors=True,
    allow_dangerous_code=True  
)

# 5. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask a question about your data..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # The agent processes the prompt
            response = agent.invoke(prompt)
            st.markdown(response['output'])
            st.session_state.messages.append({"role": "assistant", "content": response['output']})
        except Exception as e:
            st.error(f"An error occurred: {e}")
