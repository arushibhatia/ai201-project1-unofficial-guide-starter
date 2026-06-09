"""Central configuration for the Unofficial Guide RAG pipeline.

Values here are pulled from planning.md so the rest of the pipeline can import
them in one place. The chunking constants come directly from the Chunking
Strategy section: a 900-character sliding window with 150 characters of
overlap, sized to keep grading-policy tables and multi-sentence rules intact.
"""

import os

# --- Paths ---------------------------------------------------------------
# Folder holding the cleaned .txt syllabus documents.
DOCS_PATH = os.path.join(os.path.dirname(__file__), "documents")

# --- Chunking (planning.md → Chunking Strategy) --------------------------
# Character-based sliding window.
CHUNK_SIZE = 500       # chars per chunk: fits grading charts / retake policies
CHUNK_OVERLAP = 150    # chars shared at each boundary: ~2-3 sentences of context
CHUNK_MIN_LENGTH = 50  # drop whitespace artifacts / tiny trailing fragments

# --- Embedding + Vector Store (planning.md → Retrieval Approach) ----------
EMBEDDING_MODEL = "all-MiniLM-L6-v2"          # sentence-transformers model
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")  # persistent store
CHROMA_COLLECTION = "syllabi"                 # collection name in ChromaDB

# --- Retrieval -----------------------------------------------------------
N_RESULTS = 6          # top-k chunks returned per query
