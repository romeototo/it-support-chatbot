#!/usr/bin/env python3
"""
IT Support Chatbot - Enhanced Edition
Hybrid search: Keyword (Thai-optimized) → RAG → LLM
With conversation memory and improved scoring
"""

import json
import re
import sys
from pathlib import Path
from rag_engine import RAGEngine
import os
import urllib.request
import urllib.error
from collections import defaultdict
import logging
logger = logging.getLogger(__name__)

# ============================================================
# CONFIG
# ============================================================
KB_FILE = Path(__file__).parent / "knowledge_base.json"

USE_LLM = os.environ.get("USE_LLM", "false").lower() == "true"

# LLM Config (Xiaomi Token Plan)
LLM_API_URL = "https://token-plan-sgp.xiaomimimo.com/v1/chat/completions"
LLM_MODEL = "mimo-v2.5"
LLM_API_KEY = os.getenv("LLM_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""

# Initialize RAG Engine
rag_engine = RAGEngine(api_key=LLM_API_KEY)

# ============================================================
# CONVERSATION MEMORY (per session)
# ============================================================
conversation_history = defaultdict(list)  # session_id -> [(role, content)]
MAX_HISTORY = 5

def add_to_history(session_id, role, content):
    """Add message to conversation history."""
    history = conversation_history[session_id]
    history.append((role, content))
    if len(history) > MAX_HISTORY * 2:
        conversation_history[session_id] = history[-MAX_HISTORY * 2:]

def get_history_context(session_id):
    """Get recent conversation context as string."""
    history = conversation_history.get(session_id, [])
    if not history:
        return ""
    lines = [f"{role}: {msg}" for role, msg in history[-MAX_HISTORY:]]
    return "\n".join(lines)

# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================
def load_kb():
    """Load knowledge base from JSON file."""
    try:
        with open(KB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Knowledge base file not found: {KB_FILE}")
        return {"categories": [], "escalation": {"message": "กรุณาติดต่อ IT Support", "hotline": "ext.1234"}}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in knowledge base: {e}")
        return {"categories": [], "escalation": {"message": "กรุณาติดต่อ IT Support", "hotline": "ext.1234"}}

# ============================================================
# THAI-OPTIMIZED KEYWORD MATCHING
# ============================================================

# Common Thai stop words to ignore
THAI_STOP_WORDS = set([
    "ครับ", "ค่ะ", "คะ", "นะ", "มั้ย", "ไหม", "ได้", "จะ", "ให้",
    "ที่", "ของ", "ใน", "เป็น", "มี", "ไป", "มา", "ทำ", "แล้ว",
    "และ", "หรือ", "แต่", "ไม่", "ก็", "ถ้า", "จาก", "กับ",
    "the", "is", "a", "an", "to", "and", "or", "of", "in", "for",
    "how", "what", "why", "can", "do", "i", "my", "your", "it",
])

# Thai synonyms / related terms for better matching
SYNONYM_MAP = {
    "wifi": ["ไวไฟ", "wi-fi", "วายฟาย", "อินเทอร์เน็ต", "internet", "เน็ต"],
    "ไวไฟ": ["wifi", "wi-fi", "internet"],
    "printer": ["ปริ้นเตอร์", "ปริ้นท์", "พิมพ์", "print"],
    "ปริ้นเตอร์": ["printer", "print"],
    "password": ["รหัสผ่าน", "พาสเวิร์ด", "pass", "pwd"],
    "รหัสผ่าน": ["password", "pass", "pwd"],
    "email": ["อีเมล", "เมล", "mail", "gmail", "outlook"],
    "อีเมล": ["email", "mail"],
    "vpn": ["วีพีเอ็น"],
    "computer": ["คอม", "คอมพิวเตอร์", "เครื่อง", "pc"],
    "คอม": ["computer", "pc"],
    "login": ["เข้าสู่ระบบ", "ล็อกอิน", "signin", "sign-in"],
    "เข้าสู่ระบบ": ["login", "signin"],
    "error": ["ข้อผิดพลาด", "เออเร่อ", "พัง", "เสีย", "ใช้ไม่ได้"],
    "update": ["อัพเดต", "อัพเดท", "update"],
    "install": ["ติดตั้ง", "ลงโปรแกรม"],
    "ติดตั้ง": ["install"],
    "slow": ["ช้า", "อืด", "lag", "หน่วง"],
    "ช้า": ["slow", "lag"],
    "screen": ["หน้าจอ", "จอ", "monitor"],
    "keyboard": ["คีย์บอร์ด", "แป้นพิมพ์"],
    "mouse": ["เมาส์", "เม้าส์"],
    "file": ["ไฟล์", "เอกสาร"],
    "folder": ["โฟลเดอร์", "แฟ้ม"],
    "backup": ["สำรองข้อมูล", "แบ็คอัพ"],
    "virus": ["ไวรัส", "มัลแวร์", "malware", "antivirus"],
}

def tokenize_thai(text):
    """Simple Thai tokenizer - split on spaces + extract Thai word chunks."""
    text = text.lower().strip()
    # Remove punctuation
    text = re.sub(r'[^\w\sก-๙]', ' ', text)
    tokens = []
    for word in text.split():
        if word and word not in THAI_STOP_WORDS:
            tokens.append(word)
    return tokens

def expand_with_synonyms(tokens):
    """Expand token set with synonyms for better matching."""
    expanded = set(tokens)
    for token in tokens:
        if token in SYNONYM_MAP:
            expanded.update(SYNONYM_MAP[token])
    return expanded

def substring_match(user_input, target_text):
    """Check if any user token appears as substring in target (good for Thai)."""
    user_tokens = tokenize_thai(user_input)
    target_lower = target_text.lower()
    matches = 0
    for token in user_tokens:
        if len(token) >= 2 and token in target_lower:
            matches += 1
    return matches

def find_relevant_faqs(user_input, kb):
    """Find FAQs matching user input using Thai-optimized keyword scoring."""
    user_tokens = tokenize_thai(user_input)
    user_expanded = expand_with_synonyms(user_tokens)
    user_set = set(user_tokens)
    scores = []

    for category in kb["categories"]:
        cat_keywords = set(kw.lower() for kw in category["keywords"])

        for faq in category["faqs"]:
            score = 0

            # 1. Category keyword match (highest weight)
            for kw in cat_keywords:
                if kw in user_expanded:
                    score += 5
                # Substring match for Thai partial words
                for token in user_tokens:
                    if len(token) >= 2 and (kw in token or token in kw):
                        score += 3

            # 2. Exact word overlap with question
            q_tokens = set(tokenize_thai(faq["question"]))
            overlap = user_set & q_tokens
            score += len(overlap) * 3

            # 3. Expanded synonym overlap with question
            q_expanded = expand_with_synonyms(q_tokens)
            synonym_overlap = user_expanded & q_expanded
            score += len(synonym_overlap) * 1

            # 4. Substring match (critical for Thai without word segmentation)
            sub_matches = substring_match(user_input, faq["question"])
            score += sub_matches * 2

            # 5. Substring match in answer too (lower weight)
            sub_answer = substring_match(user_input, faq["answer"])
            score += sub_answer * 1

            if score > 0:
                scores.append((score, faq, category["name"]))

    scores.sort(reverse=True, key=lambda x: x[0])
    return scores[:3]

# ============================================================
# LLM ENHANCED RESPONSE (Optional)
# ============================================================
def llm_answer(user_input, context_faqs, session_id="default"):
    """Use LLM to generate better answer from FAQ context + conversation history."""
    if not USE_LLM or not LLM_API_KEY:
        return None



    context = "\n\n".join([
        f"Q: {faq['question']}\nA: {faq['answer']}"
        for _, faq, _ in context_faqs
    ])

    history = get_history_context(session_id)

    prompt = f"""คุณเป็น IT Support Chatbot ตอบคำถามสั้น ชัดเจน เป็นภาษาไทย
ใช้ข้อมูลจาก FAQ ด้านล่างเป็นหลัก ถ้าไม่มีข้อมูล ให้แนะนำติดต่อ IT Support

{f"ประวัติสนทนาล่าสุด:{chr(10)}{history}{chr(10)}" if history else ""}
FAQ Context:
{context}

คำถามผู้ใช้: {user_input}

ตอบ:"""

    try:
        data = json.dumps({
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
            "temperature": 0.3
        }).encode("utf-8")

        req = urllib.request.Request(
            LLM_API_URL,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {LLM_API_KEY}"
            }
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"LLM Error: {e}")
        return None

# ============================================================
# CHATBOT RESPONSE (Enhanced)
# ============================================================
def get_response(user_input, kb, session_id="default"):
    """Get chatbot response with improved search pipeline."""

    # Track conversation
    add_to_history(session_id, "user", user_input)

    # 1. Keyword Matching (threshold lowered for better recall)
    exact_matches = find_relevant_faqs(user_input, kb)
    if exact_matches and exact_matches[0][0] >= 5:
        best = exact_matches[0][1]
        response = f"**{best['question']}**\n\n{best['answer']}"
        add_to_history(session_id, "bot", response)
        return response, "Keyword"

    # 2. RAG Vector Search
    try:
        matches = rag_engine.query(user_input, n_results=3)
    except Exception as e:
        logger.error(f"RAG Error: {e}")
        matches = []

    if not matches:
        # If keyword had low matches, use those instead of escalating
        if exact_matches and exact_matches[0][0] >= 2:
            best = exact_matches[0][1]
            response = f"ไม่แน่ใจว่าตรง 100% แต่คุณอาจหมายถึง:\n\n**{best['question']}**\n{best['answer']}\n\nหากยังไม่ใช่ กรุณาติดต่อ {kb['escalation']['hotline']}"
            add_to_history(session_id, "bot", response)
            return response, "Keyword (Low)"

        response = kb["escalation"]["message"]
        add_to_history(session_id, "bot", response)
        return response, "Escalated"

    best_match = matches[0]
    best_score = best_match.get('score', 0)

    # Combine keyword + RAG scores for better accuracy
    keyword_bonus = 0
    if exact_matches:
        keyword_bonus = exact_matches[0][0] * 0.5

    combined_score = best_score + (keyword_bonus / 10)

    # High confidence → return directly
    if combined_score >= 0.6:
        # Try LLM for better phrasing
        context_faqs = [(m.get('score', 0), m, m.get('category', '')) for m in matches]
        llm_response = llm_answer(user_input, context_faqs, session_id)

        if llm_response:
            add_to_history(session_id, "bot", llm_response)
            return llm_response, "Gemini AI"

        response = f"**{best_match['question']}**\n\n{best_match['answer']}"
        add_to_history(session_id, "bot", response)
        return response, "RAG"

    # Medium confidence → suggest with disclaimer
    if combined_score >= 0.3:
        response = f"คุณอาจหมายถึง:\n\n**{best_match['question']}**\n{best_match['answer']}\n\nหากยังไม่ใช่ กรุณาติดต่อ {kb['escalation']['hotline']}"
        add_to_history(session_id, "bot", response)
        return response, "RAG (Suggested)"

    # Low confidence → escalate
    response = kb["escalation"]["message"]
    add_to_history(session_id, "bot", response)
    return response, "Escalated"

# ============================================================
# MAIN LOOP
# ============================================================
def main():
    kb = load_kb()

    print("=" * 50)
    print("  IT Support Chatbot - Enhanced Edition")
    print("=" * 50)
    print("  Type your IT questions here")
    print("  Type 'quit' or 'exit' to leave")
    print("  Type 'help' to see all categories")
    print("=" * 50)
    print()

    session_id = "terminal_session"

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ["quit", "exit", "ออก", "q"]:
            print("Goodbye!")
            break

        if user_input.lower() in ["help", "ช่วย", "หมวดหมู่"]:
            print("\nCategories:")
            for cat in kb["categories"]:
                print(f"  - {cat['name']} ({len(cat['faqs'])} FAQ)")
            print(f"\nContact IT Support: {kb['escalation']['hotline']}")
            print()
            continue

        response, engine = get_response(user_input, kb, session_id)
        print(f"\nBot [{engine}]: {response}\n")

if __name__ == "__main__":
    main()
