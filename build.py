#!/usr/bin/env python3
"""Builds robertahunt.com as plain static HTML.

    python3 build.py            -> docs/     (the real site; GitHub Pages serves this folder)
    python3 build.py --preview  -> preview/  (same pages, links adjusted for an in-chat preview)

Edit the content in this file, run it again, and commit docs/.
Photos go in images/ with the file names listed in IMAGES below; until a file
exists, the page shows a labeled placeholder instead.
"""
import json, os, shutil, sys, html
from datetime import date

PREVIEW = "--preview" in sys.argv
OUT = "preview" if PREVIEW else "docs"
SITE = "https://robertahunt.com"
TODAY = date.today().isoformat()
YEAR = date.today().year
HERE = os.path.dirname(os.path.abspath(__file__))
# Set to True on launch day, after the GoDaddy DNS records point at GitHub Pages.
# While False, the site is reviewable at the github.io address.
USE_CUSTOM_DOMAIN = False

# ---------------------------------------------------------------- shared facts
NAME = "Robert A. Hunt"
TITLE_LINE = "Director of Global Theological Education, SMU Perkins School of Theology"
TITLE_FULL = ("Director of Global Theological Education and Professor of Christian Mission "
              "and Interreligious Relations at SMU's Perkins School of Theology")
BOOK = "All Brain and No Soul?"
BOOK_SUB = "Real Humanity in an AI Age"
BOOK_ORDER = "https://wipfandstock.com/9798385235223/all-brain-and-no-soul/"
BOOK_AMAZON = "https://www.amazon.com/All-Brain-No-Soul-Humanity-ebook/dp/B0DZH75YJL"
SUBSTACK = "https://robertahunt.substack.com/"
LINKS = {  # footer + sameAs, in display order
    "Substack": SUBSTACK,
    "LinkedIn": "https://www.linkedin.com/in/robert-hunt-778aaa10/",
    "Facebook": "https://www.facebook.com/RealHumanity.AIAge",
    "YouTube": "https://www.youtube.com/@InterfaithEncounters",
    "Apple Podcasts": "https://podcasts.apple.com/us/podcast/interfaith-encounters/id1509237395",
    "Amazon author page": "https://www.amazon.com/stores/author/B084D1RTHB",
    "SMU faculty page": "https://www.smu.edu/perkins/facultyacademics/facultylistinga-z/hunt",
}
APPLE = LINKS["Apple Podcasts"]

IMAGES = {  # file in images/ -> (alt text, placeholder label)
    "headshot.jpg": ("Black-and-white portrait of Robert A. Hunt smiling, in a leather jacket, leaning against a tree", "Headshot"),
    "headshot-color.jpg": ("Robert A. Hunt smiling outdoors on a brick-arched campus walkway", "Headshot"),
    "book-cover.jpg": (f"Cover of {BOOK} {BOOK_SUB} by Robert A. Hunt", "Book cover"),
    "book-interior.jpg": (f"Open copies of {BOOK} showing the first page of Chapter 1, Our Place in the World", "Book interior"),
    "speaking.jpg": ("Robert A. Hunt speaking with a microphone to a seated audience, a presentation on the screen behind him", "Speaking photo"),
    "podcast-studio.jpg": (f"Robert A. Hunt in headphones at a microphone recording a podcast, with a copy of {BOOK} on the desk", "Podcast photo"),
    "cover-muslim-faith.jpg": ("Cover of Muslim Faith and Values: A Guide for Christians by Robert A. Hunt", "Book cover"),
    "cover-gospel-nations.jpg": ("Cover of The Gospel Among the Nations: A Documentary History of Inculturation by Robert A. Hunt", "Book cover"),
    "hands.jpg": ("Two hands reaching toward each other against a pink evening sky", "Image"),
}

# ---------------------------------------------------------------- page chrome
PAGES = [  # slug, nav label
    ("", "Home"),
    ("about", "About"),
    ("the-book", "The Book"),
    ("speaking-and-media", "Speaking"),
    ("blog", "Writing"),
    ("real-humanity-ai-podcasts", "Podcasts"),
    ("contact", "Contact"),
]

def href(slug):
    if PREVIEW:
        return "index.html" if slug == "" else f"{slug}.html"
    # Relative links work both at robertahunt.com and at the github.io review address.
    return "./" if slug == "" else slug

def esc(s):
    return html.escape(s, quote=True)

def img(name, cls, eager=False):
    alt, label = IMAGES[name]
    path = os.path.join(HERE, "images", name)
    if os.path.exists(path):
        from PIL import Image
        w, h = Image.open(path).size
        lazy = "" if eager else ' loading="lazy"'
        return (f'<figure class="{cls}"><img src="images/{name}" alt="{esc(alt)}" width="{w}" height="{h}"'
                f'{lazy} decoding="async"></figure>')
    return (f'<figure class="{cls}"><div class="placeholder" role="img" aria-label="{esc(alt)}">'
            f'{label}<br>goes here</div></figure>')

def ld(obj):
    return ('<script type="application/ld+json">\n'
            + json.dumps({"@context": "https://schema.org", "@graph": obj}, indent=2, ensure_ascii=False)
            + "\n</script>")

