"""Document ingestion and chunking for the Duke CS syllabus guide.

Loads the cleaned .txt syllabi from documents/ and splits each one into chunks
ready for embedding. Two strategies are selectable at runtime:

  - "character" : fixed-size sliding window with overlap (CHUNK_SIZE /
                  CHUNK_OVERLAP). Predictable size; may split a rule or table
                  across a boundary.
  - "paragraph" : split on blank lines; each paragraph is its own chunk with no
                  size cap. Respects the document's natural structure so a rule
                  stated in one paragraph stays intact, at the cost of uneven
                  chunk sizes.
"""

import os
import re

from config import (
    DOCS_PATH,
    CHUNK_STRATEGY,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    CHUNK_MIN_LENGTH,
)

# Strategies the chunker understands. "window" is accepted as an alias for
# "character" so either name works at the command line.
VALID_STRATEGIES = ("character", "window", "paragraph")


def load_documents():
    """Load all .txt syllabus documents from the documents/ folder.

    Returns a list of dicts, each with:
      - "course"   : course code derived from the filename, e.g. "CS201" (str)
      - "filename" : the source file name (str)
      - "text"     : the full document text (str)
    """
    documents = []
    for filename in sorted(os.listdir(DOCS_PATH)):
        if not filename.endswith(".txt"):
            continue
        filepath = os.path.join(DOCS_PATH, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        course = filename.replace(".txt", "")
        documents.append({
            "course": course,
            "filename": filename,
            "text": text,
        })
    print(f"Loaded {len(documents)} syllabus document(s): "
          f"{[d['course'] for d in documents]}")
    return documents


def _window_texts(text):
    """Character-based sliding window: list of chunk strings.

    Steps through the text in CHUNK_SIZE windows, advancing by
    (CHUNK_SIZE - CHUNK_OVERLAP) so adjacent chunks share `overlap` chars.
    Chunks shorter than CHUNK_MIN_LENGTH (e.g. the trailing fragment) are
    dropped as noise.
    """
    texts = []
    step = max(1, CHUNK_SIZE - CHUNK_OVERLAP)
    start = 0
    while start < len(text):
        chunk = text[start:start + CHUNK_SIZE].strip()
        if len(chunk) >= CHUNK_MIN_LENGTH:
            texts.append(chunk)
        start += step
    return texts


def _paragraph_texts(text):
    """Paragraph-based chunking: list of chunk strings.

    Splits on blank lines and treats each paragraph as its own chunk, no matter
    how long it is — there is no size cap and no packing. This respects the
    document's natural structure, so a rule (or a whole table) written as one
    paragraph stays intact in a single chunk, at the cost of uneven chunk
    sizes. Paragraphs shorter than CHUNK_MIN_LENGTH are dropped as noise.
    """
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return [p for p in paragraphs if len(p) >= CHUNK_MIN_LENGTH]


def chunk_document(text, course, source, strategy=CHUNK_STRATEGY):
    """Split one syllabus into chunks ready for embedding.

    `strategy` selects how the text is split:
      - "character" (or "window") : fixed-size sliding window with overlap
      - "paragraph"               : one chunk per blank-line paragraph, no cap

    Returns a list of dicts, each with:
      - "text"     : the chunk text (str)
      - "course"   : the course code, e.g. "CS201" (str)
      - "source"   : the source document filename, e.g. "CS201.txt" (str)
      - "position" : the chunk's 0-based position within its document (int)
      - "chunk_id" : a unique identifier, e.g. "cs201_0", "cs201_1" (str)
    """
    if strategy not in VALID_STRATEGIES:
        raise ValueError(
            f"Unknown chunking strategy {strategy!r}. "
            f"Choose one of: {', '.join(VALID_STRATEGIES)}."
        )

    if strategy == "paragraph":
        texts = _paragraph_texts(text)
    else:  # "character" or "window"
        texts = _window_texts(text)

    prefix = course.lower().replace(" ", "_")
    return [
        {
            "text": chunk_text,
            "course": course,
            "source": source,
            "position": i,
            "chunk_id": f"{prefix}_{i}",
        }
        for i, chunk_text in enumerate(texts)
    ]


def chunk_all_documents(strategy=CHUNK_STRATEGY):
    """Load every document and chunk it with `strategy`.

    Returns a flat list of chunk dicts.
    """
    documents = load_documents()
    print(f"Chunking with '{strategy}' strategy.")
    all_chunks = []
    for doc in documents:
        doc_chunks = chunk_document(doc["text"], doc["course"], doc["filename"],
                                    strategy=strategy)
        print(f"  {doc['course']}: {len(doc_chunks)} chunks")
        all_chunks.extend(doc_chunks)
    print(f"Created {len(all_chunks)} chunks total across {len(documents)} document(s).")
    return all_chunks


if __name__ == "__main__":
    import sys

    # Strategy can be passed as a CLI arg, e.g. `python chunking.py paragraph`.
    strategy = sys.argv[1] if len(sys.argv) > 1 else CHUNK_STRATEGY

    chunks = chunk_all_documents(strategy=strategy)
    print(f"\nChunk config -> strategy={strategy}, size={CHUNK_SIZE}, "
          f"overlap={CHUNK_OVERLAP}, min_length={CHUNK_MIN_LENGTH}")

    # Show a few example chunks as a sanity check.
    num_examples = 3
    for sample in chunks[:num_examples]:
        print(f"\nExample chunk [{sample['chunk_id']}] "
              f"from {sample['course']} ({len(sample['text'])} chars):")
        print("-" * 60)
        print(sample["text"][:500])
        print("-" * 60)
