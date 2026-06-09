# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

The domain I have selected is Syllabi for Duke University CS Courses. These syllabi include information about the course’s learning objectives, prerequisites if any, grading policies, and any other course related policies. This knowledge may be difficult to find otherwise because each professor may choose to have their own personal site to host this, a GitHub page, or an official Duke site; this makes it difficult to aggregate and compare courses, especially when students consider multiple options before selecting a course to enroll in.
---

## Document Sources
| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | CS201 | Syllabus for Duke CS201. | https://coursework.cs.duke.edu/201fall24/documentation/-/blob/main/syllabus.md |
| 2 | CS250 | Syllabus for Duke CS250. | https://people.ee.duke.edu/~sorin/ece250/ |
| 3 | CS310 | Syllabus for Duke CS310. | https://courses.cs.duke.edu/spring25/compsci310/syllabus.pdf |
| 4 | CS330 | Syllabus for Duke CS330. | https://courses.cs.duke.edu/compsci330/summer18/Syllabus.pdf |
| 5 | CS171 | Syllabus for Duke CS171. | https://sites.duke.edu/compsci171cnfa2025/syllabus/ |
| 6 | CS370 | Syllabus for Duke CS370. | https://sites.duke.edu/compsci_370d_001_sp24/ |
| 7 | CS216 | Syllabus for Duke CS216. | https://sites.duke.edu/compsci216sp2025/syllabus/ |
| 8 | CS116 | Syllabus for Duke CS116. | https://sites.duke.edu/compsci116fa2021/syllabus/ |
| 9 | CS230 | Syllabus for Duke CS230. | https://courses.cs.duke.edu/spring20/compsci230/ |
| 10 | CS101 | Syllabus for Duke CS101. | https://courses.cs.duke.edu/fall25/compsci101/info.php |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
500 characters (character-based sliding window). Chunks shorter than 50 characters are dropped so whitespace artifacts and tiny trailing fragments don't get embedded.

**Overlap:**
150 characters between consecutive chunks.

**Why these choices fit your documents:**
My documents are cleaned syllabi made up of short policy statements, grading rows, and lists rather than long flowing prose. A 500-character window is big enough to hold a full rule or a couple of grading-table rows together, but small enough that each chunk stays focused on one topic instead of blending several unrelated sections into one blurry embedding. The 150-character overlap (roughly 2–3 sentences) means a rule that happens to land on a window boundary still shows up intact in the neighboring chunk, so I don't lose it to the split. Before chunking, I cleaned each source by hand and with Gemini to strip HTML, navigation, and other web cruft and saved the result as a plain `.txt` file per course, so the chunker is only ever splitting real syllabus content.

I also built the chunker so the strategy is selectable at runtime (`character` vs `paragraph`) — see the Chunking Strategy section of planning.md for that stretch feature — but the numbers above describe the default `character` strategy used for the evaluation.

**Final chunk count:**
236 chunks across all 10 documents.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
`all-MiniLM-L6-v2`, run locally through the `sentence-transformers` library. ChromaDB handles the embedding automatically through its `SentenceTransformerEmbeddingFunction`, and the collection is configured to use cosine distance for similarity. I chose this model because it's small, fast, and runs locally with no API key or per-call cost, which made it easy to re-embed the whole corpus repeatedly while I was tuning chunk size and top-k. For short syllabus chunks it gives good enough semantic matching, and at 384 dimensions it keeps the vector store lightweight for a corpus this size.

**Production tradeoff reflection:**
If I were deploying this for real students and cost wasn't a concern, the main thing I'd weigh is accuracy on domain-specific text. `all-MiniLM-L6-v2` is a general-purpose model, and my failure case (the CS330 prerequisites question) shows its weakness: it doesn't strongly tie a query like "CS 330" to the document that says "COMPSCI 330". A larger or domain-tuned embedding model (or one fine-tuned on academic/course text) would likely capture the course-identity signal better. I'd also consider models with a longer context limit so I could embed bigger chunks (like a full grading table) without splitting them. The tradeoffs there are added latency and cost per query, plus a dependency on an external service — for a small, local class project the lightweight local model is the better fit, but for a real deployment I'd trade some of that speed and simplicity for retrieval accuracy.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
> "You are an assistant that answers questions about Duke University computer science course syllabi. Answer using ONLY the syllabus text provided in the context below. If the provided context does not contain enough information to answer, respond exactly with: 'I don't have enough information on that.' Do not use outside or prior knowledge, and do not guess or fill in gaps from what you may know about Duke courses. When you do answer, make clear which course each part of the answer comes from by citing the source syllabus in parentheses with its .txt filename, for example (Source: CS201.txt)."