PERSON_REF = {"@id": f"{SITE}/#person"}
PERSON = {
    "@type": "Person",
    "@id": f"{SITE}/#person",
    "name": NAME,
    "honorificPrefix": "Dr.",
    "url": f"{SITE}/",
    "image": f"{SITE}/images/headshot.jpg",
    "jobTitle": ["Director of Global Theological Education",
                 "Professor of Christian Mission and Interreligious Relations"],
    "description": ("Author, speaker and SMU professor writing on artificial intelligence, "
                    "faith and what it means to be human."),
    "worksFor": {"@type": "CollegeOrUniversity",
                 "name": "Southern Methodist University, Perkins School of Theology",
                 "url": "https://www.smu.edu/perkins"},
    "alumniOf": [
        {"@type": "CollegeOrUniversity", "name": "University of Malaya"},
        {"@type": "CollegeOrUniversity", "name": "Southern Methodist University"},
        {"@type": "CollegeOrUniversity", "name": "The University of Texas at Austin"},
    ],
    "knowsAbout": ["Artificial intelligence and ethics", "Theological anthropology",
                   "Christian-Muslim relations", "Interreligious dialogue",
                   "AI in higher education", "Christian mission"],
    "sameAs": list(LINKS.values()),
}
BOOK_LD = {
    "@type": "Book",
    "@id": f"{SITE}/the-book#book",
    "name": BOOK,
    "alternateName": f"{BOOK} {BOOK_SUB}",
    "author": PERSON_REF,
    "publisher": {"@type": "Organization", "name": "Wipf and Stock Publishers"},
    "datePublished": "2025-02-24",
    "numberOfPages": 214,
    "isbn": "9798385235223",
    "inLanguage": "en",
    "url": f"{SITE}/the-book",
    "image": f"{SITE}/images/book-cover.jpg",
    "workExample": [
        {"@type": "Book", "bookFormat": "https://schema.org/Paperback"},
        {"@type": "Book", "bookFormat": "https://schema.org/Hardcover"},
        {"@type": "Book", "bookFormat": "https://schema.org/EBook"},
        {"@type": "Book", "bookFormat": "https://schema.org/AudiobookFormat", "readBy": PERSON_REF},
    ],
    "offers": {"@type": "Offer", "url": BOOK_ORDER, "availability": "https://schema.org/InStock"},
}
WEBSITE = {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/",
           "name": NAME, "publisher": PERSON_REF, "inLanguage": "en"}

def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip_tags(q),
         "acceptedAnswer": {"@type": "Answer", "text": " ".join(strip_tags(p) for p in a)}}
        for q, a in items]}

def strip_tags(s):
    import re
    return re.sub(r"<[^>]+>", "", s)

def faq_html(items):
    out = []
    for q, a in items:
        body = "".join(f"<p>{p}</p>" for p in a)
        out.append(f"<details><summary>{q}</summary><div>{body}</div></details>")
    return '<div class="faq">' + "".join(out) + "</div>"

def page(slug, title, description, body, graph=None):
    canonical = f"{SITE}/" if slug == "" else f"{SITE}/{slug}"
    nav = "".join(
        f'<li><a href="{href(s)}"{" aria-current=\"page\"" if s == slug else ""}>{label}</a></li>'
        for s, label in PAGES)
    foot_links = "".join(f'<li><a href="{u}" rel="me">{esc(n)}</a></li>' for n, u in LINKS.items())
    banner = ('<div class="preview-banner">Draft preview of the new robertahunt.com. '
              'Photos, forms and some details are placeholders.</div>') if PREVIEW else ""
    head = f"""<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/images/headshot.jpg">
<meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Belleza&family=Lato:ital,wght@0,400;0,700;1,400&display=swap">
<link rel="stylesheet" href="style.css">
<link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32.png">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
<meta name="theme-color" content="#281e38">
{ld(graph) if graph else ""}"""
    content = f"""{banner}<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{href('')}"><img class="logo-light" src="images/logo-horizontal.png" alt="Robert A. Hunt, Author" width="274" height="60"><img class="logo-dark" src="images/logo-horizontal-white.png" alt="Robert A. Hunt, Author" width="274" height="60"></a>
    <nav class="site-nav" aria-label="Main"><ul>{nav}</ul></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div>
      <img class="footer-logo" src="images/logo-horizontal-white.png" alt="Robert A. Hunt, Author" width="274" height="60">
      <p><strong>Dr. Robert A. Hunt</strong><br>{TITLE_FULL}.</p>
      <p>&copy; {YEAR} Robert A. Hunt. Last updated <time datetime="{TODAY}">{date.today():%B %-d, %Y}</time>.</p>
    </div>
    <div>
      <p class="eyebrow" style="color:var(--footer-muted)">Elsewhere</p>
      <ul>{foot_links}</ul>
    </div>
  </div>
</footer>
<script>
document.querySelectorAll("form[data-endpoint]").forEach(function (f) {{
  f.addEventListener("submit", function (e) {{
    if (!f.dataset.endpoint) {{
      e.preventDefault();
      var n = f.querySelector(".form-note");
      if (n) {{ n.hidden = false; n.textContent = "This form isn't connected yet. It will start delivering messages when the new site goes live."; }}
    }}
  }});
}});
</script>"""
    if PREVIEW and slug == "":
        # The preview host supplies the document skeleton for the main page.
        return head + "\n" + content
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head}
</head>
<body>
{content}
</body>
</html>
"""

# ---------------------------------------------------------------- content
HOME_OPENING = (
    "Dr. Robert A. Hunt helps churches, universities, and civic and business leaders think "
    "clearly about staying human as AI reshapes work, faith and relationships. He directs "
    "Global Theological Education at SMU's Perkins School of Theology and is the author of "
    f"<cite>{BOOK} {BOOK_SUB}</cite> (Wipf and Stock, 2025).")

def home():
    body = f"""
<div class="wrap">
  <section class="hero" aria-labelledby="hero-q">
    <div>
      <p class="eyebrow">Author &middot; Speaker &middot; SMU Perkins professor</p>
      <h1 id="hero-q" class="hero-question">So what are we humans becoming in an <span>AI age?</span></h1>
      <p class="lede">{HOME_OPENING}</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="{href('speaking-and-media')}#invite">Invite Dr. Hunt to speak</a>
        <a class="btn btn-ghost" href="{href('the-book')}">About the book</a>
      </div>
    </div>
    {img("headshot.jpg", "portrait", eager=True)}
  </section>
