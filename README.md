# 🚀 Startup Finance Copilot

**Empowering startups with AI-driven financial planning and pitch deck generation**

---

## 📌 Overview

Startup Finance Copilot is an AI-powered platform designed to help startups and small businesses with financial forecasting, risk analysis, funding search, and automatic pitch deck creation. It leverages multiple AI agents working together, using advanced language models through OpenRouter and Langchain for retrieval-augmented generation (RAG).

---

## ✨ Key Features

- **🔢 Financial Projection Agent:** Transforms Excel financial data into detailed revenue forecasts, budget breakdowns, and KPIs.
- **💰 EU Funding Agent:** Identifies relevant EU or national grant programs based on your startup's mission, industry, and location.
- **⚠️ Risk Advisor Agent:** Analyzes potential business risks and offers strategic mitigation recommendations.
- **🧾 Pitch Deck Agent:** Synthesizes startup data into a compelling, investor-ready pitch deck with minimal user input.
- **🧠 RAG Workflow:** Uses Langchain and ChromaDB for semantic search and retrieval of startup documents.

---

## Architecture

The system follows a modular architecture:

- **Data ingestion:** Text files containing startup information are vectorized into embeddings stored in ChromaDB.
- **Retrieval:** Langchain’s retriever fetches relevant document chunks.
- **Agent orchestration:** Agents (financial, funding, risk) process specific tasks independently.
- **Generation:** The Pitch Deck Agent synthesizes all info into a coherent pitch deck using an LLM accessed via OpenRouter.

---

## Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/yourusername/startup-finance-copilot.git
   cd startup-finance-copilot

2. Create a virtual environment and activate it:
    python -m venv .venv
    source .venv/bin/activate   # On Windows: .venv\Scripts\activate

3. Install dependencies:
    pip install -r requirements.txt

4.  Set up environment variables:
    Create a .env file in the root directory with:

    OPENROUTER_API_KEY=your_openrouter_api_key
