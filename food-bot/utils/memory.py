import os
from langchain_community.vectorstores import Pinecone as PineconeStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX")

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=os.getenv("PINECONE_ENV"))
    )

def get_memory():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return PineconeStore(index=pc.Index(index_name), embedding=embeddings)
