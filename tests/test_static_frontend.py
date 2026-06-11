import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent.parent


def _index_html() -> str:
    return (ROOT / "index.html").read_text(encoding="utf-8")


def _render_related_link(markdown: str) -> str:
    html = markdown.replace("<", "&lt;")
    html = re.sub(
        r"\[([^\]]+)\]\(ask:([^)]+)\)",
        r'<a href="ask:\2" target="_blank">\1</a>',
        html,
    )
    html = re.sub(
        r"\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)",
        r'<a href="\2" target="_blank">\1</a>',
        html,
    )
    return html


def test_ask_link_rule_runs_before_generic_http_link_rule():
    html = _index_html()
    ask_rule_pos = html.index(r"\[([^\]]+)\]\(ask:([^)]+)\)")
    http_rule_pos = html.index(r"\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)")

    assert ask_rule_pos < http_rule_pos


def test_related_question_with_parentheses_does_not_leak_encoded_href():
    question = "เจอจอฟ้า (BSOD) ทำยังไง?"
    href = quote(question, safe="")
    rendered = _render_related_link(f"* [{question}](ask:{href})")

    assert f">{question}</a>" in rendered
    assert 'href="ask:' in rendered
    assert re.search(r"</a>.*%[0-9A-F]{2}", rendered) is None


class GeminiFormParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.form_depth = 0
        self.gemini_input_inside_form = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "form":
            self.form_depth += 1
        if (
            tag == "input"
            and attrs.get("id") == "geminiKey"
            and self.form_depth > 0
        ):
            self.gemini_input_inside_form = True

    def handle_endtag(self, tag):
        if tag == "form" and self.form_depth:
            self.form_depth -= 1


def test_gemini_password_input_is_inside_form():
    parser = GeminiFormParser()
    parser.feed(_index_html())

    assert parser.gemini_input_inside_form
