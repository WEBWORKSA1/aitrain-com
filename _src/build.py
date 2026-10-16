#!/usr/bin/env python3
"""Static site generator for AiTrain.com.
Run:  python3 _src/build.py   (from repo root). Writes HTML into the repo root.
"""
import os, re, json, html, math, datetime
import markdown
from data_paths import PATHS, VIDEOS
from data_lists import TOOLS, PROMPTS, GLOSSARY

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://aitrain.com"
NAME = "AiTrain"
ADS = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>'
TODAY = datetime.date.today().isoformat()
UPDATED = "October 2026"
E = html.escape
PAGES = []  # for sitemap

LOGO = ('<svg width="34" height="34" viewBox="0 0 34 34" aria-hidden="true"><rect x="1" y="13" width="32" height="8" rx="4" fill="#1652F0"/>'
        '<circle cx="9" cy="17" r="6" fill="#fff" stroke="#E4002B" stroke-width="3.5"/><circle cx="25" cy="17" r="6" fill="#fff" stroke="#00A86B" stroke-width="3.5"/></svg>')

NAV = [("start-here.html","Start here"),("paths.html","Learning lines"),("guides.html","Guides"),("tools.html","AI tools"),
       ("prompts.html","Prompts"),("videos.html","Videos"),("contests.html","Contests"),("support.html","Support us")]

