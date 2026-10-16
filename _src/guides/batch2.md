=== few-shot-prompting-examples | Few-shot prompting: show the AI what good looks like | Prompt Craft | 7 | How giving one to three examples in your prompt locks in tone, structure and quality — with templates for product descriptions, data extraction and classification.
"Few-shot prompting" simply means including a few examples of the output you want inside your prompt. It is the most reliable way to get consistent tone and format, and it often works better than paragraphs of description.

## Key takeaways

- Examples communicate style more precisely than adjectives like "punchy" or "professional".
- One to three good examples are usually enough.
- Make examples varied enough that the model learns the pattern, not the specific content.
- Clearly separate examples from the new input.

## Why examples work

Language models are pattern machines. If you describe the style you want, the model has to translate your description into a pattern. If you show the pattern, it can copy it directly. Telling someone "write it like our brand" is vague; handing them two past posts that nailed the brand voice is not.

## Template 1: product descriptions

```
Write a product description in the same style as the examples.

Example 1
Product: Linen apron, natural colour
Description: Stone-washed linen that softens with every wash. Deep front pocket, adjustable neck strap, and long ties that wrap to the front. Made to be used, not saved for best.

Example 2
Product: Walnut cutting board, large
Description: One solid piece of oiled walnut, big enough for a whole loaf. Juice groove on one side, flat serving face on the other. Wipe clean, oil monthly, keep for decades.

Now write one for:
Product: Cast-iron skillet, 26 cm
Description:
```

Notice what the examples teach without saying it: three short sentences, concrete materials, a practical detail, and a closing line with personality.

## Template 2: extracting data

```
Extract the company name, contact person and requested date from each message. Return one line per message as: company | person | date. Use "unknown" if missing.

Message: "Hi, this is Priya from Northfield Dental — could we book the workshop for 14 March?"
Output: Northfield Dental | Priya | 14 March

Message: "Hello, we'd like a quote for training our staff sometime in spring."
Output: unknown | unknown | spring

Message: [paste new message]
Output:
```

The second example is important: it shows the model what to do when information is missing, which prevents it from inventing a company name.

## Template 3: classification

```
Classify each support ticket as Billing, Technical, Account or Other.

Ticket: "I was charged twice this month." → Billing
Ticket: "The export button does nothing on Safari." → Technical
Ticket: "How do I add a second admin?" → Account

Ticket: [new ticket] →
```

## Common mistakes

- **Examples too similar.** If every example is about shoes, the model may assume everything is about shoes.
- **One bad example.** The model copies flaws as faithfully as strengths. Choose your best work.
- **No separator.** Use labels like "Example 1", "Input", "Output" so the boundary is obvious.
- **Too many examples.** Beyond a handful, you mostly add length. Increase only if quality is still inconsistent.

## When to use zero examples

For one-off creative tasks where you want surprise, examples can limit the model. Start without them, and add examples once you know what you like.

## Next step

Combine examples with the [five-part prompt](prompt-engineering-framework.html) and save the result as a template your whole team can reuse.

=== prompt-chaining-for-long-tasks | Prompt chaining: how to handle long or complex work with AI | Prompt Craft | 8 | Break big tasks into a sequence of focused prompts — research, outline, draft, review — to get higher-quality reports, proposals and plans from AI.
Ask an AI assistant to "write a 3,000-word market report" in a single prompt and you will usually get something long, smooth and shallow. Split the same job into a chain of smaller steps and the quality jumps. This is prompt chaining.

## Key takeaways

- Each prompt in a chain does one job and produces an output you check before moving on.
- Chains give you control points where your judgement improves the result.
- A standard four-step chain — gather, outline, draft, review — covers most writing tasks.

## Why single prompts struggle with big tasks

A long request asks the model to plan, research, structure, write and self-edit all at once, in a single pass, with no chance for you to correct direction. Errors in the plan flow straight into the draft. By the time you read the output, fixing it means starting over.

## The four-step writing chain

### Step 1 — Gather
> Here are my notes and three source documents. List the 10 most important points for [audience] about [topic]. For each, say which source it comes from.

**Check:** Are the points right? Is anything important missing? Add or remove before continuing.

### Step 2 — Outline
> Using these approved points, propose an outline for a [length] [document type]. Give section headings and one sentence per section describing its purpose.

**Check:** Is the order logical for the reader? Does each section earn its place?

### Step 3 — Draft
> Write section 2 only, following the outline. Use the tone of the example below. Keep it to about 300 words.

Drafting section by section keeps quality high and lets you redirect early.

### Step 4 — Review
> Act as a sceptical [manager/client]. Review the full draft below. List the five weakest points, any unsupported claims, and anything confusing. Don't rewrite it.

Then fix the issues yourself or with targeted prompts.

## Other useful chains

