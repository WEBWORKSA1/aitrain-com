=== ai-meeting-notes-workflow | An AI meeting-notes workflow that people actually read | Workflow Automation | 6 | Turn recordings or transcripts into decisions, owners and deadlines — plus consent, accuracy and storage rules for AI meeting notes.
AI transcription and summarising can remove one of the most tedious jobs in office life. But a raw summary that nobody reads saves nothing. This workflow produces short notes centred on what people need to do.

## Key takeaways

- Get consent before recording, every time.
- Ask for decisions, action items, owners and deadlines — not a narrative of who said what.
- A person who attended should check the notes before they are sent.
- Store notes where the team already looks.

## Step 1: consent and setup

Tell participants at the start that the meeting is being recorded and transcribed, and why. Laws and workplace rules on recording vary; follow your organisation's policy. For sensitive topics — HR matters, health, legal advice — consider not recording at all.

## Step 2: the summary prompt

```
Below is a meeting transcript. Produce:
1. Decisions made (bullet list; only items explicitly agreed).
2. Action items as a table: task | owner | due date ("not set" if none was stated).
3. Open questions that were raised but not resolved.
4. A three-sentence summary for people who missed the meeting.
Do not include anything not supported by the transcript. If ownership is unclear, write "unclear".
Transcript: [paste]
```

Asking for "unclear" instead of a guess prevents the most common error: the AI assigning a task to the wrong person.

## Step 3: human check

The meeting organiser or a note-taker spends two minutes reviewing: Are the decisions right? Are the owners right? Anything sensitive that should not go to the whole list?

## Step 4: distribute and track

Send the notes within an hour while the meeting is fresh. Copy action items into your task tracker so they don't live only in an email.

## Retention

Transcripts can contain sensitive remarks. Keep the summary and delete the full recording when it is no longer needed, in line with your organisation's retention policy.

## Results to expect

Teams that adopt this typically cut note-taking time to a few minutes per meeting and, more importantly, see fewer forgotten action items. Add it to your [automation plan](automate-repetitive-work-with-ai.html) once the prompt is stable.

=== measure-ai-productivity | How to measure the productivity gains from AI | AI for Leaders | 8 | A simple measurement framework — baseline, time saved, quality, adoption and cost — with a one-page report template for showing AI return on investment.
"Is AI actually saving us time?" is the question every manager eventually asks. Most teams cannot answer it because they never measured the starting point. This guide gives you a light framework that takes less than an hour to set up.

## Key takeaways

- Measure a baseline before rolling out AI or training.
- Track four things: time, quality, adoption and cost.
- Use a few representative tasks rather than trying to measure everything.
- Report in a single page with numbers and one or two real examples.

## The four measures

| Measure | What to record | How |
|---|---|---|
| Time | Minutes per task, before and after | Self-reported log for two weeks; spot-check |
| Quality | Edits needed, errors found, reviewer rating | Simple 1–5 rating by a reviewer |
| Adoption | % of people using AI weekly for the task | Short monthly survey or tool analytics |
| Cost | Licences, training hours, setup time | Finance records |

## Step 1: choose three to five tasks

Pick tasks that are frequent, comparable and important — for example, first drafts of client proposals, weekly reports, support replies, or data clean-up.

## Step 2: capture the baseline

For two weeks, people record minutes spent on each chosen task and the number of revision rounds. Keep it simple: a shared spreadsheet with date, task, minutes and revisions.

## Step 3: introduce AI and training

Roll out the tool and a short, task-specific training session. Generic "intro to AI" sessions rarely move numbers; showing people the exact prompts for their exact tasks does. Our [team training programmes](../teams.html) are built this way.

## Step 4: measure again

After four to six weeks, repeat the same log for two weeks.

## Step 5: calculate value

**Annual value ≈ people × adoption rate × hours saved per week × hourly cost × working weeks**

For example: 40 people × 70% adoption × 2 hours saved/week × $45/hour × 46 weeks ≈ $115,920 per year. Compare that with licence and training costs. You can model your own numbers with our [training ROI calculator](../roi-calculator.html).

## Report template

