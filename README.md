# Static Site Generator (Python)

A minimal, custom-built **Markdown-to-HTML static site generator** created as part of the [Boot.dev](https://www.boot.dev) course "Build a Static Site Generator in Python".

This project parses Markdown files, converts them into structured HTML nodes, applies inline formatting (bold, italic, code, links, images), handles block-level elements (headings, paragraphs, quotes, lists, code blocks), copies static assets, and generates a deployable static site.

### Features

- Block-level parsing: paragraphs, headings (h1–h6), code blocks, quotes, ordered & unordered lists
- Inline Markdown support: `**bold**`, `_italic_`, `` `code` ``, `[links](url)`, `![images](url)`
- Inline parsing inside paragraphs, headings, quotes, and list items
- Code blocks preserve raw formatting and newlines (no inline parsing inside `<pre><code>`)
- Dynamic heading levels (`h1` to `h6` based on number of `#`)
- Recursive static asset copying from `static/` to `docs/`
- Simple title extraction from `# Heading 1`
- Full-page generation using a template (`template.html`)
- Deploy-ready output in `docs/` (GitHub Pages compatible)

### Live Sample Site

A generated example site is live here:  
https://aggrosec.github.io/static-site-generator-python/

(It's a fun Tolkien fan page built entirely by the generator.)

### Current Limitations & Assumptions

This generator is intentionally minimal and follows course restrictions:

- **Content directory (`content/`)**: Only `.md` (Markdown) files are processed. No other file types (images, CSS, JS, PDFs, etc.) are handled from `content/` or its subdirectories. All non-Markdown files in `content/` will not work in the conversion. Use static to copy over images and the like.
- **Static assets**: Only files in the `static/` directory are copied to `docs/` (images, CSS, JS, etc.). No filtering by extension — everything in `static/` is copied as-is.
- **Inline Markdown parsing** (`**bold**`, `_italic_`, `` `code` ``, `[links](url)`, `![images](url)`):
  - Fully supported inside **paragraphs**, **headings**, **quotes**, and **list items**.
  - **Not** supported inside **code blocks** (content is preserved raw, including markup).
- **Nested inline markup** is **not supported** (e.g. `**bold _italic_ inside**` will not properly nest; the first delimiter type wins).
- **Block types**:
  - Headings: 1–6 levels (`#` to `######`), with proper `<h1>`–`<h6>` tags.
  - Code blocks: `<pre><code>...</code></pre>`, raw content preserved (newlines/whitespace intact), no language class or syntax highlighting.
  - Quotes: `<blockquote>`, content stripped of `>` markers, newlines preserved.
  - Lists: `<ul>`/`<ol>` with `<li>` containing parsed inline content.
  - Paragraphs: `<p>`, newlines replaced with spaces, full inline parsing.
- **No support for**:
  - Nested blocks (e.g. lists inside quotes, code inside lists).
  - Advanced Markdown (tables, task lists, footnotes, definition lists, HTML blocks, etc.).
  - Front matter/YAML metadata in Markdown files.
  - Custom shortcodes or plugins.
- **Output**: Generated site lives in `docs/`, which is **deleted and recreated** on each build (stale files removed).
- **No live reload** or watcher — run `main.sh` to rebuild and serve.
- **Server**: Simple Python `http.server` on port 8888 (changeable).

Future expansions could include nested inline, syntax highlighting, multi-page blog support, etc.

### Project Structure

```text
static-site-generator-python/
├── content/                    # All .md files go here
│   └── index.md
├── static/                     # CSS, images, etc.
│   ├── index.css
│   └── images/
│       └── tolkien.png
├── template.html               # HTML template with {{ Title }} and {{ Content }}
├── src/
│   ├── main.py                 # Entry point
│   ├── markdown_blocks.py
│   ├── textnode.py
│   ├── htmlnode.py
│   ├── markdown_html_conversion.py
│   └── ... (other helpers)
├── .gitignore
├── main.sh                     # Build + serve script
└── README.md
```

### How to Run Locally

1. **Build the site**

   ```bash
   ./main.sh
   ```
   This runs:

	python3 src/main.py (copies static files + generates HTML pages)
	tarts a local server: cd docs && python3 -m http.server 8888


2. **View locally**

	Open http://localhost:8888 in your browser.

### Deploy to GitHub Pages

1. Push your code to GitHub
2. Go to repo Settings → Pages
3. Set source to Deploy from a branch → main → /docs
4. Wait a few minutes → site appears at https://<username>.github.io/<repo-name>/

### Built With

- Python 3
- No external libraries beyond standard library (os, shutil, re, etc.)
- Guided by Boot.dev - Build a Static Site Generator in Python

### License

MIT License — feel free to use, modify, or learn from this project.

Made with ❤️ and a lot of debugging by Brandon (AggroSec)
