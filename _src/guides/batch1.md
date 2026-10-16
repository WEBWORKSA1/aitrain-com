=== what-is-generative-ai | What is generative AI? A plain-English guide for working people | Foundations | 8 | Generative AI explained without jargon: what it is, how it differs from older AI, what it is good at, and where it still needs a human.
Generative AI is software that produces new content — text, images, audio, code or video — in response to an instruction. When you ask an assistant to draft an email, summarise a report or suggest ten names for a product, you are using generative AI. The word *generative* is the important part: older AI systems mostly **classified** or **predicted** (is this email spam? will this customer churn?), while generative systems **create** an output that did not exist before.

## Key takeaways

- Generative AI creates new content from patterns it learned during training.
- It is excellent at first drafts, rewriting, summarising and brainstorming.
- It does not "look things up" by default, so facts, numbers and citations must be checked.
- The quality of the result depends heavily on the quality of your instruction (the prompt).

## How it differs from the AI you already used

You have used AI for years without calling it that. Your phone's face unlock, the spam filter in your inbox and the "you might also like" row on a shopping site are all machine learning. They take an input and give back a label or a score.

Generative AI flips that around. Instead of returning a label, it returns a full piece of work. That is why it feels so different: you can talk to it in ordinary sentences, and it answers in ordinary sentences.

| | Traditional machine learning | Generative AI |
|---|---|---|
| Typical output | A label, score or prediction | A paragraph, image, table, code or audio |
| Example | "This transaction is 92% likely to be fraud" | "Here is a polite reply to this complaint" |
| How you use it | Usually built into a product | Usually through a conversation or a prompt |
| Main risk | Wrong prediction | Confident but incorrect content |

## What it is genuinely good at

After watching thousands of people use these tools at work, a consistent pattern appears. Generative AI saves the most time on tasks where a **rough first version** is the hardest part:

1. **Drafting** — emails, proposals, job descriptions, social posts, lesson plans.
2. **Rewriting** — changing tone, shortening, simplifying for a different audience, translating.
3. **Summarising** — long documents, meeting transcripts, research papers.
4. **Structuring** — turning notes into an outline, a table or a checklist.
5. **Brainstorming** — names, angles, objections, test cases, interview questions.
6. **Explaining** — walking you through a concept at whatever level you ask for.

## Where it needs a human

The same system that writes a fluent paragraph can also invent a statistic, misquote a regulation or cite a paper that does not exist. This is often called a *hallucination*. It happens because the model is producing the most plausible-sounding continuation of your text, not checking a database of facts. Our guide on [catching AI hallucinations](ai-hallucinations-how-to-catch-them.html) covers a practical checking habit.

Other limits to keep in mind:

- **Knowledge cut-off.** A model only knows what was in its training data unless it is connected to search or your documents.
- **Arithmetic and precise logic.** Better than it used to be, but long calculations should be done in a spreadsheet or verified.
- **Context.** It knows nothing about your company, your client or your last meeting unless you tell it.
- **Judgement.** It can list options; deciding what is right for your situation is still your job.

## A simple mental model

Think of a generative AI assistant as a very fast, very well-read intern on their first day. They can write quickly and know a little about almost everything. They will also confidently guess when they do not know, and they have no idea how your organisation works. You get the best results by giving clear instructions, sharing the relevant background, and reviewing the work before it goes out.

## Your first exercise

Pick one task you did last week that took more than 20 minutes and produced a written result. Ask an assistant to do it with this structure:

> You are helping me with [task]. Here is the background: [2–3 sentences]. Please produce [exact output] for [audience]. Keep it under [length] and use [tone]. Ask me questions first if anything important is missing.

Compare the result with what you wrote. Note what it got right, what it missed, and what extra context would have fixed the gaps. That comparison is the beginning of real skill.

## Where to go next

Continue on the [Foundations Line](../paths/foundations.html), or jump to [how large language models work](how-large-language-models-work.html) if you want the mechanics in more detail.

=== how-large-language-models-work | How large language models work: tokens, training and prediction | Foundations | 10 | A clear explanation of large language models — tokens, next-word prediction, training, fine-tuning and context windows — and what each means for everyday use.
Large language models (LLMs) power most of today's AI assistants. Understanding roughly how they work is not just trivia: it explains why they are brilliant at some tasks, unreliable at others, and why the way you phrase a request changes the answer so much.

## Key takeaways

