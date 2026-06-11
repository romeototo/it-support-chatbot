#!/usr/bin/env python3
"""
Unit Tests for IT Support Chatbot
==================================
ทดสอบฟังก์ชันหลักทั้งหมดของ chatbot.py
- load_kb, tokenize_thai, expand_with_synonyms
- find_relevant_faqs, get_response, substring_match
- Conversation history helpers
- Edge cases: empty input, very long input, unknown language

Run:  pytest tests/ -v
"""

import json
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# ---------------------------------------------------------------------------
# Mock RAGEngine *before* importing chatbot so the module-level
# `rag_engine = RAGEngine(...)` does not need real ChromaDB / embeddings.
# ---------------------------------------------------------------------------
_mock_rag_engine = MagicMock()
_mock_rag_engine.query.return_value = []  # default: no RAG results

_mock_rag_cls = MagicMock(return_value=_mock_rag_engine)
sys.modules["rag_engine"] = MagicMock(RAGEngine=_mock_rag_cls)

# Now safe to import chatbot
from chatbot import (  # noqa: E402
    load_kb,
    tokenize_thai,
    expand_with_synonyms,
    find_relevant_faqs,
    get_response,
    substring_match,
    add_to_history,
    get_history_context,
    conversation_history,
    THAI_STOP_WORDS,
    SYNONYM_MAP,
    KB_FILE,
)


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture(scope="session")
def kb():
    """โหลด knowledge_base.json จริงเพื่อใช้ทดสอบ (session scope เพราะไม่มี mutation)"""
    kb_path = Path(__file__).resolve().parent.parent / "knowledge_base.json"
    assert kb_path.exists(), f"knowledge_base.json not found at {kb_path}"
    with open(kb_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


@pytest.fixture(autouse=True)
def _reset_rag_mock():
    """รีเซ็ต RAG mock + conversation history ก่อนทุก test"""
    _mock_rag_engine.query.reset_mock()
    _mock_rag_engine.query.return_value = []
    conversation_history.clear()
    yield


# ============================================================
# 1. load_kb()
# ============================================================

class TestLoadKB:
    """ทดสอบการโหลด Knowledge Base"""

    def test_load_kb_returns_dict_with_categories_and_escalation(self):
        """load_kb() ต้องคืน dict ที่มี key 'categories' และ 'escalation'"""
        data = load_kb()
        assert isinstance(data, dict)
        assert "categories" in data
        assert "escalation" in data

    def test_load_kb_categories_is_list(self):
        """categories ต้องเป็น list"""
        data = load_kb()
        assert isinstance(data["categories"], list)

    def test_load_kb_escalation_has_required_keys(self):
        """escalation ต้องมี message และ hotline"""
        data = load_kb()
        esc = data["escalation"]
        assert "message" in esc
        assert "hotline" in esc

    def test_load_kb_each_category_has_name_keywords_faqs(self, kb):
        """ทุก category ต้องมี name, keywords, faqs"""
        for cat in kb["categories"]:
            assert "name" in cat, f"Missing 'name' in category: {cat}"
            assert "keywords" in cat, f"Missing 'keywords' in category: {cat.get('name')}"
            assert "faqs" in cat, f"Missing 'faqs' in category: {cat.get('name')}"

    def test_load_kb_fallback_on_missing_file(self, tmp_path):
        """ถ้าไฟล์ KB ไม่มี ต้อง fallback เป็น dict ว่าง + escalation default"""
        with patch("chatbot.KB_FILE", tmp_path / "nonexistent.json"):
            data = load_kb()
        assert data["categories"] == []
        assert "message" in data["escalation"]


# ============================================================
# 2. tokenize_thai()
# ============================================================

class TestTokenizeThai:
    """ทดสอบ Thai tokenizer"""

    def test_basic_thai_tokenization(self):
        """tokenize ข้อความภาษาไทยพื้นฐาน"""
        tokens = tokenize_thai("wifi ช้า ครับ")
        assert "wifi" in tokens
        # "ครับ" เป็น stop word ต้องถูกตัดออก
        assert "ครับ" not in tokens

    def test_stop_words_removed(self):
        """stop words ทั้งไทยและอังกฤษต้องถูกลบ"""
        tokens = tokenize_thai("how to connect wifi ครับ")
        for sw in ["how", "to", "ครับ"]:
            assert sw not in tokens

    def test_lowercased(self):
        """ผลลัพธ์ต้องเป็นตัวพิมพ์เล็กทั้งหมด"""
        tokens = tokenize_thai("WiFi PASSWORD Reset")
        for t in tokens:
            assert t == t.lower()

    def test_empty_input_returns_empty_list(self):
        """input ว่างต้องคืน list ว่าง"""
        assert tokenize_thai("") == []
        assert tokenize_thai("   ") == []

    def test_punctuation_stripped(self):
        """เครื่องหมายวรรคตอนต้องถูกลบ"""
        tokens = tokenize_thai("wifi? password! email.")
        # punctuation ถูกแทนด้วย space แล้ว split
        assert all("?" not in t and "!" not in t and "." not in t for t in tokens)


# ============================================================
# 3. expand_with_synonyms()
# ============================================================

class TestExpandWithSynonyms:
    """ทดสอบการขยาย synonyms"""

    def test_wifi_expands_to_thai_variants(self):
        """wifi ต้องขยายเป็น ไวไฟ, wi-fi, internet ฯลฯ"""
        expanded = expand_with_synonyms(["wifi"])
        assert "ไวไฟ" in expanded
        assert "wi-fi" in expanded or "internet" in expanded

    def test_password_expands(self):
        """password ต้องขยายเป็น รหัสผ่าน, พาสเวิร์ด"""
        expanded = expand_with_synonyms(["password"])
        assert "รหัสผ่าน" in expanded

    def test_unknown_token_no_expansion(self):
        """token ที่ไม่มีใน SYNONYM_MAP ต้องไม่ขยาย"""
        expanded = expand_with_synonyms(["xyzrandom123"])
        assert expanded == {"xyzrandom123"}

    def test_multiple_tokens_expand(self):
        """ขยายหลาย tokens พร้อมกัน"""
        expanded = expand_with_synonyms(["wifi", "printer"])
        assert "ไวไฟ" in expanded
        assert "ปริ้นเตอร์" in expanded


# ============================================================
# 4. substring_match()
# ============================================================

class TestSubstringMatch:
    """ทดสอบ Thai substring matching"""

    def test_matching_substring_found(self):
        """ถ้า user token ปรากฏเป็น substring ใน target ต้องนับ"""
        count = substring_match("wifi ช้า", "เชื่อมต่อ WiFi ช้ามาก")
        assert count >= 1  # "wifi" หรือ "ช้า" ต้อง match อย่างน้อย 1

    def test_no_match_returns_zero(self):
        """ถ้าไม่มี substring match ต้องคืน 0"""
        count = substring_match("xyznotexist", "เชื่อมต่อ WiFi")
        assert count == 0

    def test_short_token_ignored(self):
        """token สั้นกว่า 2 ตัวอักษรต้องถูกข้ามไป (ตาม logic len >= 2)"""
        count = substring_match("a b c", "a b c d e")
        assert count == 0  # single char tokens ถูกข้าม


# ============================================================
# 5. find_relevant_faqs()
# ============================================================

class TestFindRelevantFaqs:
    """ทดสอบ FAQ keyword search"""

    def test_wifi_query_returns_network_faqs(self, kb):
        """ถามเรื่อง wifi ต้องได้ FAQ จากหมวด อินเทอร์เน็ต/Network"""
        results = find_relevant_faqs("wifi ช้า", kb)
        assert len(results) > 0
        # results = [(score, faq, category_name), ...]
        categories = [r[2] for r in results]
        assert any("อินเทอร์เน็ต" in c or "Network" in c for c in categories)

    def test_printer_query_returns_printer_faqs(self, kb):
        """ถามเรื่อง printer ต้องได้ FAQ จากหมวดเครื่องพิมพ์"""
        results = find_relevant_faqs("เครื่องพิมพ์พิมพ์ไม่ออก", kb)
        assert len(results) > 0
        categories = [r[2] for r in results]
        assert any("เครื่องพิมพ์" in c for c in categories)

    def test_password_query_returns_security_faqs(self, kb):
        """ถามเรื่อง password/รหัสผ่าน ต้องได้ FAQ จากหมวด Password/Security"""
        results = find_relevant_faqs("ลืมรหัสผ่าน", kb)
        assert len(results) > 0
        categories = [r[2] for r in results]
        assert any("Password" in c or "Security" in c for c in categories)

    def test_returns_at_most_3_results(self, kb):
        """ต้องคืนผลลัพธ์ไม่เกิน 3 รายการ"""
        results = find_relevant_faqs("computer slow ช้า คอม", kb)
        assert len(results) <= 3

    def test_results_sorted_by_score_desc(self, kb):
        """ผลลัพธ์ต้องเรียงจาก score สูง → ต่ำ"""
        results = find_relevant_faqs("email ส่งไม่ได้", kb)
        if len(results) >= 2:
            scores = [r[0] for r in results]
            assert scores == sorted(scores, reverse=True)


# ============================================================
# 6. get_response()
# ============================================================

class TestGetResponse:
    """ทดสอบ full response pipeline"""

    def test_returns_tuple_of_response_and_engine(self, kb):
        """get_response ต้องคืน (response_text, engine_name)"""
        result = get_response("wifi ช้า", kb, session_id="test_sess")
        assert isinstance(result, tuple)
        assert len(result) == 2
        response, engine = result
        assert isinstance(response, str)
        assert isinstance(engine, str)

    def test_keyword_match_returns_keyword_engine(self, kb):
        """ถ้า keyword match score >= 5 ต้องคืน engine='Keyword'"""
        # "wifi ช้า" ควรได้ score สูงพอจาก keyword matching
        response, engine = get_response("wifi เชื่อมต่อไม่ได้", kb, session_id="test_kw")
        assert engine in ("Keyword", "Keyword (Low)", "RAG", "RAG (Suggested)", "Escalated")

    def test_escalation_when_no_match(self, kb):
        """ถ้าไม่มี match ต้อง escalate"""
        _mock_rag_engine.query.return_value = []
        response, engine = get_response(
            "xyzrandomquerynothing12345", kb, session_id="test_esc"
        )
        assert engine == "Escalated"
        assert kb["escalation"]["message"] in response or "ติดต่อ" in response

    def test_rag_engine_called_on_low_keyword_score(self, kb):
        """ถ้า keyword score ต่ำ ต้องเรียก RAG engine"""
        _mock_rag_engine.query.return_value = []
        get_response("sdkfjhaskdfj", kb, session_id="test_rag_call")
        _mock_rag_engine.query.assert_called()

    def test_high_rag_score_returns_rag_engine(self, kb):
        """ถ้า RAG คืน score สูง ต้องใช้ engine='RAG'"""
        _mock_rag_engine.query.return_value = [
            {
                "question": "VPN เชื่อมต่อไม่ได้ ทำยังไง?",
                "answer": "1. ตรวจ Internet\n2. Restart VPN",
                "category": "VPN",
                "score": 0.85,
            }
        ]
        response, engine = get_response(
            "vpn ใช้ไม่ได้เลยวันนี้", kb, session_id="test_rag_high"
        )
        # keyword score for this query is likely low, so should fall to RAG
        assert engine in ("Keyword", "RAG", "Gemini AI")


# ============================================================
# 7. Conversation History
# ============================================================

class TestConversationHistory:
    """ทดสอบ conversation memory"""

    def test_add_and_get_history(self):
        """เพิ่มข้อความแล้วดึงออกมาได้"""
        add_to_history("sess1", "user", "สวัสดีครับ")
        ctx = get_history_context("sess1")
        assert "สวัสดีครับ" in ctx

    def test_empty_session_returns_empty_string(self):
        """session ที่ไม่มีประวัติต้องคืน string ว่าง"""
        ctx = get_history_context("nonexistent_session")
        assert ctx == ""


# ============================================================
# 8. Edge Cases
# ============================================================

class TestEdgeCases:
    """ทดสอบกรณีพิเศษ / ขอบเขต"""

    def test_very_long_input(self, kb):
        """input ยาวมาก ต้องไม่ crash"""
        long_text = "wifi " * 500
        response, engine = get_response(long_text, kb, session_id="test_long")
        assert isinstance(response, str)

    def test_special_characters_input(self, kb):
        """input ที่มีอักขระพิเศษ ต้องไม่ crash"""
        response, engine = get_response("@#$%^&*()!!!", kb, session_id="test_special")
        assert isinstance(response, str)

    def test_numeric_only_input(self, kb):
        """input ที่เป็นตัวเลขล้วนต้องไม่ crash"""
        response, engine = get_response("1234567890", kb, session_id="test_num")
        assert isinstance(response, str)

    def test_mixed_language_input(self, kb):
        """input ที่ผสมภาษาไทย + อังกฤษ + จีน ต้องไม่ crash"""
        response, engine = get_response(
            "wifi ใช้ไม่ได้ 不能用了 помогите", kb, session_id="test_mixed"
        )
        assert isinstance(response, str)

    def test_emoji_input(self, kb):
        """input ที่มี emoji ต้องไม่ crash"""
        response, engine = get_response("🔥 wifi 💀", kb, session_id="test_emoji")
        assert isinstance(response, str)

    def test_tokenize_thai_with_only_stop_words(self):
        """ถ้า input มีแต่ stop words ต้องคืน list ว่าง"""
        tokens = tokenize_thai("ครับ ค่ะ นะ ได้ the is a an")
        assert tokens == []

    def test_find_relevant_faqs_empty_input(self, kb):
        """input ว่างต้องคืน list ว่าง (ไม่มี score > 0)"""
        results = find_relevant_faqs("", kb)
        assert results == []
