import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = os.path.join("output", "chromadb_store")
COLLECTION_NAME = "chapter_versions"

# Use HuggingFace sentence-transformer for local embeddings (no API key needed)
hf_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

def get_chroma_client():
    return chromadb.Client(Settings(persist_directory=CHROMA_PATH))

def add_version(version_number, content, author="AI", editor=None, timestamp=None, embedding_func=hf_ef):
    client = get_chroma_client()
    collection = client.get_or_create_collection(COLLECTION_NAME, embedding_function=embedding_func)
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    metadata = {
        "version": version_number,
        "author": author,
        "timestamp": timestamp
    }
    if editor is not None:
        metadata["editor"] = editor
    doc_id = f"version_{version_number}"
    collection.add(
        documents=[content],
        metadatas=[metadata],
        ids=[doc_id]
    )
    # client.persist()  # Not needed or not available in current ChromaDB version
    print(f"Version {version_number} stored in ChromaDB.")

def semantic_search(query, n_results=3, embedding_func=hf_ef):
    client = get_chroma_client()
    collection = client.get_or_create_collection(COLLECTION_NAME, embedding_function=embedding_func)
    results = collection.query(query_texts=[query], n_results=n_results)
    for i, doc in enumerate(results['documents'][0]):
        meta = results['metadatas'][0][i]
        print(f"Match {i+1}: Version {meta['version']} by {meta['author']} at {meta['timestamp']}\nContent: {doc[:200]}...\n")
    return results

if __name__ == "__main__":
    # Example usage
    add_version(1, "This is a dream sequence in the story.", author="AI", editor="Human")
    add_version(2, "The protagonist wakes up from a dream.", author="AI", editor="Human")
    print("\nSemantic search for 'dream sequence':")
    semantic_search("dream sequence")
