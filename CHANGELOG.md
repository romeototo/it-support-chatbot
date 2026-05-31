# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). This project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

Changes that are merged to `main` but not yet tagged as a release.

---

## [0.3.0] — 2026-05

### Added
- `add_faq.py` batch FAQ management tool that syncs both `kb.js` and `knowledge_base.json` simultaneously
- `line_webhook_template.py` starter template for integrating with the LINE Messaging API
- `GUIDE.md` — contributor and user guide for setting up and extending the knowledge base
- GitHub Actions workflow: `validate-kb.yml` for CI validation of knowledge base structure
- GitHub Actions workflow: `python-lint.yml` for automated Python code linting
- QR code (`chatbot_qr.png`) for quick access to the live demo

### Changed
- `add_faq.py` now automatically syncs both static and backend knowledge base files in a single run
- SEO meta tags added to `index.html` and `dashboard.html`
- Default language attribute set to `lang="th"` on HTML pages

### Fixed
- Duplicate ticket creation caused by double Enter key event handler
- False positive `isClosing` detection (e.g., "booking" incorrectly matched "ok")
- Terminal chatbot displaying raw Python tuple instead of formatted output
- Dashboard progress bar now uses ticket status for width calculation instead of a random value

### Security
- XSS protection added to admin dashboard via `escapeHtml()` sanitization on all user-supplied content

---

## [0.2.0] — 2026-04

### Added
- **Admin Dashboard** (`dashboard.html`) — HelpDesk Pro portal for IT staff with ticket queue management
- **Real-time cross-tab sync** using `localStorage` + `storage` event API (no backend required)
- Live "Admin is typing…" indicator synchronized to the user chatbot
- Resolution rate analytics chart powered by Chart.js
- Ticket search and filter (by ID, keyword, and status)
- Canned response library for admins (one-click quick replies)
- Dark/light mode toggle with persistent preference

### Changed
- Chatbot UI redesigned with glassmorphism visual style
- Knowledge base expanded to 202 FAQs across 45 IT categories

### Fixed
- Gemini API error messages now return specific status codes (400, 403, 429) instead of a generic error
- Escape key shortcut to close the AI configuration panel

---

## [0.1.0] — 2026-03

### Added
- Initial release of the IT Support Chatbot
- User-facing chatbot interface (`index.html`) with static FAQ matching
- Flask backend (`web_app.py`) with REST API routes for ticket creation and search
- Three-layer hybrid search engine: Keyword Matching → ChromaDB RAG → Gemini AI LLM
- ChromaDB vector search integration (`rag_engine.py`, `init_rag.py`)
- Pre-loaded knowledge base with common IT support FAQs (`knowledge_base.json`, `kb.js`)
- Gemini AI optional integration (activated via API key in the UI)
- Ticket creation and basic ticket history persistence
- MIT License
- `requirements.txt` with pinned minimum versions

---

[Unreleased]: https://github.com/romeototo/it-support-chatbot/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/romeototo/it-support-chatbot/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/romeototo/it-support-chatbot/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/romeototo/it-support-chatbot/releases/tag/v0.1.0