</div>

<section class="section">
  <div class="wrap split">
    {img("book-cover.jpg", "cover")}
    <div>
      <p class="eyebrow">The book &middot; Wipf and Stock, 2025</p>
      <h2>{BOOK} <span class="muted" style="font-weight:500">{BOOK_SUB}</span></h2>
      <div class="prose" style="margin-top:1rem">
        <p>How AI and technological change challenge what it means to be human. Drawing on history, science and philosophy, the book traces a story that runs from Copernicus and Darwin to today's chatbots, and argues that the real task of the AI age is to renew our humanity through community, imagination and spiritual connection.</p>
        <p>Written for thoughtful general readers, church classes, book groups and university courses. No technical background needed.</p>
      </div>
      <div class="hero-actions">
        <a class="btn btn-primary" href="{BOOK_ORDER}">Order from Wipf and Stock</a>
        <a class="btn btn-ghost" href="{href('the-book')}">Read more</a>
      </div>
      <p class="muted" style="margin-top:0.9rem;font-size:0.93rem">Use code <strong>CONF40</strong> for 40% off at Wipf and Stock.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split" style="align-items:center">
    {img("hands.jpg", "photo square")}
    <figure class="quote">
      <blockquote><p>With the advent of AI, there is something new in our world&mdash;a technology we created that pretends to be like us in the ways that seem most uniquely human.</p></blockquote>
      <footer>From <cite>{BOOK}</cite></footer>
    </figure>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Ways to engage</p>
      <h2>Read, listen or bring him in</h2>
    </div>
    <div class="grid">
      <article class="card">
        <p class="meta">Speaking</p>
        <h3><a href="{href('speaking-and-media')}">Talks, classes and keynotes</a></h3>
        <p>Recent audiences include SMU's Industrial Advisory Council, the University of Birmingham, the Center for Brain Health and dozens of Dallas congregations.</p>
      </article>
      <article class="card">
        <p class="meta">Weekly essays</p>
        <h3><a href="{SUBSTACK}">Robert's Substack</a></h3>
        <p>New writing every week on AI, ethics and human identity. Subscribe free to get each essay by email.</p>
      </article>
      <article class="card">
        <p class="meta">Op-eds</p>
        <h3><a href="{href('blog')}#op-eds">In the press</a></h3>
        <p>Commentary in Fox News, The Hill, The Dallas Morning News, the Austin American-Statesman and the Fort Worth Star-Telegram.</p>
      </article>
      <article class="card">
        <p class="meta">Podcasts</p>
        <h3><a href="{href('real-humanity-ai-podcasts')}">Real Humanity in an AI Age</a></h3>
        <p>Two podcast series from Interfaith Encounters, including conversations with Gen Z students of several faiths.</p>
      </article>
    </div>
  </div>
</section>
"""
    return page("", "Dr. Robert A. Hunt | AI, Faith & Being Human | SMU",
                "Dr. Robert A. Hunt, SMU Perkins professor and author of All Brain and No Soul?, "
                "speaks and writes on AI, faith and what it means to be human.",
                body, [PERSON, BOOK_LD, WEBSITE])

def about():
    body = f"""
<div class="wrap">
  <header class="page-head split">
    {img("headshot-color.jpg", "portrait", eager=True)}
    <div>
      <p class="eyebrow">About</p>
      <h1>Dr. Robert A. Hunt</h1>
      <p class="lede">{TITLE_FULL}, and author of <cite>{BOOK} {BOOK_SUB}</cite>.</p>
      <div class="prose" style="margin-top:1.25rem">
        <p>My mission is to promote authentic humanity in changing times, particularly as we enter the AI age. We all have something valuable to offer others and our world if together we embrace our humanity and that of others. We discover our humanity through curiosity about our world and ourselves, critical and appreciative study, open dialogue, and a willingness to learn.</p>
      </div>
    </div>
  </header>
</div>