def mail_link(text, subject, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<a href="contact.html" data-mail="{E(subject)}"{c}>{text}</a>'

def layout(path, title, desc, body, schema=None, active=None, og_type="website"):
    depth = path.count("/")
    b = "../" * depth
    canon = SITE + "/" + ("" if path == "index.html" else path)
    nav = "".join(f'<a href="{b}{h}"{" aria-current=\"page\"" if active==h else ""}>{t}</a>' for h,t in NAV)
    ld = ""
    if schema:
        for s in (schema if isinstance(schema, list) else [schema]):
            ld += '<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False) + '</script>\n'
    full_title = title if title.endswith(NAME) or "AiTrain" in title else f"{title} | {NAME}"
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(full_title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="AiTrain">
<meta property="og:title" content="{E(full_title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#1652F0">
<meta name="google-adsense-account" content="ca-pub-6620975821265271">
<link rel="icon" href="{b}assets/img/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="{b}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Overpass:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{b}assets/css/site.css">
{ADS}
{ld}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="notice">Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership — <a href="https://web.works/contact" rel="noopener" target="_blank">web.works/contact</a></div>
<header class="site-head"><div class="wrap head-in" style="position:relative">
<a class="brand" href="{b}index.html" aria-label="AiTrain home">{LOGO}<span>AiTrain</span></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
<nav class="nav" id="nav" aria-label="Main">{nav}<button class="theme-btn" type="button" aria-label="Switch light or dark theme">◐</button><a class="btn" href="{b}teams.html">Train your team</a></nav>
</div></header>
<main id="main">
{body}
</main>
{footer(b)}
<div class="cookie" role="dialog" aria-label="Cookie choices"><b>Cookies on AiTrain.</b> We and our advertising partner Google use cookies to show ads, measure performance and remember your settings. See our <a href="{b}cookies.html">cookie policy</a>.
<div class="btn-row"><button class="btn" data-consent="all">Accept all</button><button class="btn ghost" data-consent="essential">Essential only</button></div></div>
<button class="btn ghost to-top" type="button" aria-label="Back to top">Top</button>
<script src="{b}assets/js/site.js" defer></script>
</body>
</html>
'''
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page.replace('href="contact.html" data-mail', f'href="{b}contact.html" data-mail'))
    if path not in ("404.html", "thank-you.html"):
        PAGES.append(path)

def footer(b):
    col = lambda title, links: f'<div><h4>{title}</h4><ul>' + "".join(f'<li><a href="{b}{h}">{t}</a></li>' for h,t in links) + '</ul></div>'
    return f'''<footer class="site-foot"><div class="wrap">
<div class="foot-grid">
<div><a class="brand" href="{b}index.html">{LOGO}<span>AiTrain</span></a>
<p class="muted" style="margin-top:10px">Free, practical AI training for working people — and hands-on programmes for teams.</p>
<form class="news" data-form="Newsletter" data-next="{b}thank-you.html" aria-label="Newsletter signup">
<div class="hp"><input name="_hp" tabindex="-1" autocomplete="off"></div>
<label class="skip" for="nl-email">Email</label><input id="nl-email" type="email" name="email" required placeholder="you@work.com"><input type="hidden" name="list" value="Weekly AI Skills email"><button class="btn" type="submit">Subscribe</button></form>
<p class="muted" style="font-size:.85rem;margin-top:6px">One practical AI skill every week. Unsubscribe anytime.</p></div>
{col("Learn",[("start-here.html","Start here"),("paths.html","Learning lines"),("guides.html","Guides"),("videos.html","Video lessons"),("glossary.html","AI glossary")])}
{col("Resources",[("tools.html","AI tools directory"),("prompts.html","Prompt library"),("ai-readiness-quiz.html","Team readiness check"),("roi-calculator.html","Training ROI calculator"),("contests.html","Contests")])}
{col("Work with us",[("teams.html","Team training"),("advertise.html","Advertise & sponsor"),("support.html","Support / donate"),("careers.html","Careers & contributors"),("contact.html","Contact")])}
{col("About",[("about.html","About AiTrain"),("editorial-standards.html","Editorial standards"),("privacy.html","Privacy policy"),("terms.html","Terms of use"),("cookies.html","Cookie policy"),("disclaimer.html","Disclaimer"),("affiliate-disclosure.html","Affiliate disclosure"),("trademark-copyright.html","Trademark & copyright")])}
</div>
<div class="fine">© <span id="yr">2026</span> AiTrain.com. Original content; all rights reserved. AiTrain is an independent educational publication and is not affiliated with or endorsed by any AI company, transit operator or training provider named on this site. Third-party names are used for identification only. <a href="{b}trademark-copyright.html">Trademark &amp; copyright notice</a>. Interested in this domain, sponsorship, advertising or partnership? <a href="https://web.works/contact" target="_blank" rel="noopener">web.works/contact</a>.</div>
</div></footer>'''

def crumbs(b, items):
    parts = [f'<a href="{b}index.html">Home</a>'] + [f'<a href="{b}{h}">{E(t)}</a>' if h else E(t) for h,t in items]
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " / ".join(parts) + '</nav>'

def bc_schema(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":SITE+"/"+u} for i,(u,n) in enumerate([("", "Home")]+items)]}

def hp():
    return '<div class="hp" aria-hidden="true"><label>Leave empty<input name="_hp" tabindex="-1" autocomplete="off"></label></div>'

def consent(partner=False):
    extra = " and to share it with a vetted training partner if needed to prepare a quote" if partner else ""
    return (f'<label class="consent"><input type="checkbox" name="consent" value="yes" required> I agree AiTrain may use these details to respond to my request{extra}. See the <a href="privacy.html">privacy policy</a>.</label>'
            '<label class="consent"><input type="checkbox" name="newsletter_optin" value="yes"> Also send me the weekly AI skills email (optional).</label>')

def team_cta(b, topic):
    return f'''<div class="panel" style="border:2px solid var(--ink)"><h3>Training a team?</h3>
<p class="muted">Turn this topic into a hands-on session built around your team's real tasks. Quote within 2 business days.</p>
<a class="btn" href="{b}teams.html?topic={E(topic)}">Get a team quote</a></div>'''

# ---------------------------------------------------------------- guides
def load_guides():
    guides = []
    for fn in sorted(os.listdir(os.path.join(ROOT, "_src", "guides"))):
        txt = open(os.path.join(ROOT, "_src", "guides", fn), encoding="utf-8").read()
        for chunk in txt.split("=== ")[1:]:
            head, body = chunk.split("\n", 1)
            slug, title, cat, mins, desc = [x.strip() for x in head.split("|")]
            guides.append(dict(slug=slug, title=title, cat=cat, mins=int(mins), desc=desc, md=body.strip()))
    return guides

GUIDES = load_guides()
GBY = {g["slug"]: g for g in GUIDES}

def guide_pages():
    for g in GUIDES:
        b = "../"
        htmlbody = markdown.markdown(g["md"], extensions=["tables", "fenced_code", "toc", "sane_lists"])
        # TOC from h2s
        heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', htmlbody)
        toc = "".join(f'<a href="#{i}">{t}</a>' for i,t in heads)
        # checkboxes "- [ ]"
        htmlbody = htmlbody.replace("<li>[ ] ", '<li>☐ ')
        related = [x for x in GUIDES if x["cat"] == g["cat"] and x["slug"] != g["slug"]][:4]
        rel = "".join(f'<li><a href="{x["slug"]}.html">{E(x["title"])}</a></li>' for x in related)
        body = f'''<div class="wrap" style="padding-top:28px">{crumbs(b,[("guides.html","Guides"),(None,g["cat"])])}
<div class="layout-side"><article class="article">
<span class="tag">{E(g["cat"])}</span><span class="tag">{g["mins"]} min read</span><span class="tag">Updated {UPDATED}</span>
<h1 style="font-size:clamp(1.9rem,4vw,2.8rem)">{E(g["title"])}</h1>
<p class="lede">{E(g["desc"])}</p>
<p class="muted" style="font-size:.92rem">By the AiTrain editorial team · Reviewed under our <a href="../editorial-standards.html">editorial standards</a></p>
{htmlbody}
<div class="ad-space" aria-hidden="true"></div>
<div class="panel"><h3>Keep learning</h3><ul>{rel}</ul><p style="margin:0"><a href="../guides.html">All guides</a> · <a href="../paths.html">Learning lines</a> · <a href="../prompts.html">Prompt library</a></p></div>
</article>
<aside class="side">{('<div class="panel toc"><h3>On this page</h3>'+toc+'</div>') if toc else ''}
{team_cta(b, g["title"])}
<div class="panel"><h3>Weekly AI skill</h3><p class="muted">One practical technique by email each week.</p><a class="btn ghost" href="#nl-email">Subscribe</a></div>
</aside></div></div>'''
        schema = [{"@context":"https://schema.org","@type":"Article","headline":g["title"],"description":g["desc"],
                   "dateModified":TODAY,"author":{"@type":"Organization","name":"AiTrain editorial team"},
                   "publisher":{"@type":"Organization","name":"AiTrain","url":SITE},"mainEntityOfPage":f"{SITE}/guides/{g['slug']}.html"},
                  bc_schema([("guides.html","Guides"),(f"guides/{g['slug']}.html",g["title"])])]
        layout(f"guides/{g['slug']}.html", g["title"], g["desc"], body, schema, "guides.html", "article")

def guides_index():
    cats = []
    for g in GUIDES:
        if g["cat"] not in cats: cats.append(g["cat"])
    btns = '<button type="button" data-cat="all" aria-pressed="true">All</button>' + "".join(f'<button type="button" data-cat="{E(c)}" aria-pressed="false">{E(c)}</button>' for c in cats)
    cards = "".join(f'<div class="panel" data-cat="{E(g["cat"])}"><span class="tag">{E(g["cat"])}</span><span class="tag">{g["mins"]} min</span><h3><a href="guides/{g["slug"]}.html">{E(g["title"])}</a></h3><p class="muted">{E(g["desc"])}</p></div>' for g in GUIDES)
    body = f'''<section><div class="wrap"><div class="sec-head"><h1>AI guides</h1><p class="lede">{len(GUIDES)} practical, original guides — from how AI works to role-specific playbooks for nurses, teachers, marketers, HR and finance teams.</p></div>
<div class="filters" data-filter="glist"><label class="skip" for="gq">Search guides</label><input id="gq" type="search" placeholder="Search guides">{btns}</div>
<div class="grid g3" id="glist">{cards}</div><p class="empty" hidden>No guides match. Try a broader word.</p></div></section>'''
    layout("guides.html", "AI guides: practical how-tos and role playbooks", f"{len(GUIDES)} free, practical AI guides: prompting, automation, AI policy, measurement and playbooks for specific jobs.", body, None, "guides.html")

# ---------------------------------------------------------------- line map
def line_map():
    hub = (300, 210)
    lines = [
        (PATHS[0], [(30,80),(170,80),(300,210),(430,340),(570,340)]),
        (PATHS[1], [(30,340),(170,340),(300,210),(430,80),(570,80)]),
        (PATHS[2], [(30,210),(570,210)]),
        (PATHS[3], [(300,22),(300,398)]),
        (PATHS[4], [(470,22),(470,120),(380,210)]),
        (PATHS[5], [(130,398),(130,300),(220,210)]),
    ]
    svg = ['<svg viewBox="0 0 600 420" role="img" aria-labelledby="maptitle"><title id="maptitle">Map of AiTrain learning lines and their modules</title>']
    for p, pts in lines:
        d = "M" + " L".join(f"{x},{y}" for x,y in pts)
        svg.append(f'<path d="{d}" fill="none" stroke="{p["hex"]}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
    for p, pts in lines:
        segs = [(pts[i], pts[i+1]) for i in range(len(pts)-1)]
        lens = [math.dist(a,b) for a,b in segs]; total = sum(lens)
        n = len(p["stations"]); placed = []; k = 0; tries = 0
        t = 0.04
        step = 0.92 / max(n-1,1)
        while len(placed) < n and t <= 1.0001:
            dist = t*total; acc = 0
            for (a,bb),L in zip(segs,lens):
                if acc+L >= dist:
                    r = (dist-acc)/L; pt = (a[0]+(bb[0]-a[0])*r, a[1]+(bb[1]-a[1])*r); break
                acc += L
            if math.dist(pt, hub) > 34 and all(math.dist(pt,q) > 24 for q in placed):
                placed.append(pt)
            t += step if math.dist(pt,hub) > 34 else 0.03
        for (x,y),(st,_) in zip(placed, p["stations"]):
            svg.append(f'<g class="st" tabindex="0" role="link" data-line="{E(p["name"])}" data-name="{E(st)}" data-href="paths/{p["slug"]}.html" aria-label="{E(p["name"])}: {E(st)}">'
                       f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" stroke="{p["hex"]}"/></g>')
    svg.append(f'<rect x="{hub[0]-44}" y="{hub[1]-16}" width="88" height="32" rx="16" fill="var(--surface)" stroke="var(--ink)" stroke-width="3"/>'
               f'<text x="{hub[0]}" y="{hub[1]+5}" text-anchor="middle">Central</text>')
    svg.append('</svg>')
    return "".join(svg)

# ---------------------------------------------------------------- pages
def page_index():
    paths_list = "".join(f'''<li style="--lc:{p["color"]}"><h3><a href="paths/{p["slug"]}.html">{E(p["name"])}</a></h3><p>{E(p["summary"])} <span class="muted">· {p["level"]} · {p["hours"]}</span></p></li>''' for p in PATHS)
    feat = ["prompt-engineering-framework","ai-hallucinations-how-to-catch-them","automate-repetitive-work-with-ai","write-an-ai-use-policy","ai-for-small-business-owners","ai-for-nurses-and-healthcare-teams"]
    fg = "".join(f'<div class="panel"><span class="tag">{E(GBY[s]["cat"])}</span><h3><a href="guides/{s}.html">{E(GBY[s]["title"])}</a></h3><p class="muted">{E(GBY[s]["desc"])}</p></div>' for s in feat)
    vids = "".join(video_card(v, "") for v in VIDEOS[:3])
    faq = [("Is AiTrain free?","Yes. All learning lines, guides, prompts, the tools directory and video lessons are free. The site is supported by advertising, sponsors and donations, and by paid team-training programmes."),
           ("Do I need a technical background?","No. The Foundations, Prompt Craft, Workflow Automation, Leaders and Responsible AI lines are written for non-technical people. Only the Build with AI line assumes some coding."),
           ("Which AI tool should I learn?","The skills here work across major assistants. If your employer provides one, learn that one first. Our buyer's checklist helps compare options."),
           ("Can you train my whole team?","Yes. We run live workshops and multi-week programmes built around your team's real tasks. Request a quote on the team training page.")]
    faqh = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faq)
    body = f'''<section class="hero"><div class="wrap hero-in">
<div><h1>Get on board with AI — one practical stop at a time.</h1>
<p class="lede">Free learning lines, guides, prompts and video lessons that teach working people to use AI well. Every line is a route; every station is a skill you can use the same day.</p>
<div class="btn-row"><a class="btn big" href="start-here.html">Find my starting line</a><a class="btn big ghost" href="teams.html">Train my team</a></div>
<div class="hero-stats"><span><b>{len(PATHS)}</b>learning lines</span><span><b>{len(GUIDES)}</b>original guides</span><span><b>{len(PROMPTS)}</b>tested prompts</span><span><b>{len(TOOLS)}</b>tools listed</span></div></div>
<div class="map">{line_map()}<div class="map-cap" id="map-cap" aria-live="polite"><span>Hover or tab to a station to see the skill. Select it to open the line.</span></div></div>
</div></section>
<section class="band"><div class="wrap"><div class="grid g2" style="gap:44px">
<div><h2>Choose a line</h2><p class="muted">Each line is a sequence of short modules. Start at the first station or jump to the one you need.</p><ul class="route">{paths_list}</ul></div>
<div><h2>Most-read guides</h2><div class="grid" style="gap:14px">{fg}</div><p style="margin-top:16px"><a href="guides.html">See all {len(GUIDES)} guides</a></p></div>
</div></div></section>
<section><div class="wrap"><div class="cta-band"><div><h2>Your team bought AI. Now make it stick.</h2><p>Hands-on workshops and rollout programmes built on your team's real tasks, with measurable before-and-after results. Live virtual, on-site or self-paced.</p></div>
<div><a class="btn big" href="teams.html">Get a team quote</a><div class="btn-row" style="margin-top:12px"><a class="btn ghost" href="ai-readiness-quiz.html">Free readiness check</a><a class="btn ghost" href="roi-calculator.html">ROI calculator</a></div></div></div></div></section>
<section><div class="wrap"><div class="sec-head"><h2>Watch and learn</h2><p class="muted">Hand-picked lessons from the best free AI teachers, organised by line.</p></div><div class="grid g3">{vids}</div><p style="margin-top:16px"><a href="videos.html">All video lessons</a></p></div></section>
<section class="band"><div class="wrap grid g3">
<div class="panel"><h3><a href="tools.html">AI tools directory</a></h3><p class="muted">{len(TOOLS)} tools across assistants, research, images, video, meetings, automation and coding — searchable and filterable.</p></div>
<div class="panel"><h3><a href="prompts.html">Prompt library</a></h3><p class="muted">{len(PROMPTS)} copy-ready prompts with fill-in placeholders for writing, data, HR, teaching, marketing and leadership.</p></div>
<div class="panel"><h3><a href="contests.html">Monthly prompt challenge</a></h3><p class="muted">Solve a real-world prompt brief, get feedback, and compete for sponsor-funded prizes.</p></div>
</div></section>
<section><div class="wrap grid g2" style="gap:44px"><div><h2>Questions</h2>{faqh}</div>
<div class="panel"><h2>Keep AiTrain free</h2><p class="muted">Donations fund new lessons, contest prizes, promotion and the contributors who write and review our material.</p><a class="btn" href="support.html">Support AiTrain</a>
<hr style="border:0;border-top:1px solid var(--rule);margin:22px 0"><h3>Advertise or sponsor</h3><p class="muted">Reach professionals actively learning AI: sponsored lines, contests, featured tool listings and newsletter placements.</p><a class="btn ghost" href="advertise.html">See sponsorship options</a></div></div></section>'''
    schema = [{"@context":"https://schema.org","@type":"Organization","name":"AiTrain","url":SITE,"logo":SITE+"/assets/img/favicon.svg"},
              {"@context":"https://schema.org","@type":"WebSite","name":"AiTrain","url":SITE},
              {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}]
    layout("index.html", "AiTrain — Free AI training for working people and teams", "Learn to use AI at work with free learning lines, original guides, a prompt library, AI tools directory and video lessons — plus hands-on AI training for teams.", body, schema)

def video_card(v, b):
    vid, title, ch, line, desc = v
    return f'''<div class="panel"><div class="vid"><button type="button" data-yt="{vid}" aria-label="Play: {E(title)}" style="background-image:url(https://i.ytimg.com/vi/{vid}/hqdefault.jpg)"><span>▶ Play</span></button></div>
<h3 style="margin-top:12px">{E(title)}</h3><p class="muted" style="font-size:.93rem">{E(ch)} · {E(line)}</p><p>{E(desc)}</p></div>'''

def page_paths():
    cards = "".join(f'''<div class="panel path-card" style="--lc:{p["color"]}"><h2 style="font-size:1.4rem"><span class="line-dot" style="color:{p["hex"]}"></span><a href="paths/{p["slug"]}.html">{E(p["name"])}</a></h2>
<p class="meta">{p["level"]} · {p["hours"]} · {len(p["stations"])} stations</p><p>{E(p["summary"])}</p><p class="muted"><b>For:</b> {E(p["who"])}</p><a class="btn ghost" href="paths/{p["slug"]}.html">Board this line</a></div>''' for p in PATHS)
    body = f'''<section><div class="wrap"><div class="sec-head"><h1>Learning lines</h1><p class="lede">Six free routes through practical AI skills. Each station is a short module with a reading, a video or an exercise. Mark your progress and switch lines at Central whenever you like.</p></div>
<div class="map" style="margin-bottom:30px">{line_map()}<div class="map-cap" id="map-cap" aria-live="polite"><span>Hover or tab to a station to preview it.</span></div></div>
<div class="grid g2">{cards}</div></div></section>'''
    layout("paths.html", "AI learning lines: free structured AI courses", "Six free, structured AI learning paths — Foundations, Prompt Craft, Workflow Automation, Build with AI, AI for Leaders and Responsible AI.", body, None, "paths.html")

def path_pages():
    vmap = {v[0]: v for v in VIDEOS}
    for p in PATHS:
        b = "../"
        st = "".join(f'<li style="--lc:{p["color"]}"><h3>Station {i+1}: {E(n)}</h3><p>{E(d)}</p></li>' for i,(n,d) in enumerate(p["stations"]))
        outs = "".join(f"<li>{E(o)}</li>" for o in p["outcomes"])
        gl = "".join(f'<li><a href="../guides/{s}.html">{E(GBY[s]["title"])}</a> <span class="muted">· {GBY[s]["mins"]} min</span></li>' for s in p["guides"] if s in GBY)
        vids = "".join(video_card(vmap[v], b) for v in p["videos"] if v in vmap)
        body = f'''<div class="wrap" style="padding-top:28px">{crumbs(b,[("paths.html","Learning lines"),(None,p["name"])])}
<div class="layout-side"><div>
<h1><span class="line-dot" style="color:{p["hex"]};width:26px;height:26px;border-width:6px"></span>{E(p["name"])}</h1>
<p class="lede">{E(p["summary"])}</p>
<p><span class="tag">{p["level"]}</span><span class="tag">{p["hours"]}</span><span class="tag">{len(p["stations"])} stations</span><span class="tag">Free</span></p>
<p><b>Who it's for:</b> {E(p["who"])}</p>
<h2>What you'll be able to do</h2><ul class="tick">{outs}</ul>
<h2>The route</h2><ol class="route" style="list-style:none">{st}</ol>
<h2>Read along</h2><ul>{gl}</ul>
<div class="ad-space" aria-hidden="true"></div>
<h2>Watch along</h2><div class="grid g2">{vids}</div>
<h2 style="margin-top:36px">How to complete this line</h2>
<p>Work through one station per sitting. For each: read the linked guide, watch the video where one is listed, then apply the idea to one real task from your own work and note the result. When you have done all stations, try the matching brief in this month's <a href="../contests.html">prompt challenge</a>.</p>
</div>
<aside class="side">{team_cta(b, p["name"])}
<div class="panel"><h3>Other lines</h3><ul style="padding-left:18px;margin:0">{"".join(f'<li><a href="{q["slug"]}.html">{E(q["name"])}</a></li>' for q in PATHS if q is not p)}</ul></div></aside>
</div></div>'''
        schema = [{"@context":"https://schema.org","@type":"Course","name":f"{p['name']} — AiTrain","description":p["summary"],
                   "provider":{"@type":"Organization","name":"AiTrain","sameAs":SITE},"isAccessibleForFree":True,
                   "hasCourseInstance":{"@type":"CourseInstance","courseMode":"online","courseWorkload":"PT8H"},
                   "offers":{"@type":"Offer","price":0,"priceCurrency":"USD","category":"Free"}},
                  bc_schema([("paths.html","Learning lines"),(f"paths/{p['slug']}.html",p["name"])])]
        layout(f"paths/{p['slug']}.html", f"{p['name']}: free AI course", f"{p['summary']} {p['level']}, {p['hours']}.", body, schema, "paths.html")

def page_start():
    personas = [
        ("I'm new to AI","Start with how AI works, what it gets wrong, and your first ten prompts.","paths/foundations.html","Foundations Line"),
        ("I use AI but results are hit-and-miss","Learn a repeatable prompt structure and examples-based prompting.","paths/prompt-craft.html","Prompt Craft Line"),
        ("I want hours back every week","Audit your tasks and automate the repetitive ones with AI steps.","paths/workflow-automation.html","Workflow Automation Line"),
        ("I build software","Neural-network intuition through APIs, RAG and evaluation.","paths/build-with-ai.html","Build with AI Line"),
        ("I lead a team or a business","Use cases, policy, pilots, training and ROI.","paths/ai-for-leaders.html","AI for Leaders Line"),
        ("I work in a regulated or public-facing role","Bias, accuracy, disclosure, privacy and security in practice.","paths/responsible-ai.html","Responsible AI Line"),
    ]
    roles = [("Nurses & healthcare","ai-for-nurses-and-healthcare-teams"),("Teachers","ai-for-teachers"),("Small business owners","ai-for-small-business-owners"),
             ("Real estate agents","ai-for-real-estate-agents"),("Marketers","ai-for-marketers"),("HR teams","ai-for-hr-teams"),("Accountants & finance","ai-for-accountants-and-finance")]
    cards = "".join(f'<div class="panel"><h3>{E(a)}</h3><p class="muted">{E(b_)}</p><a class="btn ghost" href="{h}">{E(l)}</a></div>' for a,b_,h,l in personas)
    rl = "".join(f'<a class="tag" style="font-size:.95rem;padding:7px 12px" href="guides/{s}.html">{E(n)}</a>' for n,s in roles)
    body = f'''<section><div class="wrap"><div class="sec-head"><h1>Start here</h1><p class="lede">Pick the sentence that sounds most like you. You can change lines at any time.</p></div>
<div class="grid g3">{cards}</div>
<h2 style="margin-top:48px">Or start from your job</h2><p class="muted">Role playbooks with prompts and the lines not to cross in your profession.</p><div>{rl}</div>
<div class="cta-band" style="margin-top:48px"><div><h2>Choosing for a whole team?</h2><p>Take the free 10-question readiness check to see where your team stands and what to train first.</p></div><div><a class="btn big" href="ai-readiness-quiz.html">Check team readiness</a></div></div>
</div></section>'''
    layout("start-here.html", "Start here: find your AI learning line", "Not sure where to start learning AI? Pick the description that fits you and we'll point you to the right free learning line or role guide.", body, None, "start-here.html")

def page_tools():
    cats = []
    for t in TOOLS:
        if t[1] not in cats: cats.append(t[1])
    btns = '<button type="button" data-cat="all" aria-pressed="true">All</button>' + "".join(f'<button type="button" data-cat="{E(c)}" aria-pressed="false">{E(c)}</button>' for c in cats)
    cards = "".join(f'<div class="panel tool" data-cat="{E(c)}"><div class="cat">{E(c)}</div><h3>{E(n)}</h3><p>{E(d)}</p><p class="muted" style="font-size:.93rem"><b>Best for:</b> {E(bf)}</p><a href="{u}" target="_blank" rel="nofollow noopener">Visit official site</a></div>' for n,c,u,d,bf in TOOLS)
    body = f'''<section><div class="wrap"><div class="sec-head"><h1>AI tools directory</h1><p class="lede">{len(TOOLS)} widely used AI tools, grouped by what they help you do. Listings are informational and independent — we don't accept payment for placement in this list.</p></div>
<div class="filters" data-filter="tlist"><label class="skip" for="tq">Search tools</label><input id="tq" type="search" placeholder="Search tools, e.g. meeting notes">{btns}</div>
<div class="grid g3" id="tlist">{cards}</div><p class="empty" hidden>No tools match. Try another word.</p>
<p class="muted" style="margin-top:20px;font-size:.92rem">Product names are trademarks of their respective owners and are used here for identification only. Features and pricing change often — always check the official site. Read our <a href="guides/how-to-choose-an-ai-assistant.html">buyer's checklist</a> before choosing.</p>
<div class="ad-space" aria-hidden="true"></div>
<div class="grid g2" style="margin-top:30px"><div class="lead-box"><h2>Suggest a tool</h2><p class="muted">Know a tool that belongs here? Tell us. Editorial review is free; sponsored "featured" placements are clearly labelled and listed separately.</p>
<form class="form" data-form="Tool suggestion" data-next="thank-you.html">{hp()}
<div class="row"><div><label for="ts-n">Tool name</label><input id="ts-n" name="tool_name" required></div><div><label for="ts-u">Website</label><input id="ts-u" name="tool_url" type="url" required placeholder="https://"></div></div>
<div class="row"><div><label for="ts-c">Category</label><select id="ts-c" name="category">{"".join(f"<option>{E(c)}</option>" for c in cats)}<option>Other</option></select></div><div><label for="ts-e">Your email</label><input id="ts-e" name="email" type="email" required></div></div>
<div><label for="ts-w">Why it's useful</label><textarea id="ts-w" name="why" required></textarea></div>
<label class="consent"><input type="checkbox" name="interested_in_featured" value="yes"> I'm the maker and interested in a featured (sponsored) listing.</label>
<label class="consent"><input type="checkbox" name="consent" value="yes" required> I agree AiTrain may contact me about this suggestion. <a href="privacy.html">Privacy</a>.</label>
<button class="btn" type="submit">Send suggestion</button><p class="form-msg" role="status"></p></form></div>
{team_cta("", "AI tools rollout")}</div>
</div></section>'''
    schema = {"@context":"https://schema.org","@type":"ItemList","name":"AI tools directory","itemListElement":[{"@type":"ListItem","position":i+1,"name":t[0],"url":t[2]} for i,t in enumerate(TOOLS)]}
    layout("tools.html", "AI tools directory: assistants, research, images, video and automation", f"A searchable directory of {len(TOOLS)} AI tools for work — assistants, research, image, video, meeting, writing, automation and coding tools, with what each is best for.", body, schema, "tools.html")

def page_prompts():
    cats = []
    for p in PROMPTS:
        if p[1] not in cats: cats.append(p[1])
    btns = '<button type="button" data-cat="all" aria-pressed="true">All</button>' + "".join(f'<button type="button" data-cat="{E(c)}" aria-pressed="false">{E(c)}</button>' for c in cats)
    cards = "".join(f'<div class="panel prompt" data-cat="{E(c)}"><div class="tool"><span class="cat">{E(c)}</span></div><h3>{E(t)}</h3><pre id="p{i}">{E(pr)}</pre><button class="copy" type="button" data-copy="p{i}">Copy prompt</button></div>' for i,(t,c,pr) in enumerate(PROMPTS))
    body = f'''<section><div class="wrap"><div class="sec-head"><h1>Prompt library</h1><p class="lede">{len(PROMPTS)} tested prompts that work across major AI assistants. Replace anything in [square brackets] with your details, then paste.</p></div>
<div class="filters" data-filter="plist"><label class="skip" for="pq">Search prompts</label><input id="pq" type="search" placeholder="Search prompts">{btns}</div>
<div class="grid g2" id="plist">{cards}</div><p class="empty" hidden>No prompts match.</p>
<div class="ad-space" aria-hidden="true"></div>
<div class="panel" style="margin-top:30px"><h2>Why these prompts work</h2><p>Each follows the <a href="guides/prompt-engineering-framework.html">five-part structure</a> — role, context, task, constraints and format — and tells the model what to do when information is missing. Learn to write your own on the <a href="paths/prompt-craft.html">Prompt Craft Line</a>, and see how to share them in a <a href="guides/build-a-team-prompt-library.html">team prompt library</a>.</p></div>
</div></section>'''
    layout("prompts.html", "AI prompt library: copy-ready prompts for work", f"{len(PROMPTS)} copy-ready AI prompts with fill-in placeholders for writing, productivity, customer service, marketing, HR, education, data, coding, research and leadership.", body, None, "prompts.html")

def page_videos():
    lines = []
    for v in VIDEOS:
        if v[3] not in lines: lines.append(v[3])
    sec = ""
    for ln in lines:
        sec += f'<h2 style="margin-top:36px">{E(ln)}</h2><div class="grid g3">' + "".join(video_card(v,"") for v in VIDEOS if v[3]==ln) + '</div>'
    body = f'''<section><div class="wrap"><div class="sec-head"><h1>Video lessons</h1><p class="lede">The clearest free AI lessons on YouTube, hand-picked and arranged by learning line. Videos load only when you press play, using YouTube's privacy-enhanced mode.</p></div>
{sec}
<p class="muted" style="margin-top:30px;font-size:.92rem">All videos are embedded through YouTube's standard player and remain the property of their creators. AiTrain is not affiliated with these channels. Creators who prefer not to be featured can <a href="contact.html">contact us</a> and we'll remove the embed.</p>
</div></section>'''
    schema = {"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"https://www.youtube.com/watch?v={v[0]}","name":v[1]} for i,v in enumerate(VIDEOS)]}
    layout("videos.html", "Free AI video lessons, organised by learning line", "Hand-picked free AI video lessons — neural networks, transformers, LLMs, prompting and machine learning — organised into AiTrain learning lines.", body, schema, "videos.html")

def page_glossary():
    gl = sorted(GLOSSARY, key=lambda x: x[0].lower())
    letters = sorted(set(g[0][0].upper() for g in gl))
    az = "".join(f'<a href="#l-{L}">{L}</a>' for L in letters)
    out, cur = "", None
    for t,dfn in gl:
        L = t[0].upper()
        if L != cur:
            out += f'<h2 id="l-{L}" style="margin-top:30px">{L}</h2>'; cur = L
        out += f'<dl class="gloss"><dt id="{re.sub("[^a-z0-9]+","-",t.lower()).strip("-")}">{E(t)}</dt><dd>{E(dfn)}</dd></dl>'
    body = f'''<section><div class="wrap"><div class="sec-head"><h1>AI glossary</h1><p class="lede">{len(GLOSSARY)} AI terms explained in one or two plain sentences.</p></div><div class="az">{az}</div>
<div class="layout-side"><div class="article">{out}</div><aside class="side">{team_cta("", "AI literacy for all staff")}</aside></div></div></section>'''
    schema = {"@context":"https://schema.org","@type":"DefinedTermSet","name":"AiTrain AI glossary","hasDefinedTerm":[{"@type":"DefinedTerm","name":t,"description":d} for t,d in GLOSSARY]}
    layout("glossary.html", "AI glossary: plain-English definitions", f"{len(GLOSSARY)} artificial intelligence terms defined in plain English — from agents and attention to tokens, RAG and zero-shot prompting.", body, schema, None)

def team_form(title="Get a team training quote", sub="Two quick steps. We reply with a tailored outline and quote within 2 business days."):
    sizes = ["1–10","11–50","51–200","201–1,000","1,000+"]
    goals = ["AI basics for all staff","Role-specific skills","Leadership strategy","Policy & compliance (e.g. EU AI Act literacy)","Prompt engineering","Workflow automation","Build with AI (technical)","Custom workshop"]
    fmts = ["Live virtual","On-site","Self-paced with coaching","Hybrid","Not sure yet"]
    tls = ["This month","This quarter","Next 6 months","Just exploring"]
    radios = lambda name, opts, req=True: '<div class="choice">' + "".join(f'<label><input type="radio" name="{name}" value="{E(o)}"{" required" if req and i==0 else ""}><span>{E(o)}</span></label>' for i,o in enumerate(opts)) + '</div>'
    checks = lambda name, opts: '<div class="choice">' + "".join(f'<label><input type="checkbox" name="{name}" value="{E(o)}"><span>{E(o)}</span></label>' for o in opts) + '</div>'
    return f'''<div class="lead-box" id="quote"><h2>{title}</h2><p class="muted">{sub}</p>
<form class="form" data-form="Team training lead" data-next="thank-you.html?f=team" data-steps>{hp()}
<input type="hidden" name="source_topic" value=""><input type="hidden" name="lead_type" value="Team training">
<div class="steps-bar" aria-hidden="true"><span></span><span></span></div>
<div class="step"><div><label for="tf-email">Work email</label><input id="tf-email" type="email" name="email" required autocomplete="email" placeholder="name@company.com"></div>
<fieldset><legend><b>Team size</b></legend>{radios("team_size", sizes)}</fieldset>
<fieldset><legend><b>Main goal</b> <span class="muted">(pick any)</span></legend>{checks("goals", goals)}</fieldset>
<button class="btn big" type="button" data-next-step>Continue</button></div>
<div class="step"><div class="row"><div><label for="tf-name">Your name</label><input id="tf-name" name="name" required autocomplete="name"></div><div><label for="tf-co">Organisation</label><input id="tf-co" name="organisation" required autocomplete="organization"></div></div>
<div class="row"><div><label for="tf-role">Your role</label><input id="tf-role" name="role" placeholder="e.g. Head of Operations"></div><div><label for="tf-country">Country</label><input id="tf-country" name="country" autocomplete="country-name"></div></div>
<fieldset><legend><b>Preferred format</b></legend>{radios("format", fmts)}</fieldset>
<fieldset><legend><b>Timeline</b></legend>{radios("timeline", tls)}</fieldset>
<div class="row"><div><label for="tf-tools">AI tools your team uses</label><input id="tf-tools" name="tools_in_use" placeholder="e.g. ChatGPT, Copilot, Gemini, Claude, none yet"></div><div><label for="tf-phone">Phone (optional)</label><input id="tf-phone" name="phone" type="tel" autocomplete="tel"></div></div>
<div><label for="tf-msg">What should your team be able to do afterwards?</label><textarea id="tf-msg" name="message" placeholder="e.g. Our support team should draft accurate replies in half the time"></textarea></div>
{consent(partner=True)}
<div class="btn-row" style="margin-top:0"><button class="btn ghost" type="button" data-prev-step>Back</button><button class="btn big" type="submit">Request my quote</button></div>
<p class="form-msg" role="status"></p></div>
</form></div>'''

def page_teams():
    progs = [
        ("AI Kickoff Workshop","2–3 hours · live","For any team getting started. How AI works, limits, your policy, the verification habit, and hands-on practice on your real tasks. Ends with a starter prompt library.","AI Kickoff Workshop"),
        ("Role Skills Programme","4–6 weeks · live + practice","Weekly 90-minute sessions for one function (sales, support, HR, finance, marketing, operations, education or healthcare admin), with homework on live work and measured results.","Role Skills Programme"),
        ("Leadership Intensive","Half day · live","For managers and executives: use-case selection, risk, policy, pilot design and how to measure return. Leave with a 90-day plan.","Leadership Intensive"),
        ("Organisation Rollout","3–6 months · blended","Readiness assessment, policy, champions network, waves of role training, completion records for AI-literacy obligations, and quarterly impact reports.","Organisation Rollout"),
    ]
    pc = "".join(f'<div class="panel"><h3>{E(n)}</h3><p class="meta muted">{E(m)}</p><p>{E(d)}</p><a class="btn ghost" href="?topic={E(t)}#quote">Ask about this</a></div>' for n,m,d,t in progs)
    steps = [("Short call","20 minutes to understand your team, tools, policies and goals."),("Tailored outline","A session plan built on your real tasks, with a fixed quote."),("Baseline","We help you capture how long key tasks take today."),("Hands-on training","Practice on real work, not slides. Every attendee leaves with prompts they'll use tomorrow."),("Results report","Before-and-after time, quality and adoption — ready for leadership.")]
    st = "".join(f'<li style="--lc:var(--action)"><h3>{E(a)}</h3><p>{E(b_)}</p></li>' for a,b_ in steps)
    faq = [("How much does team training cost?","It depends on group size, format and how much tailoring you need. Tell us your team size and goals and you'll get a fixed quote within two business days — no obligation."),
           ("Which AI tools do you train on?","Whichever your organisation uses or approves. The core skills transfer across major assistants; examples are built in your own tools."),
           ("Can you help with EU AI Act AI-literacy requirements?","Our foundation module covers the topics organisations commonly use to meet AI-literacy duties, and we provide completion records. We don't provide legal advice; pair the training with your own compliance review."),
           ("Do you train outside North America?","Yes. Live virtual sessions work anywhere; on-site training depends on location."),
           ("Who delivers the training?","AiTrain programmes are delivered by our team and vetted partner trainers with hands-on experience in the relevant role.")]
    fh = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faq)
    body = f'''<section class="hero"><div class="wrap hero-in">
<div><h1>AI training your team will actually use.</h1>
<p class="lede">Hands-on workshops and rollout programmes built around your team's real tasks — so the licences you bought turn into hours saved.</p>
<ul class="tick" style="margin-top:20px"><li>Built on your team's own documents, tools and workflows</li><li>Live virtual, on-site or self-paced with coaching</li><li>Before-and-after measurement of time saved</li><li>Covers policy, privacy and AI-literacy expectations</li><li>Groups from 5 to 1,000+</li></ul>
<div class="btn-row"><a class="btn ghost" href="ai-readiness-quiz.html">Free readiness check</a><a class="btn ghost" href="roi-calculator.html">Estimate your ROI</a></div></div>
{team_form()}</div></section>
<section class="band"><div class="wrap"><div class="sec-head"><h2>Programmes</h2><p class="muted">Start small or roll out across the organisation. Every programme is tailored.</p></div><div class="grid g4">{pc}</div></div></section>
<section><div class="wrap grid g2" style="gap:44px"><div><h2>How it works</h2><ol class="route" style="list-style:none">{st}</ol></div>
<div><h2>Common questions</h2>{fh}
<div class="panel" style="margin-top:24px"><h3>Individual learner?</h3><p class="muted">Use our <a href="guides/get-your-employer-to-pay-for-ai-training.html">email template</a> to ask your manager to fund training, or start free on the <a href="paths.html">learning lines</a>.</p></div></div></div></section>
<section><div class="wrap"><div class="cta-band"><div><h2>Not ready to talk yet?</h2><p>Take the 3-minute readiness check. You'll get a score and the first three things to train.</p></div><div><a class="btn big" href="ai-readiness-quiz.html">Start the check</a></div></div></div></section>'''
    schema = [{"@context":"https://schema.org","@type":"Service","name":"AI training for teams","provider":{"@type":"Organization","name":"AiTrain","url":SITE},"serviceType":"Corporate AI training","areaServed":"Worldwide"},
              {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}]
    layout("teams.html", "AI training for teams and organisations", "Hands-on AI training for teams: kickoff workshops, role-specific programmes, leadership intensives and organisation-wide rollouts with measured results. Get a quote in 2 business days.", body, schema, "teams.html")

def page_quiz():
    qs = [
        ("How many people on your team use an AI assistant at least weekly for work?",["Almost nobody","A few enthusiasts","About half","Most people"]),
        ("Does your organisation have a written AI use policy?",["No","Being drafted","Yes, but few know it","Yes, and people follow it"]),
        ("Is there an approved AI tool people can use with internal information?",["No","Unclear","Yes, for some teams","Yes, for everyone"]),
        ("How do people learn to use AI today?",["They don't","On their own","One-off webinar","Structured, role-based training"]),
        ("How often do people check AI output for facts and figures before sharing?",["Rarely","Sometimes","Usually","Always, it's a habit"]),
        ("Can people name specific tasks AI makes faster for them?",["No","A few can","Many can","Yes, and they share prompts"]),
        ("Does the team share prompts or templates?",["No","Informally","In a few places","A maintained library"]),
        ("Is anything automated with AI steps (e.g. sorting enquiries, summaries)?",["Nothing","Experiments only","One or two workflows","Several, measured"]),
        ("Do you measure time saved or quality from AI?",["No","Anecdotally","For a pilot","Regularly"]),
        ("How confident is leadership about AI risks and opportunities?",["Not at all","Somewhat","Fairly","Very — with a plan"]),
    ]
    qh = "".join(f'<fieldset class="q"><legend>{i+1}. {E(q)}</legend><div class="choice">' + "".join(f'<label><input type="radio" name="q{i}" value="{k}"><span>{E(o)}</span></label>' for k,o in enumerate(opts)) + '</div></fieldset>' for i,(q,opts) in enumerate(qs))
    body = f'''<section><div class="wrap"><div class="layout-side"><div>
<h1>Team AI readiness check</h1><p class="lede">Ten questions, about three minutes. See where your team stands and what to train first. No email needed to see your score.</p>
<form id="quiz" class="panel" style="margin-top:20px">{qh}<button class="btn big" type="submit">See my score</button></form>
<div id="quiz-result" class="result" style="margin-top:28px"><div class="lead-box"><h2>Your readiness</h2><div class="out"></div><div class="meter"><i></i></div><p class="rec"></p>
<p class="muted">Levels: Boarding (just starting) · Moving (pockets of use) · Express (systematic use).</p>
<h3 style="margin-top:20px">Get a free tailored training outline</h3>
<form class="form" data-form="Readiness check lead" data-next="thank-you.html?f=quiz">{hp()}<input type="hidden" id="score-field" name="readiness_score"><input type="hidden" name="source_topic" value="">
<div class="row"><div><label for="qz-n">Name</label><input id="qz-n" name="name" required></div><div><label for="qz-e">Work email</label><input id="qz-e" name="email" type="email" required></div></div>
<div class="row"><div><label for="qz-o">Organisation</label><input id="qz-o" name="organisation" required></div><div><label for="qz-s">Team size</label><select id="qz-s" name="team_size"><option>1–10</option><option>11–50</option><option>51–200</option><option>201–1,000</option><option>1,000+</option></select></div></div>
{consent(partner=True)}<button class="btn big" type="submit">Send me my outline</button><p class="form-msg" role="status"></p></form></div></div>
</div><aside class="side"><div class="panel"><h3>What this measures</h3><ul class="tick"><li>Adoption</li><li>Policy and approved tools</li><li>Training approach</li><li>Verification habits</li><li>Sharing and automation</li><li>Measurement and leadership</li></ul></div>
<div class="panel"><h3>Related</h3><p><a href="guides/ai-adoption-roadmap-for-teams.html">AI adoption roadmap</a><br><a href="guides/write-an-ai-use-policy.html">AI use policy template</a><br><a href="roi-calculator.html">Training ROI calculator</a></p></div></aside></div></div></section>'''
    layout("ai-readiness-quiz.html", "Team AI readiness check (free, 3 minutes)", "Free 10-question AI readiness assessment for teams. Get a score from Boarding to Express and the first three things to train.", body, None, None)

def page_roi():
    body = f'''<section><div class="wrap"><div class="layout-side"><div>
<h1>AI training ROI calculator</h1><p class="lede">Estimate the annual value of training your team to use AI well. Change any number; results update instantly.</p>
<form id="roi" class="panel form" onsubmit="return false" style="margin-top:20px">
<div class="row"><div><label for="people">People trained</label><input id="people" name="people" type="number" min="1" value="25"></div><div><label for="wage">Average hourly cost ($, incl. overhead)</label><input id="wage" name="wage" type="number" min="0" value="45"></div></div>
<div class="row"><div><label for="hours">Hours saved per person per week</label><input id="hours" name="hours" type="number" min="0" step="0.5" value="2"></div><div><label for="adopt">Adoption rate after training (%)</label><input id="adopt" name="adopt" type="number" min="0" max="100" value="70"></div></div>
<div class="row"><div><label for="cost">Training + tools cost per person per year ($)</label><input id="cost" name="cost" type="number" min="0" value="600"></div><div class="muted" style="align-self:end;font-size:.92rem">Assumes 46 working weeks per year.</div></div>
</form>
<div class="grid g2" style="margin-top:20px"><div class="panel"><p class="muted">Estimated annual value</p><div class="out" id="roi-save">—</div></div><div class="panel"><p class="muted">Net value after cost</p><div class="out" id="roi-net">—</div></div>
<div class="panel"><p class="muted">Return multiple</p><div class="out" id="roi-mult">—</div></div><div class="panel"><p class="muted">Hours returned per year</p><div class="out" id="roi-hours">—</div></div></div>
<p class="muted" style="margin-top:14px;font-size:.92rem">This is an estimate for planning, not a guarantee. Measure your real baseline and results using our <a href="guides/measure-ai-productivity.html">measurement guide</a>.</p>
<div class="lead-box" style="margin-top:28px"><h2>Turn the estimate into a plan</h2><p class="muted">Send us your numbers and we'll suggest a programme that targets the biggest time savings.</p>
<form class="form" data-form="ROI calculator lead" data-next="thank-you.html?f=roi">{hp()}<input type="hidden" id="roi-field" name="roi_estimate"><input type="hidden" name="source_topic" value="">
<div class="row"><div><label for="rl-n">Name</label><input id="rl-n" name="name" required></div><div><label for="rl-e">Work email</label><input id="rl-e" name="email" type="email" required></div></div>
<div><label for="rl-o">Organisation</label><input id="rl-o" name="organisation" required></div>
{consent(partner=True)}<button class="btn big" type="submit">Get my training plan</button><p class="form-msg" role="status"></p></form></div>
</div><aside class="side"><div class="panel"><h3>The formula</h3><p class="muted">Annual value = people × adoption × hours saved per week × hourly cost × 46 weeks.</p></div>{team_cta("", "ROI calculator")}</aside></div></div></section>'''
    layout("roi-calculator.html", "AI training ROI calculator for teams", "Estimate the annual value, net return and hours saved from training your team to use AI, with an adjustable calculator.", body, None, None)

def page_contests():
    body = f'''<section><div class="wrap"><div class="layout-side"><div>
<h1>Monthly prompt challenge</h1><p class="lede">One real-world brief each month. Write the prompt (or prompt chain) that solves it best, show the result, and explain your choices. Winners are featured on AiTrain and receive sponsor-funded prizes.</p>
<div class="panel" style="border-left:8px solid var(--l-prompt)"><h2 style="font-size:1.4rem">This round: “The 10-minute board update”</h2>
<p>A non-profit manager has messy notes from five programmes and needs a clear one-page update for the board. Design a prompt or chain that turns raw notes into a board-ready summary with achievements, risks, asks and one chart suggestion — without inventing facts.</p>
<p class="muted"><b>Judged on:</b> accuracy and grounding (40%), usefulness of output (30%), reusability of the prompt (20%), clarity of explanation (10%).</p>
<p class="muted"><b>Round closes:</b> last day of the month, 23:59 Eastern Time. Results within 14 days.</p></div>
<h2>Prizes</h2><p>Prizes are funded by sponsors and supporters. Each round's prize pool — for example gift cards, tool subscriptions or a free seat in a team workshop — is announced on this page before the round opens. Every entrant receives written feedback on one strength and one improvement when entries allow.</p>
<p><a class="btn ghost" href="advertise.html?topic=Contest%20sponsorship">Sponsor a round</a> <a class="btn ghost" href="support.html">Donate to the prize fund</a></p>
<div class="lead-box" style="margin-top:28px"><h2>Submit your entry</h2>
<form class="form" data-form="Contest entry" data-next="thank-you.html?f=contest">{hp()}<input type="hidden" name="round" value="The 10-minute board update">
<div class="row"><div><label for="ce-n">Name or handle</label><input id="ce-n" name="name" required></div><div><label for="ce-e">Email</label><input id="ce-e" name="email" type="email" required></div></div>
<div><label for="ce-p">Your prompt or prompt chain</label><textarea id="ce-p" name="prompt" required style="min-height:160px"></textarea></div>
<div><label for="ce-o">Sample output (use fictional notes)</label><textarea id="ce-o" name="sample_output"></textarea></div>
<div><label for="ce-x">Why it works (max 150 words)</label><textarea id="ce-x" name="explanation" required></textarea></div>
<div class="row"><div><label for="ce-c">Country of residence</label><input id="ce-c" name="country" required></div><div><label for="ce-t">Tool used</label><input id="ce-t" name="tool_used"></div></div>
<label class="consent"><input type="checkbox" name="age_confirm" value="18+" required> I am 18 or older (or the age of majority where I live).</label>
<label class="consent"><input type="checkbox" name="rules" value="accepted" required> I accept the official rules below and confirm the entry is my own work and contains no real personal data.</label>
<button class="btn big" type="submit">Submit entry</button><p class="form-msg" role="status"></p></form></div>
<h2 style="margin-top:36px">Official rules (summary)</h2>
<ol><li>No purchase or payment is necessary to enter or win. Payment does not improve chances of winning.</li>
<li>Open to individuals aged 18+ (or the age of majority in their jurisdiction). Void where prohibited or restricted by law. Each round's page states any excluded jurisdictions — for example, rounds may exclude residents of jurisdictions that require contest registration where the round is not registered.</li>
<li>One entry per person per round. Entries must be original and must not contain real personal, confidential or copyrighted material belonging to others.</li>
<li>Winners are selected by an AiTrain judging panel using the published criteria. Skill-based judging; no random draw. Some jurisdictions may require a skill-testing question before a prize is awarded.</li>
<li>By entering, you grant AiTrain a non-exclusive licence to publish your entry (with credit) on AiTrain.com and its newsletter. You keep ownership.</li>
<li>Prizes are as announced, are non-transferable, and may be substituted with a prize of equal or greater value if unavailable. Taxes are the winner's responsibility.</li>
<li>AiTrain may disqualify entries that break these rules or use automated mass submission. Questions: <a href="contact.html">contact us</a>.</li></ol>
</div><aside class="side"><div class="panel"><h3>Get ready</h3><p><a href="guides/prompt-engineering-framework.html">Five-part prompt</a><br><a href="guides/prompt-chaining-for-long-tasks.html">Prompt chaining</a><br><a href="guides/ai-hallucinations-how-to-catch-them.html">Catching hallucinations</a></p></div>
<div class="panel"><h3>Sponsors</h3><p class="muted">Put your brand in front of motivated AI learners. Rounds can be themed around your product's use case.</p><a class="btn" href="advertise.html?topic=Contest%20sponsorship">Sponsor a round</a></div></aside></div></div></section>'''
    layout("contests.html", "Monthly AI prompt challenge and contests", "Enter AiTrain's monthly AI prompt challenge: solve a real-world brief, get feedback and compete for sponsor-funded prizes. Free to enter.", body, None, "contests.html")

def page_support():
    tiers = [("Supporter","$5","/month or once","Keeps the lights on: hosting, tools and editing.","Supporter"),
             ("Backer","$25","/month or once","Funds one new guide or prompt pack each quarter.","Backer"),
             ("Patron","$100","/month or once","Funds contest prizes and a contributor's review time.","Patron"),
             ("Founding sponsor","$500+","once","Name on our supporters page (optional) and input on what we build next.","Founding sponsor")]
    tc = "".join(f'<div class="panel tier{" featured" if i==1 else ""}"><h3>{n}</h3><div class="amt">{a}</div><p class="muted">{f}</p><p>{d}</p><a class="btn{" ghost" if i!=1 else ""}" href="?plan={E(v)}#pledge">Choose {n}</a></div>' for i,(n,a,f,d,v) in enumerate(tiers))
    alloc = [("Operations","Hosting, editing tools, accessibility testing and fact-checking."),("Promotion & marketing","Reaching more learners through partnerships and outreach."),("Hiring talent","Paying contributing writers, video producers and reviewers."),("Contests & prizes","Prize pools and feedback for the monthly challenge.")]
    al = "".join(f'<div class="panel"><h3>{a}</h3><p class="muted">{b_}</p></div>' for a,b_ in alloc)
    body = f'''<section><div class="wrap"><div class="sec-head"><h1>Support AiTrain</h1><p class="lede">AiTrain keeps its lessons, guides and tools free for everyone. Your support pays for new material, the people who make it, and the prizes that keep learners practising.</p></div>
<div class="grid g4">{tc}</div>
<h2 style="margin-top:44px">Where support goes</h2><div class="grid g4">{al}</div>
<div class="grid g2" style="margin-top:44px;gap:44px"><div class="lead-box" id="pledge"><h2>Make a pledge</h2><p class="muted">Tell us how you'd like to help. We'll reply with a secure payment link (card, PayPal or bank transfer) and a receipt. Nothing is charged by this form.</p>
<form class="form" data-form="Donation pledge" data-next="thank-you.html?f=support">{hp()}
<div class="row"><div><label for="d-n">Name</label><input id="d-n" name="name" required></div><div><label for="d-e">Email</label><input id="d-e" name="email" type="email" required></div></div>
<div class="row"><div><label for="d-t">Level</label><select id="d-t" name="tier"><option>Supporter</option><option>Backer</option><option>Patron</option><option>Founding sponsor</option><option>Custom amount</option></select></div><div><label for="d-a">Amount & currency</label><input id="d-a" name="amount" placeholder="e.g. 50 CAD"></div></div>
<fieldset><legend><b>Frequency</b></legend><div class="choice"><label><input type="radio" name="frequency" value="One-time" required><span>One-time</span></label><label><input type="radio" name="frequency" value="Monthly"><span>Monthly</span></label><label><input type="radio" name="frequency" value="Yearly"><span>Yearly</span></label></div></fieldset>
<fieldset><legend><b>Direct my support to</b> <span class="muted">(optional)</span></legend><div class="choice"><label><input type="checkbox" name="allocate" value="Operations"><span>Operations</span></label><label><input type="checkbox" name="allocate" value="Promotion"><span>Promotion</span></label><label><input type="checkbox" name="allocate" value="Hiring"><span>Hiring talent</span></label><label><input type="checkbox" name="allocate" value="Contests"><span>Contests & prizes</span></label></div></fieldset>
<label class="consent"><input type="checkbox" name="public_credit" value="yes"> You may list my name as a supporter.</label>
<label class="consent"><input type="checkbox" name="consent" value="yes" required> I agree AiTrain may contact me about this pledge. <a href="privacy.html">Privacy</a>.</label>
<button class="btn big" type="submit">Send pledge</button><p class="form-msg" role="status"></p></form></div>
<div><h2>Other ways to help</h2><ul class="tick"><li>Share a guide with a colleague who's starting out.</li><li><a href="contests.html">Enter or sponsor</a> a prompt challenge.</li><li><a href="careers.html">Contribute</a> a guide, review or video.</li><li>Ask your company about <a href="teams.html">team training</a> — it funds the free material.</li><li><a href="advertise.html">Sponsor a learning line</a>.</li></ul>
<details><summary>Is my donation tax-deductible?</summary><p>AiTrain is an independent publication, not a registered charity, so donations are generally not tax-deductible. You'll receive a payment receipt.</p></details>
<details><summary>Can I cancel a monthly pledge?</summary><p>Yes, any time — reply to your receipt or use the contact page.</p></details>
<details><summary>Can my company sponsor instead?</summary><p>Yes. See <a href="advertise.html">sponsorship options</a> for brand recognition packages.</p></details></div></div>
</div></section>'''
    layout("support.html", "Support AiTrain: donate to keep AI learning free", "Support free AI education. Donations fund operations, promotion, contributing talent and contest prizes on AiTrain.", body, None, "support.html")

def page_careers():
    roles = [("Contributing writer — AI guides","Freelance · remote","Write practical, original guides for specific jobs and tools. You have used AI at work and can explain it clearly."),
             ("Video producer","Freelance · remote","Script, record and edit short lessons for our learning lines."),
             ("Partner trainer","Contract · remote or on-site","Deliver AiTrain workshops for teams in your field and region. Training or facilitation experience required."),
             ("Partnerships associate","Commission-based · remote","Introduce organisations to AiTrain team programmes and sponsorships."),
             ("Community moderator","Part-time · remote","Run the monthly challenge, give feedback on entries and keep discussions helpful."),
             ("Technical reviewer","Freelance · remote","Review Build with AI material for accuracy: APIs, retrieval, evaluation and security.")]
    rc = "".join(f'<div class="panel"><h3>{E(a)}</h3><p class="muted">{E(b_)}</p><p>{E(c)}</p><a class="btn ghost" href="#apply" onclick="document.getElementById(\'ap-r\').value=\'{E(a)}\'">Apply</a></div>' for a,b_,c in roles)
    opts = "".join(f"<option>{E(r[0])}</option>" for r in roles)
    body = f'''<section><div class="wrap"><div class="sec-head"><h1>Careers & contributors</h1><p class="lede">We're building the most practical place to learn AI for work, with a small, distributed team of experts. Paid, flexible roles for people who can teach.</p></div>
<div class="grid g3">{rc}</div>
<div class="lead-box" id="apply" style="margin-top:40px;max-width:820px"><h2>Apply or express interest</h2>
<form class="form" data-form="Careers application" data-next="thank-you.html?f=careers">{hp()}
<div class="row"><div><label for="ap-n">Name</label><input id="ap-n" name="name" required></div><div><label for="ap-e">Email</label><input id="ap-e" name="email" type="email" required></div></div>
<div class="row"><div><label for="ap-r">Role</label><select id="ap-r" name="role">{opts}<option>Other</option></select></div><div><label for="ap-l">Location / time zone</label><input id="ap-l" name="location"></div></div>
<div class="row"><div><label for="ap-p">Portfolio or LinkedIn URL</label><input id="ap-p" name="portfolio" type="url" placeholder="https://"></div><div><label for="ap-x">Field or industry expertise</label><input id="ap-x" name="expertise"></div></div>
<div><label for="ap-m">Tell us about something you've taught or explained well</label><textarea id="ap-m" name="message" required></textarea></div>
<label class="consent"><input type="checkbox" name="consent" value="yes" required> I agree AiTrain may keep my application for up to 12 months to consider me for roles. <a href="privacy.html">Privacy</a>.</label>
<button class="btn big" type="submit">Send application</button><p class="form-msg" role="status"></p></form></div>
<p class="muted" style="margin-top:20px">AiTrain welcomes applicants of all backgrounds and evaluates everyone on their work.</p>
</div></section>'''
    layout("careers.html", "Careers and contributor roles", "Paid, flexible contributor roles at AiTrain: writers, video producers, partner trainers, partnerships associates, moderators and technical reviewers.", body, None, None)

def page_advertise():
    opts = [("Sponsored learning line","Your brand presented as the sponsor of a learning line, with a clearly labelled message on every station page."),
            ("Featured tool listing","A labelled 'Featured' placement in the AI tools directory, separate from editorial listings."),
            ("Contest sponsorship","Name a monthly prompt challenge, fund the prizes and set a brief around your use case."),
            ("Newsletter placement","A labelled sponsor slot in the weekly AI skills email."),
            ("Content partnership","Co-created, clearly labelled educational material on how to use your product well."),
            ("Training partnership","Refer or co-deliver team training; revenue share for qualified referrals.")]
    oc = "".join(f'<div class="panel"><h3>{E(a)}</h3><p class="muted">{E(b_)}</p></div>' for a,b_ in opts)
    body = f'''<section><div class="wrap"><div class="sec-head"><h1>Advertise, sponsor & partner</h1><p class="lede">Reach professionals and decision-makers who are actively learning to use AI at work. All sponsored placements are clearly labelled; editorial content is never for sale.</p></div>
<div class="grid g3">{oc}</div>
<div class="grid g2" style="margin-top:40px;gap:44px"><div class="lead-box"><h2>Request the media kit</h2>
<form class="form" data-form="Advertising and sponsorship" data-next="thank-you.html?f=advertise">{hp()}<input type="hidden" name="source_topic" value="">
<div class="row"><div><label for="ad-n">Name</label><input id="ad-n" name="name" required></div><div><label for="ad-e">Work email</label><input id="ad-e" name="email" type="email" required></div></div>
<div class="row"><div><label for="ad-c">Company</label><input id="ad-c" name="company" required></div><div><label for="ad-w">Website</label><input id="ad-w" name="website" type="url" placeholder="https://"></div></div>
<div class="row"><div><label for="ad-i">Interested in</label><select id="ad-i" name="interest">{"".join(f"<option>{E(o[0])}</option>" for o in opts)}<option>Domain / website acquisition</option><option>Other</option></select></div><div><label for="ad-b">Budget range</label><select id="ad-b" name="budget"><option>Under $1,000</option><option>$1,000–$5,000</option><option>$5,000–$20,000</option><option>$20,000+</option><option>Not sure</option></select></div></div>
<div><label for="ad-m">Goals and timing</label><textarea id="ad-m" name="message"></textarea></div>
<label class="consent"><input type="checkbox" name="consent" value="yes" required> I agree AiTrain may contact me about this request. <a href="privacy.html">Privacy</a>.</label>
<button class="btn big" type="submit">Request media kit</button><p class="form-msg" role="status"></p></form></div>
<div><h2>Our standards</h2><ul class="tick"><li>Sponsored content is labelled "Sponsored" or "Featured".</li><li>No sponsor can buy editorial coverage, rankings or changes to guides.</li><li>We don't promote products we believe would mislead learners.</li><li>Google AdSense ads are served automatically and are separate from sponsorships.</li></ul>
<div class="panel" style="margin-top:20px"><h3>Interested in the AiTrain.com domain or website?</h3><p class="muted">For acquisition, investment or white-label partnerships, contact the owner directly.</p><a class="btn" href="https://web.works/contact" target="_blank" rel="noopener">web.works/contact</a></div></div></div>
</div></section>'''
    layout("advertise.html", "Advertise and sponsor on AiTrain", "Sponsor a learning line, contest or newsletter, get a featured tool listing, or partner with AiTrain to reach professionals learning AI.", body, None, None)

def page_contact():
    body = f'''<section><div class="wrap grid g2" style="gap:44px"><div>
<h1>Contact AiTrain</h1><p class="lede">Questions, corrections, partnerships or training requests — we read everything and reply within two business days.</p>
<ul class="tick"><li><a href="teams.html">Team training quote</a> — fastest route for organisations</li><li><a href="advertise.html">Advertising & sponsorship</a></li><li>Domain, website, sponsorship or partnership with the owner: <a href="https://web.works/contact" target="_blank" rel="noopener">web.works/contact</a></li><li>Prefer email? {mail_link("Email AiTrain", "AiTrain.com inquiry")}</li></ul></div>
<div class="lead-box"><h2>Send a message</h2>
<form class="form" data-form="Contact" data-next="thank-you.html">{hp()}
<div class="row"><div><label for="c-n">Name</label><input id="c-n" name="name" required autocomplete="name"></div><div><label for="c-e">Email</label><input id="c-e" name="email" type="email" required autocomplete="email"></div></div>
<div><label for="c-r">Reason</label><select id="c-r" name="reason"><option>General question</option><option>Team training</option><option>Sponsorship / advertising</option><option>Partnership</option><option>Domain / website acquisition</option><option>Correction or feedback</option><option>Copyright or trademark concern</option><option>Press</option></select></div>
<div><label for="c-m">Message</label><textarea id="c-m" name="message" required></textarea></div>
<label class="consent"><input type="checkbox" name="consent" value="yes" required> I agree AiTrain may use these details to reply. <a href="privacy.html">Privacy</a>.</label>
<button class="btn big" type="submit">Send message</button><p class="form-msg" role="status"></p></form></div></div></section>'''
    layout("contact.html", "Contact AiTrain", "Contact AiTrain about team training, sponsorship, advertising, partnerships, corrections or general questions.", body, {"@context":"https://schema.org","@type":"ContactPage","name":"Contact AiTrain"}, None)

def legal(path, title, desc, sections):
    body = f'<section><div class="wrap"><div class="article"><h1>{E(title)}</h1><p class="muted">Last updated: {UPDATED}</p>' + "".join(f'<h2>{E(h)}</h2>{c}' for h,c in sections) + '</div></div></section>'
    layout(path, title, desc, body, None, None)

def legal_pages():
    ask = 'If you have questions, <a href="contact.html">contact us</a>.'
    legal("privacy.html", "Privacy policy", "How AiTrain collects, uses and protects information, including cookies, Google AdSense advertising and form submissions.", [
      ("Who we are", "<p>AiTrain.com (“AiTrain”, “we”) is an independent educational website about artificial intelligence skills. This policy explains what information we collect and how we use it.</p>"),
      ("Information you give us", "<p>When you submit a form — contact, newsletter, team-training request, readiness check, ROI calculator, contest entry, careers application, tool suggestion or donation pledge — we receive the details you enter, such as name, email, organisation and message. We use them only to respond, provide what you requested, and keep records of the request.</p><p>Form submissions are delivered to us through FormSubmit (formsubmit.co), a third-party form-processing service, which processes the data to deliver it by email.</p><p>For team-training requests, if you agree, we may share your request with a vetted training partner solely to prepare a quote or deliver training. We do not sell personal information.</p>"),
      ("Information collected automatically", "<p>Like most websites, our host and service providers process technical data such as IP address, browser type, pages visited and referring pages to deliver and secure the site. Your theme preference and cookie choice are stored in your browser's local storage.</p>"),
      ("Advertising and Google AdSense", "<p>We use Google AdSense to show ads. Third-party vendors, including Google, use cookies to serve ads based on a user's prior visits to this website or other websites. Google's use of advertising cookies enables it and its partners to serve ads to users based on their visit to this site and/or other sites on the Internet.</p><p>You may opt out of personalised advertising by visiting <a href=\"https://adssettings.google.com\" rel=\"noopener\" target=\"_blank\">Google Ads Settings</a>, or opt out of some third-party vendors' use of cookies at <a href=\"https://www.aboutads.info\" rel=\"noopener\" target=\"_blank\">aboutads.info</a>. Learn more in <a href=\"https://policies.google.com/technologies/partner-sites\" rel=\"noopener\" target=\"_blank\">how Google uses information from sites that use its services</a>.</p><p>Visitors in the European Economic Area, the UK and Switzerland may be shown a consent message managed through Google's consent tools before personalised ads are served.</p>"),
      ("Embedded content", "<p>Video lessons are embedded from YouTube using privacy-enhanced mode and load only when you press play. Once loaded, YouTube may collect data under Google's privacy policy. Fonts are loaded from Google Fonts.</p>"),
      ("Email newsletter", "<p>If you subscribe, we use your email only to send the newsletter. Every email includes a way to unsubscribe, and you can ask us to delete your address at any time.</p>"),
      ("How long we keep data", "<p>We keep form submissions for as long as needed to handle your request and for reasonable record-keeping, generally no more than 24 months, unless the law requires longer. Careers applications are kept up to 12 months.</p>"),
      ("Your rights", "<p>Depending on where you live (for example under GDPR, UK GDPR, Canada's PIPEDA, Québec's Law 25 or US state privacy laws), you may have rights to access, correct, delete or port your personal information and to object to or restrict certain processing. To exercise them, <a href=\"contact.html\">contact us</a>. We will respond within the time required by law.</p>"),
      ("Children", "<p>AiTrain is intended for adults and is not directed to children under 13. We do not knowingly collect personal information from children.</p>"),
      ("Security", "<p>The site is served over HTTPS. No online transmission is completely secure, so please don't submit sensitive personal data through our forms.</p>"),
      ("Changes", f"<p>We'll post any changes on this page with a new date. {ask}</p>")])
    legal("terms.html", "Terms of use", "Terms governing use of AiTrain.com content, forms, contests and resources.", [
      ("Acceptance", "<p>By using AiTrain.com you agree to these terms. If you don't agree, please don't use the site.</p>"),
      ("Educational content", "<p>Our guides, learning lines, prompts and tools directory are for general educational purposes. They are not legal, medical, financial or other professional advice. AI tools change quickly; always verify important information with official and qualified sources.</p>"),
      ("Use of content", "<p>You may read, share links to, and print our content for personal or internal training use with attribution. You may copy prompts from the prompt library for your own use. You may not republish substantial parts of the site, frame it, or present it as your own without written permission.</p>"),
      ("Your submissions", "<p>You're responsible for what you submit. Don't submit unlawful content, other people's personal data or material you don't have rights to. Contest entries are licensed to us as described in the contest rules.</p>"),
      ("Third-party links and tools", "<p>We link to third-party websites, tools and videos for convenience. We don't control them and aren't responsible for their content, terms or practices.</p>"),
      ("Training services", "<p>Team training engagements are governed by a separate written agreement or quote. Information on this site does not form a contract.</p>"),
      ("Disclaimer and limitation of liability", "<p>The site is provided “as is” without warranties of any kind. To the extent permitted by law, AiTrain is not liable for any loss arising from use of the site or reliance on its content.</p>"),
      ("Changes", f"<p>We may update these terms by posting a new version here. {ask}</p>")])
    legal("cookies.html", "Cookie policy", "Which cookies and local storage AiTrain uses, including Google AdSense advertising cookies, and how to control them.", [
      ("What we use", "<p><b>Essential local storage:</b> remembers your theme and cookie choice. <b>Advertising cookies:</b> Google AdSense and its partners may set cookies to serve and measure ads, including personalised ads where permitted. <b>Embedded content:</b> YouTube may set cookies after you press play on a video.</p>"),
      ("Your choices", "<p>Use the cookie banner to accept all or essential-only cookies; essential-only requests non-personalised ads. You can also block or delete cookies in your browser settings and manage ad personalisation at <a href=\"https://adssettings.google.com\" target=\"_blank\" rel=\"noopener\">Google Ads Settings</a>.</p>"),
      ("More information", "<p>See our <a href=\"privacy.html\">privacy policy</a>.</p>")])
    legal("disclaimer.html", "Disclaimer", "Important limits on the educational information provided by AiTrain.", [
      ("General information only", "<p>AiTrain publishes general educational content about using artificial intelligence. It is not professional advice. Role guides for regulated professions (such as healthcare, finance, education, real estate and HR) do not replace your employer's policies, your regulator's standards or professional judgement.</p>"),
      ("Accuracy", "<p>We work to keep content accurate and current, but AI products, prices, features and regulations change frequently. Verify anything important with the official source.</p>"),
      ("No endorsement", "<p>Listing a tool, video or organisation is not an endorsement, and inclusion is not paid unless clearly labelled as sponsored or featured.</p>"),
      ("Results", "<p>Examples of time savings and ROI are illustrative estimates. Your results depend on your tasks, tools, people and implementation.</p>")])
    legal("affiliate-disclosure.html", "Affiliate and advertising disclosure", "How AiTrain earns money: advertising, sponsorships, team training, donations and possible affiliate links.", [
      ("How AiTrain is funded", "<p>AiTrain is free to use. We earn revenue from Google AdSense advertising, clearly labelled sponsorships, paid team-training programmes, and donations.</p>"),
      ("Affiliate links", "<p>Some links to third-party products may in future be affiliate links, which means we may earn a commission at no extra cost to you if you buy. Any such link will be disclosed near the link. Commissions never influence our editorial content or directory listings.</p>"),
      ("Sponsored content", "<p>Sponsored or featured placements are always labelled. Sponsors cannot buy editorial coverage or rankings.</p>")])
    legal("editorial-standards.html", "Editorial standards", "How AiTrain researches, writes, reviews and updates its AI learning content.", [
      ("Original, practical, tested", "<p>Every guide is written for AiTrain, based on hands-on use of AI tools in real work. Prompts in the library are tested on multiple assistants before publishing.</p>"),
      ("Accuracy and sources", "<p>We prefer primary sources: official documentation, legislation and peer-reviewed research. Where facts change quickly we say so and avoid stating volatile details such as prices.</p>"),
      ("Use of AI in our own work", "<p>We use AI tools to assist with research, outlining and editing, and every piece is reviewed, fact-checked and edited by a person before publishing. We would not ask you to do anything we don't do ourselves.</p>"),
      ("Independence", "<p>Advertisers and sponsors have no influence over editorial content. Sponsored material is labelled.</p>"),
      ("Corrections", "<p>Spotted an error? <a href=\"contact.html\">Tell us</a>. We correct mistakes promptly and update the page date.</p>")])
    legal("trademark-copyright.html", "Trademark & copyright notice", "AiTrain trademark and copyright disclosure, third-party trademark use, embedded media and how to report concerns.", [
      ("Our name", "<p>“AiTrain” is the name of this independent educational website at AiTrain.com, written as a single coined word. It is used descriptively for AI training content and is not intended to suggest any connection with any other business or mark using similar words.</p>"),
      ("No affiliation", "<p>AiTrain is <b>not</b> affiliated with, sponsored by or endorsed by: any airport or transit operator using the name “AirTrain” (including the Port Authority of New York and New Jersey or the San Francisco International Airport AirTrain); Airtrain.ai or any similarly named AI company; the owner of any “AI+ TRAINING” or similar mark; or any AI developer, including OpenAI, Anthropic, Google, Microsoft or Meta. If you believe our name causes confusion with your mark, please <a href=\"contact.html\">contact us</a> and we will respond promptly.</p>"),
      ("Third-party trademarks", "<p>Product and company names mentioned on this site (for example ChatGPT, Claude, Gemini, Copilot and others in our tools directory) are trademarks or registered trademarks of their respective owners. They are used only to identify those products, in a factual, nominative way. We don't use third-party logos.</p>"),
      ("Copyright", "<p>All original text, prompts, page designs, graphics (including the learning-line map) and code on AiTrain.com are © AiTrain.com. All rights reserved except as allowed in our <a href=\"terms.html\">terms of use</a>.</p>"),
      ("Embedded videos and quoted material", "<p>Video lessons are embedded using YouTube's standard embedding feature and remain the property of their creators; we don't host or copy them. Any short quotations are for commentary and education with attribution.</p>"),
      ("Reporting infringement", "<p>If you believe content on AiTrain infringes your copyright or trademark, use our <a href=\"contact.html\">contact form</a> (choose “Copyright or trademark concern”) with: your contact details, the work or mark concerned, the URL of the material, and a statement of your good-faith belief. We'll review and act promptly.</p>")])

def page_about():
    body = f'''<section><div class="wrap"><div class="article"><h1>About AiTrain</h1>
<p class="lede">AiTrain exists to make working people genuinely good at using AI — safely, practically and without hype.</p>
<p>Most people were handed AI tools with no instructions. Some teams got huge gains; many got nothing, or got burned by a confident wrong answer. The difference is almost always skill: knowing what to ask, what to share, and what to check.</p>
<h2>What we do</h2><ul><li><b>Free learning lines</b> — six structured routes from fundamentals to building AI features.</li><li><b>Original guides</b> — practical how-tos and playbooks for specific jobs.</li><li><b>Resources</b> — a tested prompt library, an independent tools directory, a glossary and curated video lessons.</li><li><b>Team training</b> — hands-on programmes for organisations, delivered by our team and vetted partner trainers.</li></ul>
<h2>Why a transit map?</h2><p>Learning AI isn't one course; it's a network. You might start on the Foundations Line, change at Central to Prompt Craft, and ride Workflow Automation to the end. Every station is a skill you can use that day.</p>
<h2>How we stay free</h2><p>Advertising, labelled sponsorships, team-training programmes and <a href="support.html">supporter donations</a>. Read our <a href="editorial-standards.html">editorial standards</a> and <a href="affiliate-disclosure.html">funding disclosure</a>.</p>
<h2>Get in touch</h2><p><a href="contact.html">Contact us</a>, or for domain, sponsorship, advertising or partnership interest go to <a href="https://web.works/contact" target="_blank" rel="noopener">web.works/contact</a>.</p></div></div></section>'''
    layout("about.html", "About AiTrain", "AiTrain is an independent, free resource that teaches working people and teams to use AI safely and practically.", body, {"@context":"https://schema.org","@type":"AboutPage","name":"About AiTrain"}, None)

def page_thanks():
    body = '''<section><div class="wrap article"><h1>Thanks — it's on its way.</h1><p class="lede">We've received your submission and will reply within two business days.</p>
<ul class="tick"><li>Team requests: check your inbox for a short scheduling email.</li><li>Pledges: you'll receive a secure payment link and receipt.</li><li>Contest entries: results are published within 14 days of the round closing.</li></ul>
<div class="btn-row"><a class="btn" href="paths.html">Keep learning</a><a class="btn ghost" href="prompts.html">Browse prompts</a></div></div></section>'''
    layout("thank-you.html", "Thank you", "Your submission was received.", body.replace('<title>', ''), None, None)
    # noindex
    p = os.path.join(ROOT, "thank-you.html"); s = open(p).read().replace('content="index,follow,max-image-preview:large"', 'content="noindex,follow"'); open(p,"w").write(s)

def page_404():
    body = '''<section><div class="wrap article"><h1>This station doesn't exist.</h1><p class="lede">The page may have moved. Try one of these routes instead.</p>
<div class="btn-row"><a class="btn" href="/index.html">Home</a><a class="btn ghost" href="/paths.html">Learning lines</a><a class="btn ghost" href="/guides.html">Guides</a></div></div></section>'''
    layout("404.html", "Page not found", "Page not found.", body, None, None)
    p = os.path.join(ROOT, "404.html"); s = open(p).read()
    s = s.replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/').replace('href="site.webmanifest"', 'href="/site.webmanifest"')
    s = re.sub(r'href="(?!https?:|/|#|mailto)([a-z0-9\-]+\.html[^"]*)"', r'href="/\1"', s)
    s = s.replace('content="index,follow,max-image-preview:large"', 'content="noindex,follow"')
    open(p,"w").write(s)

def extras():
    w = lambda p, c: open(os.path.join(ROOT, p), "w", encoding="utf-8").write(c)
    w("ads.txt", "google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0\n")
    w("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /_src/\nDisallow: /thank-you.html\n\nSitemap: {SITE}/sitemap.xml\n")
    w("CNAME", "aitrain.com\n")
    w(".nojekyll", "")
    w("site.webmanifest", json.dumps({"name":"AiTrain","short_name":"AiTrain","start_url":"/","display":"standalone","background_color":"#F4F6F9","theme_color":"#1652F0","icons":[{"src":"/assets/img/favicon.svg","sizes":"any","type":"image/svg+xml"}]}, indent=1))
    urls = "".join(f"<url><loc>{SITE}/{'' if p=='index.html' else p}</loc><lastmod>{TODAY}</lastmod><priority>{'1.0' if p=='index.html' else ('0.9' if p in ('teams.html','paths.html') else '0.7')}</priority></url>\n" for p in PAGES)
    w("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    os.makedirs(os.path.join(ROOT,"assets","img"), exist_ok=True)
    w("assets/img/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 34 34">' + LOGO.split('aria-hidden="true">')[1])

if __name__ == "__main__":
    guide_pages(); guides_index(); page_index(); page_paths(); path_pages(); page_start()
    page_tools(); page_prompts(); page_videos(); page_glossary(); page_teams(); page_quiz(); page_roi()
    page_contests(); page_support(); page_careers(); page_advertise(); page_contact(); legal_pages(); page_about()
    page_thanks(); page_404(); extras()
    print(f"Built {len(PAGES)} indexable pages + thank-you + 404")
