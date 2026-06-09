"""Gradio web UI for the Duke CS syllabus guide.

Run with:  python app.py
Then open the local URL it prints.

The interface lets you ask a question and (optionally) pick which chunking
strategy the corpus should be indexed with. Changing the strategy re-ingests
the corpus, so the first query after a switch takes a little longer.
"""

import gradio as gr

from query import ask

# "(use current)" maps to None — query whatever is already in the store without
# re-ingesting.
STRATEGY_CHOICES = ["(use current)", "character", "paragraph"]


def handle_query(question, strategy):
    question = (question or "").strip()
    if not question:
        return "Please enter a question."

    selected = None if strategy == "(use current)" else strategy
    result = ask(question, strategy=selected)
    return result["answer"]


with gr.Blocks(title="Duke CS Syllabus Guide") as demo:
    gr.Markdown(
        "# Duke CS Syllabus Guide\n"
        "Ask about Duke computer science course policies, prerequisites, "
        "grading, and more. Answers are grounded only in the syllabus documents."
    )

    inp = gr.Textbox(label="Your question",
                     placeholder="e.g. What are the prerequisites for CS 330?")
    strategy = gr.Dropdown(
        choices=STRATEGY_CHOICES,
        value="(use current)",
        label="Chunking strategy (optional)",
        info="Switching re-indexes the corpus; the next query will be slower.",
    )
    btn = gr.Button("Ask", variant="primary")

    answer = gr.Textbox(label="Answer", lines=8)

    btn.click(handle_query, inputs=[inp, strategy], outputs=answer)
    inp.submit(handle_query, inputs=[inp, strategy], outputs=answer)


if __name__ == "__main__":
    demo.launch()
