import streamlit as st
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# --- UI Setup ---
st.set_page_config(page_title="FMCG AI Assistant", layout="wide")
st.title("Beverages Category: AI Assistant")
st.markdown("Ask natural language questions about promotions, inventory, and sales.")

# --- API Key Input ---
api_key = st.sidebar.text_input("Enter Google Gemini API Key", type="password")
st.sidebar.markdown("*(Get a free key from Google AI Studio)*")

# --- Load the Datasets ---
@st.cache_data
def load_data():
    sales = pd.read_csv("sales_and_promotions.csv")
    inventory = pd.read_csv("inventory.csv")
    products = pd.read_csv("product_master.csv")
    stores = pd.read_csv("store_master.csv")
    return sales, inventory, products, stores

try:
    df_sales, df_inventory, df_products, df_stores = load_data()
    st.sidebar.success("✅ 4 Datasets Loaded Successfully")
except Exception as e:
    st.error(f"Error loading data: {e}. Make sure the CSVs are in the same folder as this script.")
    st.stop()

# --- User Interaction ---
user_question = st.text_input("What would you like to know?", placeholder="e.g., Which product had the highest revenue during a promotion?")

if st.button("Analyze Data") and user_question:
    if not api_key:
        st.warning("Please enter your Gemini API Key in the sidebar first.")
    else:
        with st.spinner("The AI is analyzing the datasets. Please wait..."):
            try:
                # Initialize the LLM - UPDATED TO CURRENT GEMINI MODEL
                llm = ChatGoogleGenerativeAI(
                    model="gemini-3.5-flash", 
                    google_api_key=api_key, 
                    temperature=0
                )

                # Create the Data Agent (Passing all 4 tables)
                agent = create_pandas_dataframe_agent(
                    llm,
                    [df_sales, df_inventory, df_products, df_stores],
                    verbose=True,
                    allow_dangerous_code=True # Required by LangChain to run pandas queries
                )

                # Execute the query
                response = agent.invoke(user_question)
                
                st.success("Analysis Complete")
                st.info(response["output"])
                
            except Exception as e:
                st.error("An error occurred during analysis.")
                st.code(str(e))
                st.markdown("**Debugging Note:** The LLM occasionally writes invalid pandas code. Try rephrasing your question to be more specific.")