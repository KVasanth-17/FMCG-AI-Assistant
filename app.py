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
    st.error("API Key not found in Streamlit Cloud Secrets.")
    st.stop()

# 3. Load your data
@st.cache_data
def load_data():
    df_sales = pd.read_csv("sales_and_promotions.csv") 
    df_inventory = pd.read_csv("inventory.csv")
    return df_sales, df_inventory

df_sales, df_inventory = load_data()

# 4. Initialize the LLM and Agent
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
    st.info("• 'Show me the first 5 rows of sales data.'\n• 'Which product has the highest stock?'\n• 'What was the total revenue in the last month?'")

st.title("📊 FMCG AI Assistant")

# --- KPI Metrics Section ---
col1, col2, col3 = st.columns(3)

# !!! REPLACE THESE WITH YOUR ACTUAL COLUMN NAMES !!!
# Example: If your column is 'Stock', use df_inventory['Stock']
# Example: If your column is 'Revenue', use df_sales['Revenue']
try:
    total_products = len(df_inventory)
    low_stock = len(df_inventory[df_inventory['YOUR_STOCK_COLUMN_NAME'] < 50])
    total_revenue = df_sales['YOUR_REVENUE_COLUMN_NAME'].sum()

    col1.metric("Total Products", total_products)
    col2.metric("Low Stock Items", low_stock)
    col3.metric("Total Revenue", f"${total_revenue:,.0f}")
except KeyError as e:
    st.error(f"Column name error: {e}. Please check your CSV column headers.")
    st.write("Current columns in Inventory:", df_inventory.columns.tolist())
    st.write("Current columns in Sales:", df_sales.columns.tolist())

st.write("---")

# Quick-start buttons
col1, col2, col3 = st.columns(3)
if col1.button("📉 View Sales Trends"):
    st.session_state.temp_prompt = "Summarize the sales trends from the data."
if col2.button("📦 Check Low Stock"):
    st.session_state.temp_prompt = "Identify items with low stock."
if col3.button("💰 Best Selling Product"):
    st.session_state.temp_prompt = "Which product generated the most revenue?"

# 6. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask a question about your data...")
final_prompt = None
if "temp_prompt" in st.session_state and st.session_state.temp_prompt:
    final_prompt = st.session_state.temp_prompt
    st.session_state.temp_prompt = None 
elif prompt:
    final_prompt = prompt

if final_prompt:
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with st.chat_message("user"):
        st.markdown(final_prompt)
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                response = agent.invoke(final_prompt)
                st.markdown(response['output'])
                st.session_state.messages.append({"role": "assistant", "content": response['output']})
            except Exception as e:
                st.error(f"Error: {e}")
