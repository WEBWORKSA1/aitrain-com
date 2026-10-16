# AiTrain.com — Phase-wise build prompts

These are the prompts used (and reusable) to build and extend AiTrain.com. Run them in order. Each phase is self-contained and assumes the repo `WEBWORKSA1/aitrain-com` (static HTML, GitHub Pages, free plan).

---

## Concept (decided)

**AiTrain.com = free AI skills academy for working people + B2B team-training lead engine.**

- Traffic: learning lines (structured courses), original guides, role playbooks, prompt library, AI tools directory, glossary, video lessons.
- Revenue: Google AdSense (ca-pub-6620975821265271) on high-RPM education/B2B-software content; team-training leads (fulfilled directly or referred to vetted partner trainers); labelled sponsorships; donations; contest sponsorships.
- Brand device: a transit/line map — learning paths are "lines", modules are "stations", the hub is "Central". No trains, no third-party logos.

---

## Phase 1 — Research and positioning

> Visit at least 35 leading sites in AI learning, prompt education, AI tool directories, AI newsletters and corporate AI training (e.g. deeplearning.ai, elementsofai.com, coursera.org, fast.ai, kaggle.com/learn, huggingface.co/learn, learnprompting.org, promptingguide.ai, futurepedia.io, theresanaiforthat.com, therundown.ai, superhuman.ai, toolify.ai, datacamp.com, codecademy.com, edx.org, udacity.com, grow.google, learn.microsoft.com, brilliant.org, khanmigo.ai, machinelearningmastery.com, maven.com, sectionai.com, generalassemb.ly, business.udemy.com…). For each, record core offering, standout features, lead-capture patterns, monetisation and design patterns. Synthesise the top 30 features ranked by traffic and revenue impact, B2B lead-form best practice, content gaps, and a trademark check for "AI Train / AiTrain". Output a positioning statement and sitemap.

## Phase 2 — Design system and layout

> Create `assets/css/site.css` for a static site with a transit-map identity: light and dark themes via CSS tokens on `:root` (with `prefers-color-scheme` and a `data-theme` override), Overpass typeface, six line colours, left-aligned layout, 1180px wrapper, 16px mobile gutter, no horizontal scroll, visible focus states, reduced-motion support. Components: top notice bar, sticky header with mobile menu, buttons, panels, route lists (line + station dots), hero line-map SVG, forms (multi-step with progress bar, pill radios/checkboxes, consent rows, honeypot), filters, video facades, quiz, calculator, glossary A–Z, tiers, FAQ details, CTA band, footer, cookie banner.

## Phase 3 — Site generator and global chrome

> Write `_src/build.py` that renders every page through one `layout()` function so every page has: the AdSense script in `<head>` (`<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>`), meta description, canonical, Open Graph, JSON-LD, and at the very top the notice "Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership" linking to https://web.works/contact. Generate sitemap.xml, robots.txt, ads.txt (`google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0`), CNAME, .nojekyll, manifest and favicon.

## Phase 4 — Contact address protection and forms

> All forms post via JavaScript to FormSubmit's AJAX endpoint. The destination address must never appear in HTML, JS strings, base64 or anywhere in the published source — store it as an XOR-encoded, reversed number array decoded at runtime. "Email us" links use `data-mail` and build the `mailto:` only on click. Every form has a honeypot, required consent, optional newsletter opt-in (unchecked), a status message and a redirect to `thank-you.html`.

## Phase 5 — Content (AdSense-approval grade)

> Write 25+ original, practical guides (800–1,200 words each) with key-takeaways, tables, prompts and internal links: generative AI basics, how LLMs work, hallucinations, privacy at work, five-part prompting, few-shot, prompt chaining, team prompt library, automation, spreadsheets, meeting notes, measuring productivity, RAG, evaluation, adoption roadmap, AI use policy template, EU AI Act literacy checklist, choosing an assistant, getting your employer to pay; role playbooks for nurses/healthcare, teachers, small business, real estate, marketers, HR, finance. No volatile facts (prices), no fabricated statistics or testimonials, disclaimers where professional advice is implied.

## Phase 6 — Learning lines and resources

> Build six learning lines (Foundations, Prompt Craft, Workflow Automation, Build with AI, AI for Leaders, Responsible AI), each with level, hours, audience, outcomes, 5–7 stations, linked guides and verified YouTube lessons (privacy-enhanced, load-on-click facades). Build: start-here persona router, searchable/filterable AI tools directory (40+ tools, nominative names only, no logos, suggest-a-tool form), prompt library (35+ prompts with [placeholders] and copy buttons), glossary (60+ terms with DefinedTermSet schema), video page.

## Phase 7 — Lead generation engine

> Build `teams.html` with a two-step form (step 1: work email, team-size band, goals; step 2: name, organisation, role, country, format, timeline, tools in use, outcome, consent including partner-sharing). Add programmes, process, FAQ schema and CTAs. Build lead magnets that feed the same inbox: a 10-question team AI readiness check with instant score (Boarding / Moving / Express) and gated tailored outline, and a training ROI calculator with gated plan request. Add a "Training a team?" box to every guide and line page that passes `?topic=` into a hidden field.

## Phase 8 — Donations, contests, hiring, sponsorship

> Build `support.html` (tiers, allocation to operations / promotion / hiring / contests, pledge form — payment link sent manually, nothing charged by the form), `contests.html` (monthly prompt challenge, judging criteria, entry form, official rules: no purchase necessary, 18+, void where prohibited, skill-based judging, licence to publish), `careers.html` (contributor roles and application form), `advertise.html` (sponsored lines, featured listings, contest sponsorship, newsletter slots, partnerships, domain acquisition link to web.works/contact).

## Phase 9 — Compliance and trust

> Write privacy (AdSense cookie language, opt-out links, FormSubmit processor, partner sharing with consent, GDPR/PIPEDA/Law 25 rights), terms, cookies, disclaimer, affiliate disclosure, editorial standards, about, contact and a trademark & copyright notice (no affiliation with AirTrain transit operators, Airtrain.ai, "AI+ TRAINING" applicant or any AI vendor; nominative use; embedded video rights; takedown process). Add a cookie banner with Accept all / Essential only (essential sets non-personalised ads).

## Phase 10 — QA, publish, grow

> Verify: no contact address anywhere in the published source; AdSense script and top notice on every page; zero broken internal links; no horizontal scroll at 390px; lead form, quiz and calculator work end to end. Push to `WEBWORKSA1/aitrain-com` on `main`, enable GitHub Pages (Deploy from branch → main → / root), add custom domain aitrain.com, enforce HTTPS. Then: submit sitemap in Google Search Console, apply to AdSense, enable Google's certified CMP for EEA/UK, and publish 2 new guides per week.

---

## Expansion prompts (after approval)

- **Programmatic SEO:** "Generate one page per tool in the directory (`/tools/<slug>.html`) with what it does, best uses, 3 prompts for it, alternatives and a team-training CTA."
- **Comparisons:** "Create neutral 'X vs Y for [task]' pages for the 10 most-searched assistant pairs, based on criteria not prices."
- **French edition:** "Translate the top 10 guides and the teams page into Canadian French under `/fr/` with hreflang."
- **Role playbooks:** "Add playbooks for lawyers, government, trades, customer support, sales, nonprofits and students."
- **Newsletter:** "Connect the footer form to a double-opt-in email service and publish a weekly 'one AI skill' issue."
