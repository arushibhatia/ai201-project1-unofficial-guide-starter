"""Compare chunking strategies by ANSWER QUALITY on the same query set.

For each strategy ("character" and "paragraph"), re-ingest the corpus and run
the full pipeline (retrieve -> generate) for every evaluation question plus the
documented CS330 failure case. We print the actual grounded answer produced
under each strategy so they can be compared side by side on response quality,
not just on which document was retrieved.
"""

from chunking import chunk_all_documents
from embed_and_retrieve import embed_and_store, reset_collection, retrieve
from generator import generate_response

# (question, expected answer) pairs. The first five are the evaluation
# questions; the last is the documented failure case.
QUESTIONS = [
    ("How is the final exam administered in CS230?",
     "Online, take-home, open-book/open-notes; released 12:01am, due 11:59pm ET, ~3 hrs untimed within a 24-hour window."),
    ("How much is Exam 3 worth in CS116?",
     "18% of the final grade."),
    ("How is CS216 structured?",
     "Hybrid, Flipped, and Just-in-Time."),
    ("What is the late submission penalty for projects in CS201?",
     "<=24 hrs late: no penalty; after that 10% per day."),
    ("Should I take CS 201 before CS 101?",
     "No - CS101 is a prerequisite for CS201."),
    ("What are the prerequisites for CS 330?",
     "CompSci 201 and CompSci 230 (or equivalent)."),
]

STRATEGIES = ["character", "paragraph"]


def run_strategy(strategy):
    reset_collection()
    embed_and_store(chunk_all_documents(strategy=strategy))
    answers = []
    for question, expected in QUESTIONS:
        chunks = retrieve(question)
        answer = generate_response(question, chunks)
        answers.append((question, expected, answer))
    return answers


def main():
    results = {s: run_strategy(s) for s in STRATEGIES}

    print("\n\n" + "=" * 72)
    print("ANSWER-QUALITY COMPARISON")
    print("=" * 72)
    for i, (question, expected) in enumerate(QUESTIONS):
        print(f"\nQ{i+1}: {question}")
        print(f"  Expected: {expected}")
        for strat in STRATEGIES:
            ans = results[strat][i][2].replace("\n", " ").strip()
            print(f"  [{strat:>9}] {ans}")


if __name__ == "__main__":
    main()
