"""Run the 5 evaluation questions from planning.md through retrieval.

Inspect which chunks come back for each question to judge retrieval quality.
Assumes the vector store is already populated (run embed_and_retrieve.py first).
"""

from embed_and_retrieve import retrieve

# The 5 test questions from planning.md → Evaluation Plan.
TEST_QUESTIONS = [
    "Which courses allow you to use AI?",
    "Does CS 201 allow you to retake exams?",
    "What percentage does discussion account for in CS201?",
    "What are the prerequisites for CS 330?",
    "Should I take CS 201 before CS 101?",
]

if __name__ == "__main__":
    for i, question in enumerate(TEST_QUESTIONS, start=1):
        print(f"\n{'=' * 70}")
        print(f"Q{i}: {question}")
        print("=" * 70)
        retrieve(question)
