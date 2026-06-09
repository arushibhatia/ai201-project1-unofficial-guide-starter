"""Embedding, vector storage, and retrieval for the Duke CS syllabus guide.

Milestone 4: embed each chunk with all-MiniLM-L6-v2, store the vectors in a
persistent ChromaDB collection, and run semantic search over them.
"""

import chromadb
from chromadb.utils import embedding_functions

from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL, N_RESULTS

# Embedding function and ChromaDB client are initialized once at module load.
# sentence-transformers downloads the model on first use — this may take
# 30–60 seconds the very first time. Subsequent runs use a local cache.
_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)
_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=_ef,
    metadata={"hnsw:space": "cosine"},
)


def get_collection():
    """Return the ChromaDB collection. Used during ingestion."""
    return _collection


def reset_collection():
    """Drop and recreate the collection so a fresh ingestion starts empty.

    Useful when re-ingesting with a different chunking strategy or chunk size:
    the old vectors would otherwise persist (and their chunk_ids would collide
    with the new ones on add()).
    """
    global _collection
    try:
        _client.delete_collection(CHROMA_COLLECTION)
    except Exception:
        # Collection may not exist yet on a first run — that's fine.
        pass
    _collection = _client.get_or_create_collection(
        name=CHROMA_COLLECTION,
        embedding_function=_ef,
        metadata={"hnsw:space": "cosine"},
    )
    return _collection


def embed_and_store(chunks):
    """Embed a list of chunks and store them in the vector database.

    _collection.add() takes three parallel lists built from the chunks
    returned by chunk_document():
      - documents : raw text strings — ChromaDB's embedding function converts
                    these to vectors automatically using sentence-transformers
      - metadatas : one dict per chunk, stored alongside the vector. We keep
                    the course, the source document filename, and the chunk's
                    position within that document so retrieve() can surface
                    where a result came from for attribution later.
      - ids       : the unique chunk_id strings used to identify each entry

    Embeddings are not generated manually here — we hand over the text and
    ChromaDB handles the vector math via the embedding function.
    """
    if not chunks:
        print("No chunks to store.")
        return

    _collection.add(
        documents=[c["text"] for c in chunks],
        metadatas=[
            {
                "course": c["course"],
                "source": c["source"],
                "position": c["position"],
            }
            for c in chunks
        ],
        ids=[c["chunk_id"] for c in chunks],
    )
    print(f"Stored {_collection.count()} total chunks in the vector database.")


def retrieve(query, n_results=N_RESULTS):
    """Find the most relevant syllabus chunks for a user's question.

    Runs a semantic search via _collection.query() and returns a list of dicts,
    each with:
      - "text"     : the chunk text
      - "course"   : the course code (pulled from metadata)
      - "source"   : the source document filename (for attribution)
      - "position" : the chunk's position within its document
      - "distance" : cosine distance (lower = more similar)
    """
    if _collection.count() == 0:
        print("Vector database is empty — run ingestion first.")
        return []

    results = _collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    # Chroma returns one list per query text. We only send one query, so [0].
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    retrieved = []
    for text, metadata, distance in zip(documents, metadatas, distances):
        retrieved.append({
            "text": text,
            "course": metadata.get("course", "Unknown"),
            "source": metadata.get("source", "Unknown"),
            "position": metadata.get("position", -1),
            "distance": float(distance),
        })

    # Lower cosine distance means a better match.
    retrieved.sort(key=lambda item: item["distance"])

    for chunk in retrieved:
        print(f"[{chunk['source']}#{chunk['position']}] "
              f"(dist: {chunk['distance']:.3f}) {chunk['text'][:80]}...")

    return retrieved


if __name__ == "__main__":
    # Ingest all chunks, then run a sample query. The chunking strategy can be
    # chosen at runtime, e.g.:
    #   python embed_and_retrieve.py paragraph
    #   python embed_and_retrieve.py character   (default)
    import sys

    from config import CHUNK_STRATEGY
    from chunking import chunk_all_documents

    strategy = sys.argv[1] if len(sys.argv) > 1 else CHUNK_STRATEGY

    print(f"Ingesting chunks into ChromaDB using '{strategy}' chunking...")
    reset_collection()  # start fresh so a strategy switch doesn't mix old chunks
    embed_and_store(chunk_all_documents(strategy=strategy))

    print("\nSample query: 'Does CS 201 allow you to retake exams?'")
    print("-" * 60)
    retrieve("Does CS 201 allow you to retake exams?")
