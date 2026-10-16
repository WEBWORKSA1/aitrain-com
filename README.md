# AiTrain.com

Free AI skills academy for working people, with a B2B team-training lead engine. Static HTML, hosted free on GitHub Pages.

## Structure

| Path | What |
|---|---|
| `index.html` | Home with interactive learning-line map |
| `paths.html`, `paths/*.html` | 6 learning lines (courses) |
| `guides.html`, `guides/*.html` | 26 original guides and role playbooks |
| `tools.html` · `prompts.html` · `videos.html` · `glossary.html` | Resources |
| `teams.html` · `ai-readiness-quiz.html` · `roi-calculator.html` | Lead generation |
| `support.html` · `contests.html` · `careers.html` · `advertise.html` | Donations, contests, hiring, sponsorship |
| Legal | privacy, terms, cookies, disclaimer, affiliate disclosure, editorial standards, trademark & copyright |
| `_src/` | Generator (`build.py`) and content sources |

## Edit and rebuild

```bash
pip install markdown
python3 _src/build.py
```

Guides live in `_src/guides/*.md` (`=== slug | title | category | minutes | description` header per guide). Lines, videos, tools, prompts and glossary live in `_src/data_*.py`.

## Monetisation setup

- AdSense script on every page; `ads.txt` at root.
- Forms submit via FormSubmit (AJAX). The first submission triggers a one-time activation email to the site inbox — click it to start receiving submissions.
- Contact address is never present in the published source.

## Hosting

GitHub Pages → Deploy from branch → `main` / root. After editing `_src/`, run the build and commit the regenerated HTML. Custom domain `aitrain.com` (CNAME file included): point DNS A records to 185.199.108.153, .109.153, .110.153, .111.153 and `www` CNAME to `webworksa1.github.io`, then enable "Enforce HTTPS".

See `PROMPTS.md` for the phase-wise build prompts.
