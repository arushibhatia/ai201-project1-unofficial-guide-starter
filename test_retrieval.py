"""Run the 5 evaluation questions from planning.md through retrieval.

Inspect which chunks come back for each question to judge retrieval quality.
Assumes the vector store is already populated (run embed_and_retrieve.py first).
"""

from embed_and_retrieve import retrieve

# The 5 test questions from planning.md → Evaluation Plan.
TEST_QUESTIONS = [
    "How is the final exam administered in CS230?",
    "How much is Exam 3 worth in CS116?",
    "How is CS216 structured?",
    "What is the late submission penalty for projects in CS201?",
    "Should I take CS 201 before CS 101?",
]

if __name__ == "__main__":
    for i, question in enumerate(TEST_QUESTIONS, start=1):
        print(f"\n{'=' * 70}")
        print(f"Q{i}: {question}")
        print("=" * 70)
        retrieve(question)
