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

**Sample chunks:**
Five real chunks produced by the default `character` strategy (reproduce with `python chunking.py character`). Each is labeled with its `chunk_id`, source file, 0-based position in its document, and character length.

```
[chunk_id: cs216_0 | source: CS216.txt | position: 0 | 500 chars]
CS216 Everything Data - Spring 2025
Syllabus

Course Structure: Hybrid, Flipped, Just-in-Time
* Hybrid: A Zoom session is associated with the class for equity. However, you are
expected to attend class in person if at all possible. To attend online, you must
request it on the forms page to receive that day's password.
* Flipped: Easier-to-grasp material is learned before class via readings, videos,
and comprehension quizzes. Class time is spent actively engaging with the more
complex, harder-to-
```
*A short, topically focused chunk around the "Course Structure" heading — this is the chunk that lets the system answer Q3 under `character` but not `paragraph` (see the comparison below).*

```
[chunk_id: cs116_7 | source: CS116.txt | position: 7 | 499 chars]
ng that third of the semester.
* Project 3 (Final Project): An open-ended project of your group's choosing. Your
group is responsible for finding, cleaning, exploring, and analyzing a unique
dataset.

Exams
* Three evenly spaced midterms administered individually.
* To minimize high-stakes stress, Exam 3 takes place on the final day of standard
class rather than a block final exam period.
* Before Exam 1, the instructor will run an in-class mock exam so students can
familiarize themselves with
```

```
[chunk_id: cs201_44 | source: CS201.txt | position: 44 | 499 chars]
her your code passes a suite of tests. In general, passing 85% of the tests will
result in full credit for the assignment. Projects turned in up to 24 hours late
receive no penalty. After that, a late submission loses 10% a day (weekend counts
as one day). Projects are not accepted after one week. Each project requires
developing code and answering questions about the assignment (the project's
analysis). Your write-up should be your own.

Exams
There are three midterms scheduled in 201 for Fall
```

```
[chunk_id: cs201_45 | source: CS201.txt | position: 45 | 499 chars]
questions about the assignment (the project's analysis). Your write-up should be
your own.

Exams
There are three midterms scheduled in 201 for Fall 2024. Each counts for 11% of
your course grade. These will be held during class, in the classroom. You may not
use any electronic device nor may you communicate with anyone. Exams will be
multiple choice and/or short-answer; you will not be expected to write extensive
code or paragraphs. The final exam is mandatory, counts for 11% of your grade, an
```
```
[chunk_id: cs330_0 | source: CS330.txt | position: 0 | 499 chars]
COMPSCI 330 Design and Analysis of Algorithms
Summer 2018

Class: M/Tu/W/Th 3:30 - 5:05pm (LSRC A156)
Recitations: Tu/Th 2:00 - 3:15pm (Allen 103)
Prerequisites: CompSci 201 and CompSci 230 (or equivalent)
Course Website: https://www2.cs.duke.edu/courses/summer18/compsci330
Instructor: Brandon Fain
Office Hours: 2-3:20 pm M/W and 5:15-6:15 pm Th in LSRC D301
Contact: By email at btfain@cs.duke.edu (expect a response within a business day)

Required Book:
Algorithms by Sanjoy Dasgupta, Christos
```

---

## Chunking Strategy Comparison

I ran the full pipeline under both selectable strategies — `character` and `paragraph` — over the same query set: the 5 evaluation questions plus the documented CS330 failure case. Everything except chunking was held constant. I then judged the generated answers against the expected answers. This is reproducible with `python compare_chunking.py`.

| # | Question | `character` answer | `paragraph` answer | Better |
|---|----------|--------------------|--------------------|--------|
| 1 | How is the final exam administered in CS230? | Accurate — online, take-home, open-book/notes, released 12:01am, due 11:59pm ET, ~3 hrs untimed in 24-hr window | Accurate — same content | tie |
| 2 | How much is Exam 3 worth in CS116? | Accurate — "18%" | Accurate — "18%" | tie |
| 3 | How is CS216 structured? | Accurate — "Hybrid, Flipped, and Just-in-Time…" with the full explanation | "I don't have enough information on that." | **character** |
| 4 | What is the late submission penalty for projects in CS201? | Accurate — ≤24 hrs no penalty, then 10%/day | Accurate — same, plus "not accepted after one week" | tie |
| 5 | Should I take CS 201 before CS 101? | Accurate — no, CS101 is the prerequisite | Accurate — same conclusion | tie |
| 6 | What are the prerequisites for CS 330? *(failure case)* | "I don't have enough information" | "I don't have enough information" | tie |

**Score on the 5 evaluation questions: `character` 5/5 accurate, `paragraph` 4/5.**

**Which performed better, and why:**
**`character` produced higher-quality responses for this corpus.** On four of the five evaluation questions the two strategies produce effectively identical, accurate answers — these are short, keyword-heavy lookups (an exam weight, a late penalty, a prerequisite line) where either way of splitting keeps the relevant fact intact, so the *response* is the same regardless of chunking. The strategies diverge on **Q3 ("How is CS216 structured?")**, and that single question is decisive: under `character` the system returns a complete, correct answer ("CS216 is structured as a Hybrid, Flipped, and Just-in-Time course…"), while under `paragraph` it refuses entirely with "I don't have enough information on that."