<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">My story</p><h2>Forty-five years of teaching across cultures</h2></div>
    <div class="prose">
      <p>Raised in Texas, I lived and worked for more than 20 years in Malaysia, Singapore, Austria and Eastern Europe. I earned my PhD at the University of Malaya, focusing on Christian-Muslim relations, and I have 45 years of experience teaching about different religions and cultures. I have loved every minute: learning new things and contributing to mutual respect and understanding.</p>
      <p>The focus of my professional life as a teacher has been interpretation: helping people understand themselves, their history, and the cultures, religions and social movements that shape their human experience. In an age that is increasingly artificial and two-dimensional, I believe every person, culture and society should be seen in all its fullness and complexity.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">The work</p><h2>Why the humanities matter in the AI age</h2></div>
    <div class="prose">
      <p>Robert Hunt's career bridges theology, history and global education, with a sustained focus on what it means to remain deeply human in a rapidly changing world. His work insists that the humanities are the foundation of leadership in every sphere, from business to politics to science. AI can process information faster than any person, but it cannot model the most essential lesson: how to be a human among other humans.</p>
      <p>He holds degrees from The University of Texas at Austin (BA), Southern Methodist University (MDiv) and the University of Malaya (PhD in history), and has taught and led programs across Southeast Asia, Europe and the United States, from developing continuing education in Malaysia and Singapore to directing global theological education at SMU. He edits the American Society of Missiology Monograph Series.</p>
      <p>Across all of it, his scholarship asks how communities can orient themselves toward dignity and flourishing: protecting the human space for meaning-making, truth-seeking and community-building, even as AI becomes part of our world of relationships.</p>
    </div>
    <dl class="facts">
      <dt>Role</dt><dd>{TITLE_FULL}</dd>
      <dt>Education</dt><dd>PhD, University of Malaya (1994); MDiv, SMU (1982); BA, UT Austin (1977)</dd>
      <dt>Based in</dt><dd>Dallas, Texas</dd>
      <dt>Topics</dt><dd>AI and human identity; AI ethics; faith and technology; AI in higher education; interreligious dialogue</dd>
    </dl>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Books</p><h2>Selected books</h2></div>
    <div class="grid">
      <article class="card">
        {img("book-cover.jpg", "thumb")}
        <p class="meta">2025 &middot; Wipf and Stock</p>
        <h3><a href="{href('the-book')}">{BOOK} {BOOK_SUB}</a></h3>
        <p>How AI and the scientific revolutions before it reshape human identity, and how we can renew our humanity in response.</p>
      </article>
      <article class="card">
        {img("cover-gospel-nations.jpg", "thumb")}
        <p class="meta">Documentary history</p>
        <h3><a href="https://www.amazon.com/Gospel-Among-Nations-Documentary-Inculturation-ebook/dp/B00JJWD1GA">The Gospel Among the Nations: A Documentary History of Inculturation</a></h3>
        <p>The key primary documents showing how Christians have translated the gospel into new cultural settings.</p>
      </article>
      <article class="card">
        {img("cover-muslim-faith.jpg", "thumb")}
        <p class="meta">Guide</p>
        <h3><a href="https://www.amazon.com/Muslim-Faith-Values-Guide-Christians-ebook/dp/B083G7HK3R">Muslim Faith and Values: A Guide for Christians</a></h3>
        <p>An introduction to Islamic belief and practice, written to help Christians understand and love their Muslim neighbors.</p>
      </article>
    </div>
    <p style="margin-top:1.5rem"><a href="https://img1.wsimg.com/blobby/go/0ed6750d-2355-4f0d-ab1c-d5d60e41efec/CV%20robert%20hunt%202025%20-%20Academic.pdf">Academic CV (PDF)</a></p>
  </div>
</section>
"""
    return page("about", "About Dr. Robert A. Hunt | SMU Perkins",
                "Dr. Robert A. Hunt directs Global Theological Education at SMU Perkins. After 20 years "
                "teaching in Malaysia, Singapore and Vienna, he speaks and writes on AI and human identity.",
                body, [PERSON])

BOOK_FAQ = [
    ("Who is <cite>All Brain and No Soul?</cite> written for?", [
        "It is written for thoughtful general readers, especially people of faith, who want to understand AI without hype or fear. You do not need a technical background. Dr. Hunt explains how large language models work and where they fall short, then places AI in a longer story that runs from Copernicus and Darwin to today's chatbots and brain-computer interfaces."]),
    ("Can a church class or book group use it?", [
        "Yes. Church classes, book groups and university courses use it to ask what makes us human when machines can talk like us. The six chapters work well as a six-week series. Dr. Hunt has taught classes on the book at Highland Park, University Park, Lovers Lane and Lake Highlands UMC, among others, and can visit or join your group by video. <a href=\"" + href("contact") + "\">Get in touch</a> to arrange it."]),
    ("What formats is it available in?", [
        "Hardcover, paperback, Kindle, and an 8-hour audiobook read by the author. The book is 214 pages, published by Wipf and Stock in 2025."]),
    ("Where can I buy it?", [
        "Order directly from <a href=\"" + BOOK_ORDER + "\">Wipf and Stock</a> with code CONF40 for 40% off, or from <a href=\"" + BOOK_AMAZON + "\">Amazon</a>. A free preview is available on Google Books."]),
    ("Is the book against AI?", [
        "No. It treats AI as a powerful technology with real limits. The book argues that the real challenge is not AI replacing us but whether we keep practicing the things that make us human: community, imagination and spiritual connection."]),
]

def the_book():
    chapters = ["Our Place in the World", "The Screen Age", "Calculators to Computers to AI",
                "How It Works", "Limits of Generative AI", "Children of the AI Age"]
    ch = "".join(f"<li>{c}</li>" for c in chapters)
    body = f"""
<div class="wrap">
  <header class="page-head split">
    {img("book-cover.jpg", "cover", eager=True)}
    <div>
      <p class="eyebrow">The book</p>
      <h1>{BOOK}</h1>
      <p class="lede" style="font-family:var(--display);font-style:italic;margin-top:0.4rem">{BOOK_SUB}</p>
      <div class="prose" style="margin-top:1.25rem">
        <p>Artificial intelligence forces us to reconsider what it means to be human. Dr. Hunt traces that question through the Copernican and Darwinian revolutions to the arrival of generative AI. Rather than treating AI as the end of humanity, he argues that our real challenge is to rekindle our humanity through community, imagination and spiritual connection.</p>
      </div>
      <div class="hero-actions">
        <a class="btn btn-primary" href="{BOOK_ORDER}">Order from Wipf and Stock</a>
        <a class="btn btn-ghost" href="{BOOK_AMAZON}">Buy on Amazon</a>
      </div>
      <p class="muted" style="margin-top:0.9rem;font-size:0.93rem">Use code <strong>CONF40</strong> for 40% off at Wipf and Stock.</p>
      <dl class="facts">
        <dt>Author</dt><dd>Robert A. Hunt</dd>
        <dt>Publisher</dt><dd>Wipf and Stock Publishers</dd>
        <dt>Published</dt><dd>February 24, 2025</dd>
        <dt>Pages</dt><dd>214</dd>
        <dt>Formats</dt><dd>Hardcover, paperback, Kindle, audiobook (8 hours, read by the author)</dd>
        <dt>ISBN</dt><dd>9798385235223</dd>
      </dl>
    </div>
  </header>