1. **Headline:** "AI saves the proposals team about 6 hours per person per month."
2. **Numbers:** table of before/after time, quality and adoption.
3. **Cost and return:** annual value vs. annual cost.
4. **Two stories:** concrete examples in people's own words.
5. **Risks and fixes:** errors found and how they were handled.
6. **Next step:** the next team or task to expand to.

## Pitfalls

- **Self-reporting optimism.** Spot-check a sample.
- **Quality drift.** Faster but worse is not a win; keep the reviewer rating.
- **Counting licences as adoption.** Seats are not usage.
- **Ignoring learning time.** The first weeks are slower; measure after people are comfortable.

=== retrieval-augmented-generation-explained | Retrieval-augmented generation (RAG) explained | Build with AI | 9 | How RAG lets AI answer from your own documents: chunking, embeddings, vector search and grounded answers, with design tips and common failure modes.
Retrieval-augmented generation, usually shortened to RAG, is the most common way to make an AI assistant answer questions from your own documents — policies, manuals, contracts, knowledge bases — instead of from general training data.

## Key takeaways

- RAG = search your documents for relevant passages, then give those passages to the model with the question.
- It reduces made-up answers and lets the model cite sources.
- Most quality problems come from the retrieval step, not the model.
- Always show users which sources an answer came from.

## The pipeline

1. **Collect** documents you trust.
2. **Chunk** them into passages (often a few paragraphs each), keeping titles and section headings with each chunk.
3. **Embed** each chunk: convert it into a list of numbers (a vector) that represents its meaning.
4. **Store** the vectors in a searchable index.
5. **Retrieve**: when a question arrives, embed it and find the chunks with the most similar meaning.
6. **Generate**: send the question plus the top chunks to the model with an instruction such as "Answer using only these sources and cite them."

## Why embeddings work

Embeddings place text with similar meaning close together in a high-dimensional space. "How many vacation days do I get?" lands near a policy paragraph about "annual leave entitlement" even though they share few words. That is why RAG search often beats keyword search for natural questions. Many systems combine both — semantic search plus keyword matching — for the best results.

## Design tips

- **Chunk by meaning.** Split on headings and sections rather than fixed character counts where possible.
- **Keep metadata.** Store document title, date, owner and link with each chunk to enable citations and filtering.
- **Retrieve a few, not many.** Too many chunks dilute the relevant ones and raise cost.
- **Instruct grounding.** "If the sources don't contain the answer, say so."
- **Keep documents current.** Outdated policies produce confidently outdated answers. Re-index when documents change.

## Common failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Says "not found" for answers that exist | Chunks too small or poor search | Larger chunks, hybrid search, better titles |
| Mixes up two similar policies | Missing metadata | Add document names and dates; filter by them |
| Cites the wrong section | Too many retrieved chunks | Retrieve fewer; re-rank results |
| Answers from general knowledge | Weak instruction | Explicit "use only the sources" rule |

## Evaluate it

Build a test set of 30–50 real questions with known correct answers and the source each should come from. Re-run it whenever you change chunking, search or prompts. Our guide on [evaluating AI outputs](evaluate-ai-outputs.html) shows how.

## Security

Only index documents users are allowed to see, and enforce permissions at retrieval time. Treat text inside documents as data, not instructions, to reduce prompt-injection risk.

=== evaluate-ai-outputs | How to evaluate AI outputs: test sets, rubrics and regression checks | Build with AI | 8 | A practical approach to measuring AI quality — building a test set, writing a scoring rubric, using human and automated review, and catching regressions.
Whether you are rolling out an internal assistant or shipping an AI feature, "it seemed fine when I tried it" is not a quality process. Evaluation turns impressions into evidence.

## Key takeaways

- Build a test set from real inputs, including the awkward ones.
- Score against a written rubric, not gut feel.
- Re-run the same tests after every change to prompts, models or data.
- Combine automated checks with periodic human review.

## Step 1: build a test set

Collect 30–100 real examples of what users will ask or submit. Include:

- Typical cases (the bulk of real usage).
- Edge cases: very short, very long, ambiguous, multilingual.
- Cases where the correct answer is "I don't know" or "out of scope".
- Known past failures.

