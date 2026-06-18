import streamlit as st
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# 1. Page Configuration
st.set_page_config(page_title="FMCG AI Assistant", layout="wide")

# 2. Access your API key securely
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("API Key not found in Secrets.")
    st.stop()

# 3. Load your data
@st.cache_data
def load_data():
    df_sales = pd.read_csv("sales_and_promotions.csv") 
    df_inventory = pd.read_csv("inventory.csv")
    return df_sales, df_inventory

df_sales, df_inventory = load_data()

# 4. Initialize the LLM and Agent (Using stable 3.5-flash)
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", google_api_key=api_key)

agent = create_pandas_dataframe_agent(
    llm, 
    [df_sales, df_inventory], 
    verbose=True,
    max_iterations=4,           
    handle_parsing_errors=True,
    allow_dangerous_code=True  
)

# 5. UI Layout
with st.sidebar:
    st.header("💡 How to use")
    st.write("Ask me anything about your FMCG data!")
    st.info("• 'Show me the first 5 rows of sales data.'\n• 'Which product has the highest stock?'\n• 'What was the total revenue in the last month?'")

st.title("📊 FMCG AI Assistant")
st.write("---")

# Quick-start buttons
col1, col2, col3 = st.columns(3)
if col1.button("📉 View Sales Trends"):
    st.session_state.temp_prompt = "Summarize the sales trends from the sales_and_promotions data."
if col2.button("📦 Check Low Stock"):
    st.session_state.temp_prompt = "Identify items in the inventory with less than 50 units."
if col3.button("💰 Best Selling Product"):
    st.session_state.temp_prompt = "Which product in the sales data generated the highest revenue?"

# 6. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process input (from chat or button)
prompt = st.chat_input("Ask a question about your data...")

# Handle button click or chat input
final_prompt = None
if "temp_prompt" in st.session_state and st.session_state.temp_prompt:
    final_prompt = st.session_state.temp_prompt
    st.session_state.temp_prompt = None # Clear it
elif prompt:
    final_prompt = prompt

if final_prompt:
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with st.chat_message("user"):
        st.markdown(final_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing data..."):
            try:
                response = agent.invoke(final_prompt)
                st.markdown(response['output'])
                st.session_state.messages.append({"role": "assistant", "content": response['output']})
            except Exception as e:
                st.error(f"Error: {e}")
