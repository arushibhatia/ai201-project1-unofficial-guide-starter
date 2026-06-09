"""Document ingestion and chunking for the Duke CS syllabus guide.

Milestone 3: load the cleaned .txt syllabi from documents/ and split each one
into overlapping character windows ready for embedding.
"""

import os

from config import DOCS_PATH, CHUNK_SIZE, CHUNK_OVERLAP, CHUNK_MIN_LENGTH


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


def chunk_document(text, course, source):
    """Split one syllabus into chunks ready for embedding.

    Strategy: character-based sliding window with overlap (per planning.md).
      - chunk_size = CHUNK_SIZE characters: long enough to keep a grading-policy
        chart or exam-retake rule together in a single chunk rather than
        splitting it across a boundary.
      - overlap = CHUNK_OVERLAP characters: duplicates ~2-3 sentences at each
        boundary so a rule that spans two chunks is still retrievable intact.
      - min_length = CHUNK_MIN_LENGTH characters: filters whitespace artifacts
        and tiny trailing fragments that add noise without useful content.

    Returns a list of dicts, each with:
      - "text"     : the chunk text (str)
      - "course"   : the course code, e.g. "CS201" (str)
      - "source"   : the source document filename, e.g. "CS201.txt" (str)
      - "position" : the chunk's 0-based position within its document (int)
      - "chunk_id" : a unique identifier, e.g. "cs201_0", "cs201_1" (str)
    """
    chunk_size = CHUNK_SIZE
    overlap = CHUNK_OVERLAP
    min_length = CHUNK_MIN_LENGTH

    chunks = []
    prefix = course.lower().replace(" ", "_")
    counter = 0

    start = 0
    step = max(1, chunk_size - overlap)
    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end].strip()

        if len(chunk_text) >= min_length:
            chunks.append({
                "text": chunk_text,
                "course": course,
                "source": source,
                "position": counter,
                "chunk_id": f"{prefix}_{counter}",
            })
            counter += 1

        # Advance by (chunk_size - overlap) so the next window shares
        # `overlap` characters with the tail of this one.
        start += step

    return chunks


def chunk_all_documents():
    """Load every document and chunk it. Returns a flat list of chunk dicts."""
    documents = load_documents()
    all_chunks = []
    for doc in documents:
        doc_chunks = chunk_document(doc["text"], doc["course"], doc["filename"])
        print(f"  {doc['course']}: {len(doc_chunks)} chunks")
        all_chunks.extend(doc_chunks)
    print(f"Created {len(all_chunks)} chunks total across {len(documents)} document(s).")
    return all_chunks


if __name__ == "__main__":
    # Quick verification: chunk everything, report counts, show a sample.
    chunks = chunk_all_documents()
    print(f"\nChunk config -> size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP}, "
          f"min_length={CHUNK_MIN_LENGTH}")

    # Show a few example chunks as a sanity check.
    num_examples = 3
    for sample in chunks[:num_examples]:
        print(f"\nExample chunk [{sample['chunk_id']}] "
              f"from {sample['course']} ({len(sample['text'])} chars):")
        print("-" * 60)
        print(sample["text"][:500])
        print("-" * 60)