</div>

<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Contents</p><h2>Six chapters</h2></div>
    <ol class="chapters">{ch}</ol>
    {img("book-interior.jpg", "photo wide")}
  </div>
</section>

<section class="section">
  <div class="wrap" style="display:grid;gap:2.5rem">
    <figure class="quote">
      <blockquote><p>[The book] calls for our churches and homes to become centers of humanization&mdash;sanctuaries where we nurture the essence of our humanity in an AI age.</p></blockquote>
      <footer>Drew Dickens, host of the <cite>AI &amp; Spirituality</cite> podcast</footer>
    </figure>
    <figure class="quote">
      <blockquote><p>[It] offers a nuanced and comprehensive overview of generative AI.</p></blockquote>
      <footer>Gary Brubaker, Director, SMU Guildhall, Southern Methodist University</footer>
    </figure>
    <figure class="quote">
      <blockquote><p>The way to enrich our humanity is by being human with humans, even if that process is emotionally demanding and the demand comes from someone half our age.</p></blockquote>
      <footer>From the book</footer>
    </figure>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Questions</p><h2>About the book</h2></div>
    {faq_html(BOOK_FAQ)}
  </div>
</section>
"""
    return page("the-book", f"{BOOK} {BOOK_SUB} | Robert A. Hunt",
                f"{BOOK} {BOOK_SUB} by Dr. Robert A. Hunt (Wipf and Stock, 2025): what AI means for "
                "human identity, for general readers and church classes. Formats, contents and where to buy.",
                body, [BOOK_LD, PERSON, faq_ld(BOOK_FAQ)])

TALKS = [
    ("AI and the Copernican Revolution in Intelligence",
     "How AI joins Copernicus and Darwin as a revolution that changes where humans think they stand, and what that means for how we understand ourselves.",
     "Lecture series, general audiences"),
    ("Intelligence, Consciousness and Soul: Negotiating Humanity in an AI Age",
     "What machines can and cannot do, and why the difference matters for faith, relationships and what we teach our children.",
     "Churches, adult classes, women's and men's fellowships"),
    ("AI Impacts and Possibilities",
     "A clear-eyed briefing on where generative and agentic AI are heading, and the human judgment leaders still have to supply.",
     "Business, civic and advisory boards"),
    ("AI in the Future of Education",
     "How AI can strengthen teaching in the humanities, including custom chatbots that bring historical voices into the classroom.",
     "Universities, faculty development, schools"),
]
UPCOMING = [
    ("2026-10-16", "October 16, 2026", "AI and the Copernican Revolution in Intelligence",
     "Frontiers of Brain Health lecture series, Center for Brain Health, University of Texas at Dallas"),
    ("2026-10-28", "October 28, 2026", "Intelligence, Consciousness and Soul: Negotiating Humanity in an AI Age",
     "Leadership First Alumnae Symposium, First UMC Richardson"),
    ("2026-11-08", "November 8 and 15, 2026", "Social Media, Artificial Intelligence, and the Challenge of Evangelism and Ministry in a Digital Age",
     "The Fellowship Class, Highland Park UMC, 9:30 am"),
    ("2027-03-09", "March 9, 2027", "To Serve the Present Age: The Challenge of AI in Ministry",
     "World Parish webinar (online)"),
]
PAST = [
    ("2026-08-10", "Aug 10, 2026", "Living as humans in an ecosystem of intelligences", "Interdisciplinary AI Network, University of Birmingham, UK"),
    ("2026-04-16", "Apr 16, 2026", "AI and Real Humanity", "The Forum at Park Lane, Dallas"),
    ("2026-04-14", "Apr 14, 2026", "Faith and Artificial Intelligence (moderator)", "SMU Center for Faith and Learning interfaith panel"),
    ("2026-03-28", "Spring 2026", "AI and Real Humanity: church classes", "Highland Park, University Park, Lovers Lane, Lake Highlands and First UMC Richardson; Christ the King Lutheran; UMC Women of Faith regional gathering; Preston Hollow Men's Fellowship"),
    ("2026-02-26", "Feb 26, 2026", "AI and Real Humanity", "Dallas civic and business leaders, The Thanksgiving Foundation, hosted by Kyle Ogden"),
    ("2025-11-17", "Nov 17–18, 2025", "Workshops on AI and humanity, and using AI to teach the humanities", "Beijing Academy of Educational Sciences, at SMU"),
    ("2025-11-12", "Nov 12, 2025", "Living for Others (panel with Dr. George Mason and Rabbi Steve Gutow)", "Dialogue Dallas"),
    ("2025-10-24", "Oct 24, 2025", "AI Impacts and Possibilities", "SMU Industrial Advisory Council, Moody Graduate School"),
    ("2025-09-09", "Sep 9, 2025", "The Meaning of AI in a Multi-faith Society", "Dialogue Institute of Dallas"),
    ("2025-07-11", "Jul 11, 2025", "Technology, Humanity, and Identity (workshop with Dr. Kate Montgomery)", "European Conference on Arts and Humanities, London"),
    ("2025-05-28", "May 28, 2025", "Speaker for the Dead: Bespoke AI Chatbots for Student Engagement", "Conference on Teaching and Learning with AI, Orlando"),
    ("2025-05-23", "May 23, 2025", "AI in Professional Life (panel)", "Conference of the Professionals, Scottish Rite Hospital, Dallas"),
    ("2025-05-20", "May 20, 2025", "AI in Higher Education", "SMU Provost's Symposium on AI"),
    ("2025-05-12", "May 12, 2025", "AI in the Future of Education (keynote)", "SMU Town and Gown Symposium"),
    ("2024-09-24", "Sep 24, 2024", "AI and Humanity (keynote and panel)", "BigBang! Conference, Social Venture Partners Dallas"),
]
SPEAK_FAQ = [
    ("What kinds of groups does Dr. Hunt speak to?", [
        "Congregations and adult Sunday school classes, universities and faculty groups, business and civic leaders, and interfaith audiences. Recent hosts include SMU's Industrial Advisory Council, the University of Birmingham, the Center for Brain Health at UT Dallas and many Dallas-area churches."]),
    ("Does he speak online or travel?", [
        "Both. He speaks in person across North Texas, has traveled to engagements in London, Birmingham and Orlando, and presents online by webinar or video call."]),
    ("What formats are available?", [
        "Keynotes, single lectures, multi-week classes, workshops, panels and moderated discussions. Sessions usually include time for questions, which audiences tend to make the best part."]),
    ("How do I book him?", [
        "Use the <a href=\"#invite\">speaking request form</a> below with your date, audience and format. He will reply to discuss topic and logistics."]),
]

def speaking():
    talks = "".join(f'<article class="card"><p class="meta">{esc(a)}</p><h3>{esc(t)}</h3><p>{esc(d)}</p></article>' for t, d, a in TALKS)
    up = "".join(f'<li><time datetime="{iso}">{esc(d)}</time><div><h3>{esc(t)}</h3><p>{esc(w)}</p></div></li>' for iso, d, t, w in UPCOMING)
    past = "".join(f'<li><time datetime="{iso}">{esc(d)}</time><div><h3>{esc(t)}</h3><p>{esc(w)}</p></div></li>' for iso, d, t, w in PAST)
    events_ld = [{"@type": "Event", "name": t, "startDate": iso, "description": w,
                  "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode" if "online" in w.lower() else "https://schema.org/OfflineEventAttendanceMode",
                  "performer": PERSON_REF,
                  "location": ({"@type": "VirtualLocation", "url": f"{SITE}/speaking-and-media"} if "online" in w.lower()
                               else {"@type": "Place", "name": w, "address": {"@type": "PostalAddress", "addressRegion": "TX", "addressCountry": "US"}})}
                 for iso, d, t, w in UPCOMING]
    body = f"""