| Task | Chain |
|---|---|
| Proposal | Client needs → objections → solution outline → pricing table → draft → critique |
| Job posting | Role outcomes → must-have skills → draft → bias check → final |
| Data analysis | Describe dataset → questions to answer → formulas/code → interpret results → summary |
| Lesson plan | Learning goals → activities → assessment → differentiation → handout |
| Research brief | Questions → sources (yours) → extract findings → compare → conclusions |

## Tips

- **Carry forward only what's needed.** Paste the approved outline into the draft step rather than relying on a long chat history.
- **Name the steps.** "This is step 3 of 4" helps the model stay in its lane.
- **Save the chain.** A chain that works once will work again; store it in your [team prompt library](build-a-team-prompt-library.html).
- **Automate later.** Once a chain is stable, it is a natural candidate for [automation](automate-repetitive-work-with-ai.html).

Chaining feels slower the first time. By the second or third use, it is faster than single prompts — because you stop rewriting outputs that went wrong at step one.

=== build-a-team-prompt-library | How to build a prompt library your team will actually use | Prompt Craft | 7 | A practical system for collecting, naming, testing and sharing your team's best AI prompts so everyone gets expert-level results.
In most teams, a few people quietly get great results from AI while everyone else gets average ones. The difference is usually a handful of well-tuned prompts. A shared prompt library spreads those prompts to everyone.

## Key takeaways

- Start with ten prompts for your team's most frequent tasks, not a hundred generic ones.
- Every entry needs a name, a purpose, the prompt, an example output and an owner.
- Use placeholders in square brackets so people know exactly what to fill in.
- Review the library monthly; delete what nobody uses.

## Step 1: find the tasks

Ask each team member: "What did you use AI for this week, and what result were you happiest with?" You will quickly see repeated tasks — meeting summaries, client emails, report sections, social posts, code reviews. Pick the ten most frequent.

## Step 2: write a standard entry

| Field | Example |
|---|---|
| Name | Client follow-up after discovery call |
| Purpose | Turn call notes into a follow-up email with next steps |
| Prompt | (full text with [placeholders]) |
| Inputs needed | Call notes, client name, agreed next step |
| Example output | A short sample |
| Owner | Sam (sales) |
| Last tested | Month and year |

## Step 3: use clear placeholders

```
You are an account manager at [company]. Using the call notes below, write a follow-up email to [client name] that:
- thanks them for their time in one sentence,
- summarises the three most important needs they mentioned,
- confirms the next step: [next step and date],
- stays under 150 words in a friendly, professional tone.
Call notes: [paste notes]
```

Square-bracket placeholders make prompts usable by people who did not write them.

## Step 4: test before publishing

Run each prompt on three different real inputs. If any result needs heavy editing, refine the prompt or add an example (see [few-shot prompting](few-shot-prompting-examples.html)). Only publish prompts that work reliably.

## Step 5: choose a home

Use whatever your team already opens daily: a shared document with a table of contents, a wiki page, a spreadsheet with one row per prompt, or the shared-prompt feature in your AI tool if it has one. The best location is the one people will actually check.

## Step 6: keep it alive

- Add a "suggest a prompt" form or channel.
- Mark entries tested within the last quarter.
- Retire prompts nobody has used in two months.
- Share one "prompt of the week" with a before-and-after example.

## Measuring the impact

Track a simple before-and-after for two or three library tasks: minutes per task and how much editing the output needed. Our guide to [measuring AI productivity](measure-ai-productivity.html) has a template. Numbers like "client follow-ups went from 15 minutes to 4" make the case for wider adoption.

Browse our public [prompt library](../prompts.html) for starter entries you can adapt.

=== automate-repetitive-work-with-ai | Automate repetitive work with AI: a step-by-step method | Workflow Automation | 10 | Find the tasks worth automating, add AI steps to no-code workflows, keep a human in the loop, and measure the hours you get back.
Prompting saves minutes. Automation saves hours, because the work happens without you starting it. This guide walks through a method that works for individuals and small teams with no coding background.

## Key takeaways

- Automate tasks that are frequent, rule-based and annoying — not the ones that need your judgement.
- Every automation has a **trigger**, **actions** and **data** passed between them.
- An AI step is best at classifying, extracting, summarising and drafting.
- Put a human approval step anywhere a mistake would be expensive or embarrassing.

## Step 1: run a one-week task audit

For five working days, jot down repetitive digital tasks: what you did, how often, and how long it took. Then score each:

**Score = times per week × minutes each × (1 + error cost)**

Use error cost 0 for "harmless if wrong", 1 for "annoying", 2 for "costly". The top three scores are your first candidates.

Typical winners:

- Sorting incoming enquiries and routing them to the right person.
- Copying details from emails or forms into a spreadsheet or CRM.
- Summarising long email threads or meeting transcripts.
- Drafting routine replies for review.
- Producing a weekly status summary from several sources.

