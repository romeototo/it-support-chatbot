# Contributing to IT Support Chatbot

Thank you for your interest in contributing. This document explains how to get involved, report issues, and submit changes.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Adding or Updating FAQs](#adding-or-updating-faqs)
- [Reporting Bugs](#reporting-bugs)
- [Requesting Features](#requesting-features)
- [Style Guidelines](#style-guidelines)

---

## Code of Conduct

Please be respectful in all interactions. This project follows basic open-source norms: be constructive, be kind, and assume good intent.

---

## Ways to Contribute

You do not have to write code to contribute. Useful contributions include:

- Reporting bugs clearly with steps to reproduce
- Suggesting improvements to the FAQ knowledge base
- Improving documentation or fixing typos
- Writing or improving unit tests
- Translating FAQ content to other languages
- Sharing feedback on the chatbot response quality

---

## Development Setup

### Prerequisites

- Python 3.10 or higher
- `pip` (Python package manager)
- A modern browser (Chrome or Firefox recommended for testing the UI)

### Local Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/it-support-chatbot.git
cd it-support-chatbot

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Initialize the ChromaDB vector database
python init_rag.py

# 4. Start the Flask development server
python web_app.py

# 5. Open http://localhost:5000 in your browser
```

The static version (GitHub Pages mode) does not require Python — just open `index.html` directly in your browser.

---

## Project Structure

| File / Folder | Purpose |
| ------------- | ------- |
| `chatbot.py` | Hybrid search engine core (keyword → RAG → Gemini) |
| `rag_engine.py` | ChromaDB vector search logic |
| `init_rag.py` | Ingests `knowledge_base.json` into ChromaDB |
| `add_faq.py` | CLI tool to add FAQs — syncs both `kb.js` and `knowledge_base.json` |
| `web_app.py` | Flask server with REST API routes |
| `index.html` | User-facing chatbot UI |
| `dashboard.html` | Admin dashboard UI |
| `kb.js` | Static knowledge base (used by GitHub Pages mode) |
| `knowledge_base.json` | Structured FAQ data (used by Flask backend) |
| `config.json` | Runtime flags (RAG on/off, Gemini on/off) |
| `line_webhook_template.py` | Starter template for LINE Messaging API |

---

## Submitting a Pull Request

1. **Fork** the repository and create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes.** Keep each PR focused on a single change or fix.

3. **Test your changes:**
   - If you changed `chatbot.py` or `rag_engine.py`, run the Flask server and verify search results still work.
   - If you changed FAQ data, run `python init_rag.py` to rebuild the vector DB.
   - If you changed front-end files, test in both static mode (open `index.html`) and Flask mode.

4. **Commit clearly:**
   ```bash
   git commit -m "fix: prevent duplicate ticket on Enter key double press"
   ```
   Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format when possible (`fix:`, `feat:`, `docs:`, `chore:`).

5. **Push your branch** and open a Pull Request against `main`.

6. **Fill in the PR template** — describe what changed, why, and how it was tested.

The maintainer will review and provide feedback. Please be patient; this is maintained by a single person.

---

## Adding or Updating FAQs

The recommended way to add FAQ entries is through the `add_faq.py` script, which keeps both `kb.js` (static mode) and `knowledge_base.json` (Flask mode) in sync.

```bash
python add_faq.py
```

Follow the prompts to enter:
- Category name
- Question (trigger phrase)
- Answer
- Keywords (comma-separated)

After adding FAQs, rebuild the vector database:

```bash
python init_rag.py
```

If you are contributing a batch of new FAQs, you can also edit `knowledge_base.json` directly and submit a PR. Include a description of the topic area and why the FAQs are useful.

---

## Reporting Bugs

Use the [bug report template](https://github.com/romeototo/it-support-chatbot/issues/new?template=bug_report.md) and include:

- Browser and version
- Deployment mode (GitHub Pages or Flask)
- Steps to reproduce
- What you expected vs. what actually happened
- Screenshots if applicable

---

## Requesting Features

Use the [feature request template](https://github.com/romeototo/it-support-chatbot/issues/new?template=feature_request.md) and explain:

- The use case or problem you are trying to solve
- Your proposed solution (if you have one)
- Alternatives you have considered

---

## Style Guidelines

### Python

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use clear variable names — avoid single-letter variables except in list comprehensions
- Add a comment for any non-obvious logic, especially in the search pipeline

### JavaScript

- Use `const` and `let`, not `var`
- Keep functions small and focused
- Sanitize any user input before inserting it into the DOM (see `escapeHtml()` in `dashboard.html`)

### HTML / CSS

- Use semantic HTML5 elements
- Keep CSS class names descriptive
- Do not use inline styles for logic — keep styling in the `<style>` block

---

## Questions?

If you are unsure about anything, open a [discussion](https://github.com/romeototo/it-support-chatbot/discussions) or an issue and ask. There are no dumb questions when contributing to open source.