**How source attribution is surfaced in the response:**
The model cites its source inline, in parentheses with the `.txt` filename, attached to the claim it supports — e.g. *"Exam 3 is worth 18% in CS116 (Source: CS116.txt)."* Because each chunk in the context is labeled with its real source filename, the citation reflects the document the answer was actually drawn from. I deliberately chose this inline approach over listing every retrieved file: an earlier version showed all retrieved chunks under a separate "Retrieved from" box, but that listed everything that was searched, not where the answer actually came from, so I moved attribution into the answer text itself.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | How is the final exam administered in CS230? | Online, take-home, open-book/open-notes; released 12:01am, due 11:59pm ET, ~3 hrs but untimed within a 24-hour window. | "Online, take-home, open-book, open-notes exam... released at 12:01am and due by 11:59pm Eastern Time... roughly 3 hours... untimed within the 24-hour window (Source: CS230.txt)." | Relevant | Accurate |
| 2 | How much is Exam 3 worth in CS116? | 18% of the final grade. | "Exam 3 is worth 18% in CS116 (Source: CS116.txt)." | Relevant | Accurate |
| 3 | How is CS216 structured? | Hybrid, Flipped, and Just-in-Time: pre-class readings/videos/quizzes, in-class active work on harder material. | "Hybrid, Flipped, and Just-in-Time course... easier-to-grasp material is learned before class via readings, videos, and comprehension quizzes, and class time is spent actively engaging with the more complex... material (Source: CS216.txt)." | Relevant | Accurate |
| 4 | What is the late submission penalty for projects in CS201? | ≤24 hrs late: no penalty; after that 10% per day. | "Projects turned in up to 24 hours late receive no penalty. After that, a late submission loses 10% a day (weekend counts as one day) (Source: CS201.txt)." | Relevant | Accurate |
| 5 | Should I take CS 201 before CS 101? | No — CS101 is a prerequisite for CS201. | "...the prerequisites state 'introductory programming experience at the level of Computer Science 101...' This implies that you should take CS 101 before taking CS 201 (Source: CS201.txt)." | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:**
"What are the prerequisites for CS 330?"

**What the system returned:**
"I don't have enough information on that." This is despite the fact that CS330.txt states the answer explicitly and unambiguously near the top of the document: `Prerequisites: CompSci 201 and CompSci 230 (or equivalent)`. Inspecting the retrieved chunks confirms the problem — the top 10 results (at k=10) were CS201#4, CS370#5, CS310#5, CS230#10, CS230#0, CS250#4, CS201#51, CS250#0, CS250#1, and CS101#8. Not a single CS330 chunk was retrieved, so the generator never saw the relevant text and correctly refused to answer rather than hallucinate.

**Root cause (tied to a specific pipeline stage):**
This is a retrieval and/or embedding failure, not a chunking or generation one.The embeddings don't have awareness about the course so that is a weak signal. Additionally every one of the syllabi has a prerequisites/preconditions section, so the word "prerequisites" matches all of them roughly equally. This means that chunks across all of the courses syllabi, all of which discuss prerequisites, out-rank the actual CS330 chunk.

**What you would change to fix it:**
What we could do is prepend the course code to every chunk's text before embedding. For example, begin each CS330 chunk with `"CS330 / COMPSCI 330 — "`. This bakes the course identity into every vector, so "CS 330" in a query pulls CS330 chunks upward.
---

## Spec Reflection
**One way the spec helped you during implementation:**
The spec helped me separate each of the stages into clear and well defined steps. It also helped me enumerate which parts of the planning process were relevant towards implementing each part of the project. Additionally it helped serve as a framework to think thorugh things like configuration values (chunk size etc.) so that I could think about it in a systematic way.

**One way your implementation diverged from the spec, and why:**
I actually documented and added a stretch feature that allows the user to select which chunking strategy to use (character based/fixed-length OR paragraph basede). So that was not originally in the spec or even the project requirements but I added it to explore how it would help. Additionally I altered the top k number while I was working on the project and updated the spec to reflect the updated value.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* For the generation stage I gave Claude parts of my planning.md, which did not say anything about citing sources in the response. I asked it to help me wire up the LLM call so the answer was built only from the retrieved chunks.
- *What it produced:* It produced a working generator that answered from the retrieved context, but the response itself didn't surface where the answer actually came from — there was no source attribution in the text the user would read.
- *What I changed or overrode:* Because my planning doc never dictated source attribution, I had to override the behavior and direct it to actually return the source in the response, not just answer from the documents silently. This is what later turned into the inline `(Source: …txt)` citation.

**Instance 2**

- *What I gave the AI:* For source attribution, my first version listed every retrieved file under a "Retrieved from" box, which I didn't like because it showed all the chunks searched, not where the answer actually came from. I told Claude I wanted the answer to show only the source the answer was actually built from.
- *What it produced:* Claude first proposed parsing the course codes out of the generated answer text, and then proposed having the LLM output a separate `SOURCES:` line that the code would parse and validate against the retrieved files.
- *What I changed or overrode:* I directed  to adjust the system prompt so the LLM cites the source inline in parentheses with the `.txt` extension, e.g. `(Source: CS201.txt)`, and then to remove the separate sources box from the Gradio UI entirely. This kept attribution simple and tied directly to the claim the model was making.

---

## Query Interface

The query interface is a Gradio web app (`app.py`), launched with `python app.py` and opened in the browser at the local URL it prints.

**Input fields:**
- **Your question** — a text box where the user types their question about a Duke CS syllabus (e.g. "How much is Exam 3 worth in CS116?"). Pressing Enter or clicking **Ask** submits it.
- **Chunking strategy (optional)** — a dropdown with `(use current)`, `character`, and `paragraph`. Leaving it on `(use current)` queries whatever is already indexed; picking `character` or `paragraph` re-indexes the corpus under that strategy before answering (so the first query after a switch takes a little longer). This exposes the selectable-chunking stretch feature in the UI.

**Output field:**
- **Answer** — a text box showing the grounded answer, with the source cited inline in parentheses, e.g. `(Source: CS116.txt)`. If the retrieved context can't answer the question, this field instead shows "I don't have enough information on that."

**Sample interaction transcript:**

```
Your question:        How is the final exam administered in CS230?
Chunking strategy:    (use current)

[Ask]

Answer:
The final exam in CS230 is administered online, as a take-home, open-book,
open-notes exam (Source: CS230.txt). It is released at 12:01am and due by
11:59pm Eastern Time, and is designed to take roughly 3 hours to complete,
although it is untimed within the 24-hour window (Source: CS230.txt).
```
