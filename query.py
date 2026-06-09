"""End-to-end query entry point: retrieve → generate → attribute.

`ask()` is the single function the interface (app.py) calls. It optionally
re-ingests the corpus under a chosen chunking strategy, retrieves the most
relevant chunks, generates a grounded answer, and returns the answer together
with the source documents it was drawn from.
"""

from chunking import chunk_all_documents
from config import CHUNK_STRATEGY
from embed_and_retrieve import embed_and_store, get_collection, retrieve, reset_collection
from generator import generate_response, sources_from_chunks

# Tracks which chunking strategy the vector store currently holds, so we only
# re-ingest when the caller asks for a different one. None means "unknown /
# whatever is already persisted on disk" — we don't touch it unless asked.
_loaded_strategy = None


def ingest(strategy=CHUNK_STRATEGY):
    """Wipe the vector store and re-ingest the corpus using `strategy`."""
    global _loaded_strategy
    print(f"Ingesting corpus with '{strategy}' chunking...")
    reset_collection()
    embed_and_store(chunk_all_documents(strategy=strategy))
    _loaded_strategy = strategy


def ask(question, strategy=None):
    """Answer a question against the syllabus corpus.

    Args:
      question : the user's question (str)
      strategy : optional chunking strategy ("character" or "paragraph"). If
                 given and different from what's currently loaded, the corpus is
                 re-ingested under that strategy first. If None, whatever is
                 already in the store is used.

    Returns a dict:
      - "answer"  : the grounded answer text (str)
      - "sources" : list of source filenames the answer was drawn from (list[str])
    """
    if strategy and strategy != _loaded_strategy:
        ingest(strategy)
    elif get_collection().count() == 0:
        # Empty store (e.g. first run) — ingest with the configured default.
        ingest(CHUNK_STRATEGY)

    chunks = retrieve(question)
    return {
        "answer": generate_response(question, chunks),
        "sources": sources_from_chunks(chunks),
    }


if __name__ == "__main__":
    result = ask("What are the prerequisites for CS 330?")
    print("\nAnswer:\n" + result["answer"])
    print("\nSources:\n" + "\n".join(f"- {s}" for s in result["sources"]))