- An LLM reads and writes in **tokens** — chunks of words.
- At its core it repeatedly predicts the **next token** given everything before it.
- It learns patterns from huge amounts of text during **pre-training**, then is shaped into a helpful assistant through **fine-tuning** and human feedback.
- Everything it can "see" in a conversation must fit inside its **context window**.

## Step 1: text becomes tokens

Computers work with numbers, so text is first split into tokens. A token is often a whole common word, part of a longer word, or a punctuation mark. "Training" might be one token; an unusual surname might be three or four. As a rough rule for English, 100 tokens is about 75 words.

Why it matters: limits and prices for AI services are usually counted in tokens, and very long documents may need to be split.

## Step 2: predicting the next token

Give the model the text "The capital of France is" and it calculates a probability for every possible next token. "Paris" gets a very high probability, so it is likely to be chosen. The model then adds "Paris" to the text and predicts again, one token at a time, until it decides the answer is complete.

That is the whole trick, repeated extremely fast. The surprising part is how much ability emerges from it. To predict the next word in a legal contract, a recipe or a Python file well, the model has to absorb a great deal about grammar, facts, reasoning patterns and style.

### A pencil-and-paper version

Try this with a colleague. Write: "Thank you for your email. Unfortunately, we are unable to…" Ask them to guess the next three words. Most people write something like "accept your request" or "process your order". They are not looking anything up — they are drawing on patterns from every polite rejection they have ever read. An LLM does the same thing, with patterns from far more text.

## Step 3: pre-training

During pre-training, the model reads a vast collection of text and practises predicting the next token billions of times. Each time it is wrong, its internal settings (called **parameters** or **weights**) are nudged slightly to make the right answer more likely next time. The method behind those nudges is called gradient descent; the [Build with AI Line](../paths/build-with-ai.html) has visual videos that show it beautifully.

After pre-training, the model is a powerful text predictor but not yet a helpful assistant. Ask it a question and it might continue with three more questions, because that is a common pattern on the internet.

## Step 4: fine-tuning into an assistant

Developers then train the model further on examples of good conversations, and use human ratings to reward answers that are helpful, honest and harmless. This stage teaches the model to follow instructions, answer in a useful format, and decline clearly harmful requests.

## Step 5: the context window

When you chat, the model does not remember you the way a person does. Each time it answers, it is given the conversation so far — your messages, its replies, and any documents you pasted — up to a maximum size called the **context window**. Anything outside that window is invisible to it.

Practical consequences:

- In a very long chat, early instructions can lose influence. Restate important constraints.
- Paste the actual source material when you want answers based on it.
- Start a fresh conversation for an unrelated task, so old context does not leak in.

## Why answers vary

Most assistants add a little randomness when choosing tokens, so the same prompt can produce different wording each time. That is useful for brainstorming and less useful when you need consistency. Clear formats and examples reduce variation a lot — see [few-shot prompting](few-shot-prompting-examples.html).

## Why it can be confidently wrong

The model is optimised to produce plausible text. Most of the time plausible and true overlap. When they don't — an obscure fact, a recent event, a specific statistic — it can produce something that reads perfectly and is simply invented. Tools that connect the model to search or to your own documents (see [retrieval-augmented generation](retrieval-augmented-generation-explained.html)) reduce this, but checking still matters.

## Summary table

| Concept | One-line meaning | What you should do |
|---|---|---|
| Token | A chunk of text the model reads | Expect limits counted in tokens |
| Next-token prediction | Writes one piece at a time | Give a clear start and format |
| Pre-training | Learns patterns from huge text | Assume broad but imperfect knowledge |
| Fine-tuning | Learns to be an assistant | Give instructions directly |
| Context window | What it can see right now | Paste sources; restate key rules |

=== ai-hallucinations-how-to-catch-them | AI hallucinations: a five-question habit for catching errors | Foundations | 8 | Why AI assistants invent facts and citations, which outputs are most at risk, and a five-question review habit that catches most errors before they cause damage.
An AI "hallucination" is output that sounds right and is wrong: a statistic nobody published, a court case that never happened, a product feature that does not exist. It is the single most important limitation for anyone using AI at work, because the error arrives in the same confident tone as everything else.

## Key takeaways

- Hallucinations come from the way models generate text, not from a bug that will simply be patched away.
- Risk is highest for specific facts: numbers, names, dates, quotes, citations, laws and recent events.
- A short, consistent review habit catches the large majority of problems.
- Giving the model your source documents and asking it to quote from them reduces errors sharply.

