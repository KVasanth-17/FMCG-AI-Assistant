# FMCG AI Assistant Prototype 📊🤖

## Overview
This repository contains a prototype for a conversational AI assistant designed to query structured Fast-Moving Consumer Goods (FMCG) data. The goal of this project is to eliminate the bottleneck of relying on data analysts for ad-hoc reporting by allowing business stakeholders to ask natural language questions about sales, inventory, and promotions.

## Architecture & Tech Stack
* **Frontend:** Streamlit (Rapid Python-native UI deployment)
* **Orchestration:** LangChain (`create_pandas_dataframe_agent`)
* **LLM Engine:** Google Gemini-3.5-Flash
* **Data Layer:** In-memory Pandas DataFrames processing locally generated CSVs.

## Data Strategy
The dataset is entirely synthetic, generated via `generate_data.py`. It is specifically designed to model real-world FMCG edge cases, including:
* **Promotional Spikes:** When `promotion_flag` is true, sales volume randomly spikes.
* **Inventory Drawdowns & Stockouts:** Sales volume mathematically drains inventory. If demand exceeds supply, it triggers a `stockout_flag`.

## Repository Contents
* `app.py`: The main Streamlit application and LangChain agent logic.
* `generate_data.py`: The script used to synthesize the relational FMCG datasets.
* `requirements.txt`: Dependencies required for deployment.
* `*.csv`: The 4 core datasets (Sales & Promotions, Inventory, Product Master, Store Master).

## Known Constraints & Mitigations (Evaluator Note)
This prototype leverages a free-tier LLM API, making it susceptible to `503 Service Unavailable` and `429 Too Many Requests` errors during rapid sequential tool-calling. To mitigate infinite looping and excessive quota consumption during AST parsing, the LangChain agent is strictly constrained with `max_iterations=4` and `handle_parsing_errors=True`.
