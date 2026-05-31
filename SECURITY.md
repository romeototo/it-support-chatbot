# Security Policy

## Supported Versions

This project is in active development. Security fixes are applied to the latest release on the `main` branch only.

| Version | Supported |
| ------- | --------- |
| Latest (`main`) | ✅ Yes |
| Older releases | ❌ No |

---

## Reporting a Vulnerability

**Please do not open a public GitHub issue to report a security vulnerability.**

If you discover a security issue in this project, please report it privately using one of the following methods:

### Option 1 — GitHub Private Security Advisory (Preferred)

Use GitHub's built-in private vulnerability reporting:

1. Go to the [Security tab](https://github.com/romeototo/it-support-chatbot/security) of this repository
2. Click **"Report a vulnerability"**
3. Fill in the details

This creates a private advisory that only the maintainer can see.

### Option 2 — Direct Contact

If you prefer, you can contact the maintainer directly via GitHub:
[@romeototo](https://github.com/romeototo)

---

## What to Include in Your Report

To help reproduce and fix the issue quickly, please include:

- A description of the vulnerability
- The affected file(s) and line(s), if known
- Steps to reproduce the issue
- Potential impact (e.g., data exposure, code execution, XSS)
- Your suggested fix, if you have one

---

## Response Timeline

This project is maintained by a single person. I will aim to:

- Acknowledge receipt within **5 business days**
- Provide an initial assessment within **10 business days**
- Release a fix or mitigation within **30 days** for confirmed issues

I will keep you informed of progress throughout. If a fix takes longer due to complexity, I will communicate this openly.

---

## Scope

### In Scope

- **XSS vulnerabilities** in the admin dashboard or chatbot UI
- **API key exposure** through client-side code or logs
- **Insecure data handling** in Flask routes (`web_app.py`)
- **Dependency vulnerabilities** in `requirements.txt`
- **Unintended data persistence** in `localStorage` or `tickets.db`

### Out of Scope

- Issues in third-party services (Gemini API, ChromaDB, GitHub Pages infrastructure)
- Security of the user's own deployment environment
- Social engineering attacks
- Reports without a reproducible example

---

## Disclosure Policy

Once a fix is released, the maintainer will:

1. Publish a GitHub Security Advisory with full details
2. Credit the reporter in the advisory (unless they request anonymity)
3. Add a note to [CHANGELOG.md](CHANGELOG.md) under the relevant release

---

## Notes on Data Handling

This project is designed for **local and demo use**. By default:

- The static GitHub Pages version stores all ticket data in the **browser's `localStorage`** — no data is sent to any server
- The Flask backend stores tickets in a local **SQLite database** (`tickets.db`) — no cloud sync
- No analytics or telemetry is collected by this project

If you deploy this in a real environment, you are responsible for your own data security practices.