## Why it happens

A language model predicts likely text. When you ask for "three studies showing X", the most plausible-looking answer contains three study titles with authors and years — so that is what it writes, whether or not those studies exist. The model is not lying; it has no built-in sense of the difference between "I know this" and "this would fit here".

## The risk map

| Output type | Risk | Why |
|---|---|---|
| Rewriting your own text | Low | The facts come from you |
| Summarising a document you pasted | Low–medium | May drop nuance or merge points |
| General explanations of well-known topics | Medium | Usually right, sometimes outdated |
| Statistics, prices, dates | High | Specific and easy to invent |
| Citations, links, quotes | Very high | Format is easy to fake |
| Legal, medical, financial specifics | Very high | Errors are costly and rules change |

## The five-question habit

Before AI-assisted work leaves your hands, ask:

1. **Where did each fact come from?** If a number, name or claim did not come from you or a source you can open, treat it as unverified.
2. **Can I open every citation?** Click every link. Search every paper title. If it does not exist, remove it.
3. **Is anything time-sensitive?** Prices, regulations, leadership roles and product features change. Check the current official source.
4. **Did it answer the question I actually asked?** Fluent answers sometimes drift to an easier, adjacent question.
5. **Would I sign my name to it?** If you could not defend a sentence to your manager or client, rewrite or cut it.

## Prompts that reduce hallucinations

- *"Use only the information in the document below. If the answer is not in the document, say 'not stated'."*
- *"Quote the exact sentence from the source that supports each point."*
- *"List anything in your answer you are not certain about."*
- *"Do not include statistics unless they appear in the material I provided."*

These do not make the model perfect, but they change its default from "produce something plausible" to "stay inside the evidence".

## A worked example

A marketing manager asked an assistant for "five statistics about remote-work productivity with sources". The answer listed five neat figures with publisher names. Checking took eight minutes: two figures matched real reports (with slightly different numbers), one came from a real publisher but a different year, and two could not be found at all. The fix was simple: she searched for two credible reports herself, pasted them in, and asked the assistant to pull the key figures from those reports only. The final result was accurate and still much faster than writing from scratch.

## Building it into team practice

- Add a line to your [AI use policy](write-an-ai-use-policy.html): "All facts, figures and citations in AI-assisted work must be verified against a primary source."
- Keep a shared list of near-misses. Real examples teach faster than rules.
- For high-stakes work, have a second person review sources, not just wording.

Teams that adopt this habit early tend to trust AI more, not less — because they know exactly where it needs watching.

=== ai-privacy-at-work | Using AI at work without leaking sensitive data | Responsible AI | 8 | What not to paste into AI tools, how consumer and business plans typically differ, and a quick checklist for reading any AI tool's data policy.
The fastest way to turn a productivity win into a serious incident is to paste the wrong thing into the wrong tool. This guide gives you a practical rule set you can follow today, whatever assistant your organisation uses.

## Key takeaways

- Treat any AI tool your organisation has not approved like a public website.
- Never paste personal data about customers, patients, students or employees into an unapproved tool.
- Business and enterprise plans often offer stronger data commitments than free consumer plans — but read the actual terms.
- When in doubt, remove names and identifying details first.

## The traffic-light rule

**Green — generally fine in any reputable assistant**
- Public information and your own general questions.
- Drafts that contain no confidential details.
- Generic templates ("a polite reminder about an overdue invoice").

**Amber — only in tools your organisation has approved**
- Internal documents, strategy notes, unreleased product details.
- Financial figures that are not public.
- Code from private repositories.

**Red — avoid unless a specific, approved process exists**
- Personal health information.
- Government ID numbers, bank or card details, passwords, API keys.
- Information about children.
- Anything covered by a confidentiality agreement or legal privilege.

## Consumer versus business plans

Many AI providers offer both free or individual plans and business or enterprise plans. Common differences — which you should always confirm in the provider's current terms — include whether conversations may be used to improve models, how long data is retained, administrative controls, single sign-on, and contractual commitments such as data-processing agreements. Policies change, so check the current version rather than relying on a blog post (including this one).

## Five questions to ask of any AI tool

1. Is my input used to train or improve the provider's models, and can that be switched off?
2. How long are conversations and files stored, and can I delete them?
3. Where is the data processed and stored?
4. Who at my organisation can see what I put in?
5. Is there a signed agreement covering this data?

If you cannot answer these, the tool belongs in the amber or red zone for anything sensitive.