I think this is because of how each strategy split the CS216 structure section, which the syllabus writes as a heading plus three bullets (`Course Structure: Hybrid, Flipped, Just-in-Time`, then the Hybrid/Flipped/Just-in-Time explanations). `paragraph` chunking keeps that whole block as one large chunk that also includes in other details irrelevant to the strategy in the same paragraph. It's likely that those extra words pull the chunk's embedding directionally away from what the query looks like, so it never enters the top-10 the generator sees. `character` chunking instead carves a short, focused chunk around the `Course Structure: Hybrid, Flipped…` heading, whose embedding stays close to the query, so the generator receives the right text and answers it. The overlap also gives each section a second chance to surface near a window boundary. In short, `paragraph`'s "respect the natural structure" behavior backfires when a section is long and topically mixed because it dilutes the embedding and costs an answer, whereas `character`'s fixed-size windows keep every chunk narrow enough to match. This is consistent with the Evaluation Report below, which was run under the default `character` strategy and scored all 5 questions accurate.

---

## Embedding Model

**Model used:**
`all-MiniLM-L6-v2`, run locally through the `sentence-transformers` library. ChromaDB handles the embedding automatically through its `SentenceTransformerEmbeddingFunction`, and the collection is configured to use cosine distance for similarity. I chose this model because it's small, fast, and runs locally with no API key or per-call cost, which made it easy to re-embed the whole corpus repeatedly while I was tuning chunk size and top-k. For short syllabus chunks it gives good enough semantic matching, and at 384 dimensions it keeps the vector store lightweight for a corpus this size.

**Production tradeoff reflection:**
If I were deploying this for real students and cost wasn't a concern, the main thing I'd weigh is accuracy on domain-specific text. `all-MiniLM-L6-v2` is a general-purpose model, and my failure case (the CS330 prerequisites question) shows its weakness: it doesn't strongly tie a query like "CS 330" to the document that says "COMPSCI 330". A larger or domain-tuned embedding model (or one fine-tuned on academic/course text) would likely capture the course-identity signal better. I'd also consider models with a longer context limit so I could embed bigger chunks (like a full grading table) without splitting them. The tradeoffs there are added latency and cost per query, plus a dependency on an external service — for a small, local class project the lightweight local model is the better fit, but for a real deployment I'd trade some of that speed and simplicity for retrieval accuracy.

---

## Retrieval

Retrieval is a semantic search over the 236 embedded chunks: the query is embedded with the same `all-MiniLM-L6-v2` model and ChromaDB returns the top `k=10` chunks by cosine distance (lower = closer). The examples below are real output from `python embed_and_retrieve.py` (truncated for readability), showing each query, the top returned chunks with their cosine distance, and which chunk actually answers the question.

A consistent pattern shows up across all three: because every syllabus shares the same vocabulary (every course has exams, projects, late penalties, and grading tables), several near-miss chunks from *other* courses crowd the top of the ranking, but the chunk that actually answers the question is reliably pulled into the top-10 the generator sees — which is why all five evaluation answers come out accurate.

### Example 1 — "How much is Exam 3 worth in CS116?"

| Rank | Chunk | Distance | Relevant? |
|------|-------|----------|-----------|
| 1 | CS116.txt#7 | 0.519 | Partial — CS116 exam *section*, but describes exam scheduling, not weights |
| 2 | CS250.txt#5 | 0.530 | Off — CS250 grading breakdown (wrong course) |
| 3 | CS216.txt#12 | 0.532 | Off — CS216 practicum grading |
| … | … | … | |
| **10** | **CS116.txt#10** | **0.589** | **Yes — the grading table, where Exam 3 is listed at 18%** |

The exact answer (`Exam 3 | 18%`) lives in CS116.txt#10, which lands at rank 10. The higher-ranked distractors are other courses' grading/exam chunks that share the words "exam" and "grade." It's a close call, but the relevant chunk is retrieved within `k=10`, so the generator answers correctly ("Exam 3 is worth 18%"). This is the weakest of the three retrievals and the main argument for keeping `k` at 10 rather than lower.

### Example 2 — "What is the late submission penalty for projects in CS201?"

| Rank | Chunk | Distance | Relevant? |
|------|-------|----------|-----------|
| 1 | CS116.txt#10 | 0.409 | Off — CS116 grading table + late-window text (wrong course) |
| **2** | **CS201.txt#44** | **0.429** | **Yes — `Projects turned in up to 24 hours late receive no penalty. After that … 10% a day`** |
| 3 | CS370.txt#4 | 0.483 | Off — CS370 late penalty (wrong course) |
| 4 | CS230.txt#14 | 0.492 | Off — CS230 late penalty (wrong course) |

Strong retrieval: the correct chunk (CS201.txt#44) is rank 2, behind only a CS116 chunk that matched on "late" + "penalty" generically. The full late-submission rule sits intact in one chunk, so the generator reproduces it exactly.

### Example 3 — "How is the final exam administered in CS230?"

| Rank | Chunk | Distance | Relevant? |
|------|-------|----------|-----------|
| 1 | CS101.txt#20 | 0.404 | Off — CS101 final exam date/time (wrong course) |
| 2 | CS201.txt#46 | 0.423 | Off — CS201 final exam format (wrong course) |
| … | … | … | |
| **6** | **CS230.txt#11** | **0.455** | **Yes — `Final Exam … Online, take-home, open-book, open-notes … Released at 12:01am … untimed within the 24-hour window`** |

The answer chunk (CS230.txt#11, the "Exam Policy" block) is at rank 6. Every other course's "final exam" chunk scores slightly closer to the generic phrasing of the query, but the CS230 chunk is comfortably inside `k=10`, so the generator produces the full, accurate administration detail.

---

## Grounded Generation

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