<div class="wrap">
  <header class="page-head">
    <p class="eyebrow">Speaking and media</p>
    {img("speaking.jpg", "photo banner", eager=True)}
    <h1>Invite Dr. Hunt to speak</h1>
    <p class="lede">Talks, classes and keynotes on AI, ethics and human identity for churches, universities, and business and civic leaders. Clear explanations of how AI works, honest about its limits, and grounded in what it means to be human.</p>
    <div class="hero-actions"><a class="btn btn-primary" href="#invite">Request a talk</a><a class="btn btn-ghost" href="#upcoming">See upcoming events</a></div>
  </header>
</div>

<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Signature talks</p><h2>Topics</h2><p class="muted">Each can be shaped for a keynote, a single session or a multi-week class.</p></div>
    <div class="grid">{talks}</div>
  </div>
</section>

<section class="section" id="upcoming">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Upcoming</p><h2>Where to hear him next</h2></div>
    <ul class="dated">{up}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Recent</p><h2>Recent engagements</h2></div>
    <ul class="dated">{past}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Questions</p><h2>Booking a talk</h2></div>
    {faq_html(SPEAK_FAQ)}
  </div>
</section>

<section class="section" id="invite">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Speaking request</p><h2>Tell us about your event</h2><p class="muted">Dr. Hunt will reply by email to discuss topic, format and logistics.</p></div>
    <form class="form" method="post" action="" data-endpoint="">
      <div class="row">
        <div class="field"><label for="sr-name">Your name</label><input id="sr-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="sr-email">Email</label><input id="sr-email" name="email" type="email" autocomplete="email" required></div>
      </div>
      <div class="row">
        <div class="field"><label for="sr-org">Organization</label><input id="sr-org" name="organization" autocomplete="organization"></div>
        <div class="field"><label for="sr-date">Date or timeframe</label><input id="sr-date" name="date" placeholder="e.g. March 2027"></div>
      </div>
      <div class="row">
        <div class="field"><label for="sr-format">Format</label>
          <select id="sr-format" name="format"><option>Keynote or lecture</option><option>Class (one or more sessions)</option><option>Workshop</option><option>Panel or moderated discussion</option><option>Not sure yet</option></select></div>
        <div class="field"><label for="sr-mode">In person or online</label>
          <select id="sr-mode" name="mode"><option>In person</option><option>Online</option><option>Either</option></select></div>
      </div>
      <div class="field"><label for="sr-msg">About your audience and what you hope they take away</label><textarea id="sr-msg" name="message"></textarea></div>
      <p class="form-note" hidden></p>
      <button class="btn btn-primary" type="submit">Send request</button>
    </form>
  </div>