## Anonymise before you paste

You can often get the same help with identifying details removed:

- Replace names with roles: "Client A", "Employee B".
- Round or remove exact figures that are not needed for the task.
- Remove addresses, account numbers and dates of birth.
- Summarise the situation in your own words instead of pasting the original record.

## Watch out for connected tools

AI features that can read your email, calendar or drive are powerful and need extra care. Content from an incoming email or web page can contain hidden instructions (so-called prompt injection) that try to make the assistant do something you did not ask. Review actions such as sending messages or sharing files before they happen, and keep permissions as narrow as the task allows.

## For managers

Staff will use AI whether or not there is a policy. A short, clear [AI use policy](write-an-ai-use-policy.html) plus an approved tool is far safer than a ban that pushes usage into personal accounts. Training people on the traffic-light rule takes under an hour and prevents most of the problems we see.

*This guide is general information, not legal advice. Your obligations depend on your jurisdiction, sector and contracts.*

=== prompt-engineering-framework | The five-part prompt: a framework that works on any AI assistant | Prompt Craft | 9 | Role, context, task, constraints and format — a repeatable prompt structure with before-and-after examples you can use with any AI assistant.
Most disappointing AI answers come from instructions that leave the model guessing. The five-part prompt removes the guesswork. It works on every major assistant because it mirrors how you would brief a capable human colleague.

## Key takeaways

- Good prompts answer five questions: **who** should the AI be, **what background** matters, **what** should it do, **what rules** apply, and **what shape** should the answer take.
- You do not need all five every time; add parts until the output is right.
- Format instructions are the cheapest way to get output you can use immediately.

## The five parts

| Part | Question it answers | Example |
|---|---|---|
| Role | Who is doing the work? | "Act as an experienced customer-support lead." |
| Context | What does it need to know? | "Our customers are small bakeries; the delivery was two days late because of a supplier issue." |
| Task | What exactly should it produce? | "Write a reply to the complaint below." |
| Constraints | What rules apply? | "Under 120 words. Offer a 10% credit. Don't blame the supplier by name." |
| Format | What should the output look like? | "Subject line, then the email body. No sign-off; I'll add mine." |

## Before and after

**Before:**

> Write a reply to this angry customer.

The result is generic, probably too long, and may promise things you cannot deliver.

**After:**

> You are an experienced customer-support lead for a wholesale flour supplier. Our customers are small independent bakeries. This customer's delivery arrived two days late because a supplier missed a shipment; that has been fixed.
> Write a reply to the complaint below. Keep it under 120 words, apologise once (not repeatedly), offer a 10% credit on the next order, and do not name the supplier. Use a warm, direct tone.
> Format: a subject line, then the email body. No sign-off.
> Complaint: [paste]

The second prompt takes 40 seconds longer to write and usually saves several rounds of editing.

## Part by part

### Role
A role sets vocabulary, priorities and level of detail. "Explain this as a tax accountant" and "explain this as a primary-school teacher" give very different answers. Keep roles realistic and relevant.

### Context
This is where most of the value is. The model knows nothing about your audience, history or goals. Two or three sentences of context typically beat any amount of clever wording. If you have source material, paste it and say so: "Use the policy text below."

### Task
Use a clear verb: draft, summarise, compare, rewrite, extract, classify, critique. One main task per prompt works best; for bigger jobs see [prompt chaining](prompt-chaining-for-long-tasks.html).

### Constraints
Length, tone, things to include, things to avoid, reading level, legal or brand rules. Positive instructions ("use plain English") tend to work better than only negative ones ("don't be complicated").

### Format
Ask for exactly the shape you need: a table with named columns, a numbered checklist, three options labelled A/B/C, headings matching your template, or structured data. You will paste the result faster and spot gaps sooner.

## A reusable template

```
Role: You are a [role] helping [who].
Context: [2–4 sentences of background]. Source material is below if relevant.
Task: [verb] [what] for [audience/purpose].
Constraints: [length], [tone], include [x], avoid [y].
Format: [exact structure].
If anything important is missing, ask me up to 3 questions before answering.
```

That last line is surprisingly powerful: it lets the model surface gaps instead of guessing.

## Practise it

Take three prompts you used this week and rewrite each with all five parts. Run both versions and compare. Then save the best ones to a shared [prompt library](build-a-team-prompt-library.html) — or start from our [prompt library](../prompts.html), which uses this structure throughout.
