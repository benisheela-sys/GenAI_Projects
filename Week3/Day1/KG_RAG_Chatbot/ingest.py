import json
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_neo4j import Neo4jGraph, LLMGraphTransformer

load_dotenv()


def build_knowledge_graph(json_path: str = "schemes_data.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        schemes = json.load(f)

    documents = [
        Document(
            page_content=item["content"][:4000],  # Trim overly long pages
            metadata={"title": item["title"], "source": item["url"]},
        )
        for item in schemes
    ]

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Constrain schema for higher Cypher generation accuracy
    transformer = LLMGraphTransformer(
        llm=llm,
        allowed_nodes=[
            "Scheme",
            "Department",
            "Beneficiary",
            "Benefit",
            "Eligibility",
            "Document",
        ],
        allowed_relationships=[
            "OFFERED_BY",
            "FOR_BENEFICIARY",
            "PROVIDES",
            "REQUIRES_ELIGIBILITY",
            "REQUIRES_DOCUMENT",
        ],
        node_properties=["description", "url"],
    )

    print(f"Extracting graph entities from {len(documents)} documents...")
    graph_documents = transformer.convert_to_graph_documents(documents)

    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
    )

    print("Loading graph documents into Neo4j...")
    graph.add_graph_documents(
        graph_documents,
        baseEntityLabel=True,
        include_source=True,
    )

    graph.refresh_schema()
    print("Knowledge Graph ingestion complete!")
    print("Current Schema:\n", graph.schema)


if __name__ == "__main__":
    build_knowledge_graph()