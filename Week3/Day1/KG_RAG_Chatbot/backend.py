import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain

load_dotenv()

app = FastAPI(title="TN Government Schemes KG-RAG API")

graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)
graph.refresh_schema()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

CYPHER_GENERATION_TEMPLATE = """Task: Generate a Cypher statement to query a Neo4j graph database.
Instructions:
- Use only the provided relationship types and properties in the schema.
- ALWAYS use case-insensitive partial matching with `toLower(...) CONTAINS '...'` when filtering by keywords.
- Search across `d.text` (the full scheme text on `:Document` nodes) AND node `id` / `description` properties so broad topic questions match relevant schemes.
- Return specific text/properties (such as `s.id`, `d.text`, `b.id`) rather than raw nodes.
- Do not include any explanations or markdown—output ONLY the Cypher query.

Schema:
{schema}

Example:
Question: explain about crop cultivation
Cypher:
MATCH (d:Document)-[:MENTIONS]->(s:Scheme)
WHERE toLower(d.text) CONTAINS 'crop' OR toLower(d.text) CONTAINS 'cultivation' OR toLower(s.id) CONTAINS 'crop'
RETURN DISTINCT s.id AS scheme, d.text AS details
LIMIT 10

The question is:
{question}"""

cypher_prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template=CYPHER_GENERATION_TEMPLATE,
)

qa_chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    cypher_prompt=cypher_prompt,
    top_k=15,
    verbose=True,
    return_intermediate_steps=True,
    allow_dangerous_requests=True,
)


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    cypher_query: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    try:
        result = qa_chain.invoke({"query": request.question})
        intermediate = result.get("intermediate_steps", [])
        cypher = intermediate[0].get("query", "") if intermediate else ""

        return QueryResponse(
            answer=result.get("result", "No answer generated."),
            cypher_query=cypher,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))