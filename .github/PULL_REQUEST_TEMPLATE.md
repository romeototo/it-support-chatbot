## Pull Request Summary

<!-- Provide a clear, one-sentence summary of what this PR does. -->

Fixes # <!-- Issue number if applicable -->

---

## Type of Change

<!-- Check all that apply. -->

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (existing functionality changes in a way that may break other things)
- [ ] FAQ / knowledge base update (adding or editing entries in `knowledge_base.json` or `kb.js`)
- [ ] Documentation update
- [ ] Refactor (no behavior change, code structure improvement)
- [ ] CI / tooling update

---

## What Changed

<!-- Briefly describe the technical changes made. List files modified and why. -->

-
-

---

## Testing Done

<!-- Describe how you tested these changes. -->

- [ ] Tested in static mode (opened `index.html` directly in browser)
- [ ] Tested in Flask mode (`python web_app.py` → `http://localhost:5000`)
- [ ] Tested with Gemini AI enabled
- [ ] Tested with Gemini AI disabled (RAG + keyword only)
- [ ] Ran `python init_rag.py` after FAQ changes
- [ ] Verified admin dashboard real-time sync still works (open both tabs)

---

## Checklist

- [ ] My changes follow the style guidelines in [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] I have added comments for any non-obvious logic
- [ ] I have updated the documentation if needed (README, inline comments, etc.)
- [ ] If I changed FAQ data, I ran `python init_rag.py` to rebuild the vector DB
- [ ] I have not introduced any `console.log` or debug prints in production code
- [ ] This PR is focused on a single change (not bundling unrelated fixes)

---

## Screenshots (if applicable)

<!-- For UI changes, include before/after screenshots. -->
