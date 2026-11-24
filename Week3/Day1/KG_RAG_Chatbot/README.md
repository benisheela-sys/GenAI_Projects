# Tamil Nadu Government Schemes KG-RAG Assistant

An end-to-end **Knowledge Graph Retrieval-Augmented Generation (KG-RAG)** chatbot that scrapes Tamil Nadu Government scheme details from `tn.gov.in`, models them as a structured **Neo4j Knowledge Graph**, and answers natural-language questions through a **FastAPI** backend and **Streamlit** chat interface.

---

## Architecture Overview

```text
tn.gov.in (Scheme Portal)
        │
        ▼
  scraper.py (Requests + BeautifulSoup4)
        │  Saves structured text to schemes_data.json
        ▼
  ingest.py (LangChain LLMGraphTransformer + GPT-4o-mini)
        │  Extracts entities & relationships
        ▼
  Neo4j Knowledge Graph (AuraDB / Neo4j Desktop)
        │
        ▼
  backend.py (FastAPI + GraphCypherQAChain)
        │  Converts natural language → Cypher → grounded answer
        ▼
  app.py (Streamlit Chat UI)