## Step 2: check what you already have

Before buying anything, look at AI features inside tools you already pay for: email clients, office suites, CRMs, helpdesks and meeting software increasingly include summarising and drafting. Switching these on is the cheapest automation there is.

## Step 3: understand the three building blocks

1. **Trigger** — what starts it: a new email, a form submission, a new row, a scheduled time.
2. **Actions** — what happens: create a record, send a message, update a sheet, call an AI step.
3. **Data mapping** — which piece of information flows into which field.

Popular no-code automation platforms all use these same three ideas, so the skills transfer.

## Step 4: add an AI step

Write prompts for automations differently from chat prompts: they must work on every input without you there to clarify.

```
Classify the enquiry below into exactly one category: Sales, Support, Partnership, Job application, Other.
Then extract: sender name, company (or "none"), and a one-sentence summary.
Return only valid JSON with keys: category, name, company, summary.
Enquiry: {{email body}}
```

Rules for automation prompts:

- Ask for a fixed format (often JSON or a fixed list) so the next step can read it.
- Define what to do when information is missing.
- Keep the task narrow. Two simple AI steps beat one complicated one.

## Step 5: keep a human in the loop

| Risk if wrong | Pattern |
|---|---|
| Low (internal tagging) | Fully automatic; spot-check weekly |
| Medium (internal summaries) | Automatic, with a "flag issue" link |
| High (anything sent to customers) | AI drafts → person approves → send |

Never let an automation send external messages, make payments or delete data without approval until it has a long, checked track record.

## Step 6: measure and report

Record the baseline time per task before you start and the time after a month. Include error rates. A short report — "Enquiry routing: 3.5 hours/week → 25 minutes/week, 2 misroutes in 140 enquiries" — makes the next automation easy to approve. See [measuring AI productivity](measure-ai-productivity.html).

## A starter project

Automate your form or inbox enquiries: trigger on a new message, classify and summarise with an AI step, add a row to a spreadsheet, and notify the right person. Most people can build this in an afternoon and save time every week.

=== ai-for-spreadsheets | Using AI with spreadsheets: formulas, cleaning and summaries | Workflow Automation | 8 | Practical ways to use AI assistants for spreadsheet formulas, messy data cleanup, pivot analysis and plain-English summaries — with prompts that work.
Spreadsheets are where a huge amount of office work lives, and they are one of the places AI helps most. You do not need to be a formula expert; you need to describe what you want clearly.

## Key takeaways

- Describe your columns and your goal, and the AI can write the formula.
- Ask for an explanation of every formula so you can check and maintain it.
- Use AI to clean inconsistent text, but always verify on a sample first.
- For calculations that matter, let the spreadsheet do the maths, not the chatbot.

## Writing formulas

The key is describing your layout precisely.

> My sheet has order dates in column A (from row 2), customer names in column B and order totals in column C. Write a formula for cell F2 that returns the total order value for the customer named in E2, but only for orders in 2025. Explain how it works.

Check the explanation line by line. If the formula references the wrong column or misses a condition, say exactly what is wrong and ask for a fix.

## Cleaning messy data

Common jobs AI handles well:

- Standardising company names ("Acme Inc.", "ACME", "Acme Incorporated").
- Splitting full names into first and last name.
- Converting mixed date formats into one format.
- Categorising free-text entries (e.g. reasons for cancellation).

Workflow:

1. Paste 20–30 representative rows (with sensitive data removed — see [privacy at work](ai-privacy-at-work.html)).
2. Ask for the cleaned version **and** the rule it applied.
3. Check the sample carefully.
4. Apply the rule with a formula or your spreadsheet's built-in tools across the full dataset, rather than pasting thousands of rows into a chat.

## Analysis and summaries

> Here is a summary table of monthly sales by region. Write five plain-English observations a regional manager would care about, then two questions the data raises but doesn't answer. Don't calculate anything new; use only the numbers shown.

That last sentence matters. Language models can make arithmetic slips; asking them to interpret numbers you already calculated is safer than asking them to calculate.

## Building templates

AI is good at designing a sheet from a description:

> Design a simple project tracker spreadsheet for a five-person team. List the columns, the data type for each, any dropdown values, and two conditional-formatting rules that would help spot late tasks.

## Prompts to keep

- "Explain what this formula does in plain English: [formula]"
- "This formula returns an error: [formula]. Here's my layout: [description]. What's wrong?"
- "Suggest three charts that would best show [goal] using these columns: [list]."
- "Turn this table into a short email update for my manager."

## Check your work

- Test formulas on rows where you already know the answer.
- Watch for ranges that stop short of your data.
- Keep a copy of the original data before bulk changes.

Spreadsheet skills are one of the quickest wins in team training because nearly everyone uses them and results are easy to measure.