</section>
"""
    return page("speaking-and-media", "Speaking: Dr. Robert A. Hunt on AI and Being Human",
                "Invite Dr. Robert A. Hunt to speak on AI, faith and human identity. Signature talks, "
                "upcoming events, recent engagements and a speaking request form.",
                body, [PERSON, faq_ld(SPEAK_FAQ)] + events_ld)

OPEDS = [
    ("2025-04", "April 2025", "AI-Generated Art Bites the Hand That Feeds It", "Fort Worth Star-Telegram", "https://tinyurl.com/5n8hnyzf"),
    ("2025-03", "March 2025", "With Agentic AI, We Need Guardrails", "Austin American-Statesman", "https://www.statesman.com/story/opinion/columns/your-voice/2025/03/23/what-is-agentic-ai-artificial-intelligence-congress-needs-guardrails/82529966007/"),
    ("2025-03", "March 2025", "AI Is All Brain and No Ethics", "Fox News", "https://www.foxnews.com/opinion/ai-is-all-brain-and-no-ethics"),
    ("2025-02", "February 2025", "AI Agents Reshape Humanity", "The Hill", "https://thehill.com/opinion/technology/5143728-ai-agents-reshape-humanity"),
    ("2024-06", "June 2024", "Will We Lose Our Humanity to AI?", "The Dallas Morning News", "https://www.dallasnews.com/opinion/commentary/2024/06/02/shall-we-lose-our-humanity-for-ai/"),
    ("2024-06", "June 2024", "Real Artist or AI Creative?", "DC Journal", "https://dcjournal.com/skilled-artists-create-art-creatives-no/"),
    ("2023-07", "July 2023", "Pandemic Prompts Course in Digitally Mediated Ministry", "InsideSources", "https://insidesources.com/pandemic-prompts-class-on-digitally-mediated-ministry/"),
    ("2023-02", "February 2023", "ChatGPT Won't Make Us Slaves. Uninspired Education Might.", "The Dallas Morning News", "https://www.dallasnews.com/opinion/commentary/2023/02/04/chatgpt-isnt-going-to-make-us-slaves-uninspired-education-might/"),
    ("2022-10", "October 2022", "Are We Humans or Machines?", "The Dallas Morning News", "https://www.dallasnews.com/opinion/commentary/2022/10/16/the-more-we-think-of-ai-as-human-the-more-we-think-of-ourselves-as-machines/"),
]

def blog():
    ops = "".join(f'<li><time datetime="{iso}">{esc(d)}</time><div><h3><a href="{u}">{esc(t)}</a></h3><p>{esc(o)}</p></div></li>' for iso, d, t, o, u in OPEDS)
    body = f"""
<div class="wrap">
  <header class="page-head">
    <p class="eyebrow">Writing</p>
    <h1>Weekly essays on AI and being human</h1>
    <p class="lede">Dr. Hunt publishes a new essay every week on Substack, on AI, ethics, faith and human identity. Subscribe free to get each one by email.</p>
    <div class="hero-actions"><a class="btn btn-primary" href="{SUBSTACK}subscribe">Subscribe on Substack</a><a class="btn btn-ghost" href="{SUBSTACK}archive">Browse all essays</a></div>
  </header>
</div>

<section class="section" id="op-eds">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Op-eds</p><h2>In the press</h2></div>
    <ul class="dated">{ops}</ul>
  </div>
</section>
"""
    return page("blog", "Writing by Dr. Robert A. Hunt: Essays and Op-eds on AI",
                "Weekly essays by Dr. Robert A. Hunt on AI, faith and being human, plus his op-eds in "
                "Fox News, The Hill, The Dallas Morning News and other outlets.",
                body, [PERSON])

SERIES = [
    ("Real Humanity in an AI Age",
     "An Interfaith Encounters series for anyone wondering what it means to be human in a world increasingly shaped by algorithms, automation and digital life. It asks whether humans are biological machines, tests the brain-computer analogy, and explores what authentic living looks like now.",
     ["Real Humanity and AI: Introduction", "AI and the Experiment Changing Humanity", "Are Humans Biological Machines?",
      "What Is Human Intelligence?", "The Brain as a Computer?", "The Human Place in the World",
      "Being Human, Spare Parts and Immortality", "AI: Consciousness, Self-Consciousness and Algorithms",
      "Being an Authentic Human"]),
    ("Gen Z, Religion and AI",
     "How AI is reshaping religious thought across communities, with a media psychologist, students and religious leaders discussing faith, ethics and human uniqueness.",
     ["Angela Patterson: Gen Z in an AI World", "Four University Students on AI and Faith",
      "Three High School Students on AI and Faith", "Four Jewish Students Reflect on AI and Faith",
      "Two Muslim Students Reflect on Islam and AI", "AI, Christian Ministry and Theological Education"]),
]
GUESTING = [
    ("Preserving Humanity in an AI Age", "Transform Now (Blue Prism)", None),
    ("Artificial Intelligence", "The Weight", "https://podcasts.apple.com/us/podcast/artificial-intelligence-with-robert-hunt/id1500772724?i=1000665418742"),
    ("Are Religious People Happier?", "For Real Life", "https://podcasts.apple.com/us/podcast/15-dr-robert-hunt-are-religious-people-happier-than/id1703346439?i=1000669448588"),
]

def podcasts():
    series = ""
    for t, d, eps in SERIES:
        li = "".join(f"<li>{esc(e)}</li>" for e in eps)
        series += f"""<article class="card" style="gap:0.9rem"><p class="meta">{len(eps)} episodes &middot; Interfaith Encounters</p><h3>{esc(t)}</h3><p>{esc(d)}</p><ol class="episodes">{li}</ol><p><a href="{APPLE}">Listen on Apple Podcasts</a></p></article>"""
    guest = "".join(
        f'<li><span class="when">Guest</span><div><h3>{f"<a href=\"{u}\">{esc(t)}</a>" if u else esc(t)}</h3><p>{esc(s)}</p></div></li>'
        for t, s, u in GUESTING)
    graph = [PERSON] + [{"@type": "PodcastSeries", "name": t, "description": d, "url": APPLE,
                         "author": PERSON_REF, "isPartOf": {"@type": "PodcastSeries", "name": "Interfaith Encounters", "url": APPLE}}
                        for t, d, _ in SERIES]
    body = f"""