For each, write the expected result or the key facts a good answer must contain.

## Step 2: write a rubric

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Correctness | Wrong or invented | Partly correct | Fully correct |
| Completeness | Misses key points | Some missing | All key points |
| Grounding | No sources / wrong sources | Some cited | Correctly cited |
| Format | Unusable | Needs edits | Ready to use |
| Safety/tone | Problematic | Minor issues | Appropriate |

Keep criteria few and clear so two reviewers would score the same answer similarly.

## Step 3: score

- **Human review** for nuance. Have two people score a sample and compare to keep the rubric honest.
- **Automated checks** for objective things: valid format, required fields present, banned phrases absent, length limits.
- **Model-assisted grading** can speed up review, but calibrate it against human scores first and spot-check it regularly.

## Step 4: watch for regressions

Save scores with the date and what changed (prompt version, model, data). When you change anything, re-run the full set. A prompt tweak that fixes one problem can quietly break three others.

## Step 5: monitor in production

- Let users flag bad answers easily.
- Sample real conversations (with appropriate privacy controls) for review.
- Add new failure cases to the test set.

## Minimum viable evaluation

If you only have an afternoon: 30 real examples, a three-criterion rubric (correct, grounded, usable), and a spreadsheet. That alone puts you ahead of most AI rollouts.

=== ai-adoption-roadmap-for-teams | An AI adoption roadmap for teams: from curiosity to measurable results | AI for Leaders | 10 | A five-stage roadmap for introducing AI in a team or small organisation — use-case selection, policy, pilot, training, measurement and scale.
Buying AI licences is easy. Getting people to change how they work is the hard part. This roadmap reflects the approach that consistently works for teams of 10 to 1,000 people.

## Key takeaways

- Start with specific tasks, not with "AI strategy" in the abstract.
- Publish a short policy before or alongside the rollout.
- Pilot with one motivated team and measure from day one.
- Training must be role-specific and hands-on.
- Scale what the numbers support.

## Stage 1: inventory and prioritise (week 1–2)

Ask each team for their five most time-consuming recurring tasks. Plot ideas on a simple grid:

| | Low risk | High risk |
|---|---|---|
| **High value** | Do now | Pilot carefully |
| **Low value** | Quick wins if easy | Wait |

"Risk" includes data sensitivity, customer impact and regulatory exposure. Good first candidates: drafting internal documents, summarising, research support, spreadsheet work, first-line support drafts with human approval.

## Stage 2: set guardrails (week 2–3)

Publish a one-page [AI use policy](write-an-ai-use-policy.html): approved tools, what data stays out, review requirements, disclosure, and who to ask. Approve at least one tool so people are not pushed into personal accounts.

## Stage 3: pilot (weeks 3–8)

- One team, three to five tasks, a named champion.
- Capture a baseline first (see [measuring AI productivity](measure-ai-productivity.html)).
- Weekly 20-minute check-ins: what worked, what failed, which prompts to share.
- Decide in advance what result means "scale up".

## Stage 4: train for behaviour change (in parallel)

What doesn't work: a single one-hour webinar for the whole company.

What does work:

1. A short shared foundation (60–90 minutes): how AI works, limits, policy, verification habit.
2. Role-specific workshops using the team's real tasks and documents.
3. A prompt library seeded from the workshop.
4. Office hours or a chat channel for questions during the first month.
5. A refresher after 30 days to share wins and fix bad habits.

## Stage 5: measure and scale (month 3+)

Report time saved, quality, adoption and cost. Expand to the next team using the pilot's prompt library and champions. Revisit the policy quarterly.

## Signs it's working

- People share prompts without being asked.
- Managers can name specific tasks that got faster.
- Fewer requests to use unapproved tools.
- Quality holds or improves while cycle time drops.

## Signs it isn't

- Licence usage falls after the first month.
- The same few enthusiasts do all the usage.
- People can't explain the policy.

If your team needs help with any stage, our [team training](../teams.html) page describes formats from a single workshop to a full rollout programme.
