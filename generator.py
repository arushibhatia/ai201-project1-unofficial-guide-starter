"""Grounded answer generation for the Duke CS syllabus guide.

Ttake the chunks returned by retrieve() and ask the LLM
(llama-3.3-70b-versatile via Groq) to answer the question using ONLY that
retrieved context — never its own training knowledge — and to attribute the
answer to the source syllabus it came from.
"""

from groq import Groq

from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """Generate a grounded answer from retrieved syllabus chunks.

    `retrieved_chunks` is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "course"   : the course code, e.g. "CS201"
      - "source"   : the source document filename, e.g. "CS201.txt"
      - "position" : the chunk's position within its document
      - "distance" : cosine distance (lower = more similar)

    Grounding comes from the system prompt, which forbids using outside/training
    knowledge and tells the model to say so when the context doesn't contain the
    answer. Source attribution is handled separately by sources_from_chunks(),
    which derives the source list from the retrieved chunks themselves so it
    can't be hallucinated.

    Returns the model's answer as a plain string (no source list appended).
    """
    if not retrieved_chunks:
        return (
            "I don't have enough information on that. I couldn't find anything "
            "relevant in the loaded syllabi — try rephrasing your question, or "
            "the topic may not be covered by the documents in this system."
        )

    # Build a numbered context block, labeling each chunk with its course/source
    # so the model can ground specific claims to specific syllabi.
    context_blocks = []
    for i, chunk in enumerate(retrieved_chunks, start=1):
        context_blocks.append(
            f"Chunk {i}\n"
            f"Course: {chunk.get('course', 'Unknown')}\n"
            f"Source: {chunk.get('source', 'Unknown')}\n"
            f"Text: {chunk.get('text', '')}"
        )
    context_text = "\n\n---\n\n".join(context_blocks)

    system_prompt = (
        "You are an assistant that answers questions about Duke University "
        "computer science course syllabi. Answer using ONLY the syllabus text "
        "provided in the context below. "
        "If the provided context does not contain enough information to answer, "
        "respond exactly with: 'I don't have enough information on that.' "
        "Do not use outside or prior knowledge, and do not guess or fill in "
        "gaps from what you may know about Duke courses. "
        "When you do answer, make clear which course each part of the answer "
        "comes from by citing the source syllabus in parentheses with its .txt "
        "filename, for example (Source: CS201.txt)."
    )

    user_prompt = (
        "Retrieved syllabus context:\n"
        f"{context_text}\n\n"
        "Question:\n"
        f"{query}"
    )

    completion = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,  # deterministic, reduces drift away from the context
    )

    return completion.choices[0].message.content or ""


def sources_from_chunks(retrieved_chunks):
    """Return the unique source filenames behind a set of retrieved chunks.

    The course code doubles as the filename, so the source is course + ".txt".
    Order is preserved (already sorted best-match-first by retrieve()).
    """
    sources = []
    for chunk in retrieved_chunks:
        source = f"{chunk.get('course', 'Unknown')}.txt"
        if source not in sources:
            sources.append(source)
    return sources


if __name__ == "__main__":
    # End-to-end smoke test: retrieve, then generate a grounded answer.
    from embed_and_retrieve import retrieve

    question = "What are the prerequisites for CS 330?"
    print(f"Question: {question}\n")
    chunks = retrieve(question)
    print("\n" + "=" * 70)
    print(generate_response(question, chunks))
    print("\nSources retrieved:")
    for source in sources_from_chunks(chunks):
        print(f"- {source}")