<div class="wrap">
  <header class="page-head split" style="align-items:center">
    {img("podcast-studio.jpg", "photo square", eager=True)}
    <div>
    <p class="eyebrow">Podcasts</p>
    <h1>Real Humanity AI podcasts</h1>
    <p class="lede">Two series from Dr. Hunt's Interfaith Encounters podcast, plus his recent guest appearances on other shows.</p>
    <div class="hero-actions"><a class="btn btn-primary" href="{APPLE}">Apple Podcasts</a><a class="btn btn-ghost" href="{LINKS['YouTube']}">YouTube</a></div>
    </div>
  </header>
</div>
<section class="section">
  <div class="wrap"><div class="grid">{series}</div></div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Appearances</p><h2>As a guest</h2></div>
    <ul class="dated">{guest}</ul>
  </div>
</section>
"""
    return page("real-humanity-ai-podcasts", "Real Humanity AI Podcasts | Robert A. Hunt",
                "Real Humanity in an AI Age and Gen Z, Religion and AI: podcast series by Dr. Robert A. Hunt "
                "on what it means to be human in an AI age.", body, graph)

def contact():
    body = f"""
<div class="wrap">
  <header class="page-head">
    <p class="eyebrow">Contact</p>
    <h1>Get in touch</h1>
    <p class="lede">For speaking invitations, please use the <a href="{href('speaking-and-media')}#invite">speaking request form</a>. For anything else, including media requests, review copies for classes and your own experience of being human with AI, write here.</p>
  </header>
  <div class="split" style="padding-bottom:3rem">
    <form class="form" method="post" action="" data-endpoint="">
      <div class="field"><label for="c-name">Name</label><input id="c-name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="c-topic">Topic</label>
        <select id="c-topic" name="topic"><option>General message</option><option>Media or interview request</option><option>Book or class use</option><option>Speaking</option></select></div>
      <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" required></textarea></div>
      <p class="form-note" hidden></p>
      <button class="btn btn-primary" type="submit">Send message</button>
    </form>
    <div class="prose">
      <h2 style="font-size:1.3rem">Follow along</h2>
      <p>New essays arrive weekly on <a href="{SUBSTACK}">Substack</a>. For news on talks and articles, follow Dr. Hunt on <a href="{LINKS['LinkedIn']}">LinkedIn</a>.</p>
    </div>
  </div>
</div>
"""
    return page("contact", "Contact Dr. Robert A. Hunt",
                "Contact Dr. Robert A. Hunt about speaking, media interviews, or using All Brain and No Soul? with a class.",
                body, [PERSON])

def not_found():
    body = f"""
<div class="wrap"><header class="page-head">
  <p class="eyebrow">Page not found</p>
  <h1>That page has moved</h1>
  <p class="lede">If you were looking for one of Dr. Hunt's blog posts, his essays now live on <a href="{SUBSTACK}archive">Substack</a>. Otherwise, try the <a href="{href('')}">home page</a>.</p>
</header></div>"""
    return page("404", "Page not found | Robert A. Hunt", "This page has moved.", body)

# ---------------------------------------------------------------- machine-readable files
def llms_txt():
    lines = [
        f"# {NAME}",
        "",
        f"> Dr. Robert A. Hunt is {TITLE_FULL}, and author of {BOOK} {BOOK_SUB} (Wipf and Stock, 2025). "
        "He speaks and writes on artificial intelligence, faith and what it means to be human, for churches, "
        "universities, and business and civic leaders. Based in Dallas, Texas.",
        "",
        "Not to be confused with other people named Robert Hunt (for example the NFL guard or the illustrator).",
        "",
        "## Pages",
        f"- [About]({SITE}/about): biography, education and books",
        f"- [The book]({SITE}/the-book): {BOOK} {BOOK_SUB}; formats, contents, FAQ and where to buy",
        f"- [Speaking]({SITE}/speaking-and-media): signature talks, upcoming and recent events, how to book",
        f"- [Writing]({SITE}/blog): weekly Substack essays and published op-eds",
        f"- [Podcasts]({SITE}/real-humanity-ai-podcasts): Real Humanity in an AI Age; Gen Z, Religion and AI",
        f"- [Contact]({SITE}/contact)",
        "",
        "## Elsewhere",
    ] + [f"- [{n}]({u})" for n, u in LINKS.items()]
    return "\n".join(lines) + "\n"

def robots_txt():
    return f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n"

def sitemap():
    urls = "".join(f"  <url><loc>{SITE}{'/' if s == '' else '/' + s}</loc><lastmod>{TODAY}</lastmod></url>\n" for s, _ in PAGES)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'

# ---------------------------------------------------------------- write
def main():
    out = os.path.join(HERE, OUT)
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    builders = {"": home, "about": about, "the-book": the_book, "speaking-and-media": speaking,
                "blog": blog, "real-humanity-ai-podcasts": podcasts, "contact": contact, "404": not_found}
    for slug, fn in builders.items():
        name = "index.html" if slug == "" else f"{slug}.html"
        with open(os.path.join(out, name), "w") as f:
            f.write(fn())
    shutil.copy(os.path.join(HERE, "src", "style.css"), out)
    if os.path.isdir(os.path.join(HERE, "images")) and os.listdir(os.path.join(HERE, "images")):
        shutil.copytree(os.path.join(HERE, "images"), os.path.join(out, "images"))
    if not PREVIEW:
        for name, text in {"llms.txt": llms_txt(), "robots.txt": robots_txt(),
                           "sitemap.xml": sitemap()}.items():
            with open(os.path.join(out, name), "w") as f:
                f.write(text)
        if USE_CUSTOM_DOMAIN:
            with open(os.path.join(out, "CNAME"), "w") as f:
                f.write("robertahunt.com\n")
    print("built", out, sorted(os.listdir(out)))

if __name__ == "__main__":
    main()
