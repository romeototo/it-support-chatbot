#!/usr/bin/env python3
"""
IT Support Chatbot - Prototype
Simple FAQ-based chatbot with keyword matching + optional LLM
"""

import json
import re
import sys
from pathlib import Path
from rag_engine import RAGEngine
import os

# ============================================================
# CONFIG
# ============================================================
KB_FILE = Path(__file__).parent / "knowledge_base.json"

# Set to True to use LLM API for better responses (requires API key)
USE_LLM = False

# LLM Config (Xiaomi Token Plan)
LLM_API_URL = "https://token-plan-sgp.xiaomimimo.com/v1/chat/completions"
LLM_MODEL = "mimo-v2.5"
LLM_API_KEY = os.getenv("GOOGLE_API_KEY") or ""  # Will use environment variable if set

# Initialize RAG Engine
rag_engine = RAGEngine(api_key=LLM_API_KEY)

# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================
def load_kb():
    with open(KB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ============================================================
# KEYWORD MATCHING (No LLM needed)
# ============================================================
def find_relevant_faqs(user_input, kb):
    """Find FAQs matching user input using keyword scoring."""
    user_lower = user_input.lower()
    scores = []

    for category in kb["categories"]:
        for faq in category["faqs"]:
            score = 0

            # Check keyword matches in category
            for kw in category["keywords"]:
                if kw.lower() in user_lower:
                    score += 3

            # Check question text overlap
            q_words = set(faq["question"].lower().split())
            u_words = set(user_lower.split())
            overlap = q_words & u_words
            score += len(overlap) * 2

            # Check if any FAQ keyword is in user input
            faq_lower = faq["question"].lower()
            for word in user_lower.split():
                if word in faq_lower:
                    score += 1

            if score > 0:
                scores.append((score, faq, category["name"]))

    # Sort by score, return top matches
    scores.sort(reverse=True, key=lambda x: x[0])
    return scores[:3]

# ============================================================
# LLM ENHANCED RESPONSE (Optional)
# ============================================================
def llm_answer(user_input, context_faqs):
    """Use LLM to generate better answer from FAQ context."""
    if not USE_LLM or not LLM_API_KEY:
        return None

    import urllib.request
    import urllib.error

    context = "\n\n".join([
        f"Q: {faq['question']}\nA: {faq['answer']}"
        for _, faq, _ in context_faqs
    ])

    prompt = f"""คุณเป็น IT Support Chatbot ตอบคำถามสั้น ชัดเจน เป็นภาษาไทย
ใช้ข้อมูลจาก FAQ ด้านล่างเป็นหลัก ถ้าไม่มีข้อมูล ให้แนะนำติดต่อ IT Support

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
        print(f"[LLM Error: {e}]")
        return None

# ============================================================
# CHATBOT RESPONSE
# ============================================================
def get_response(user_input, kb):
    # 1. Try Exact Keyword Matching first (Highly accurate for Thai)
    exact_matches = find_relevant_faqs(user_input, kb)
    if exact_matches and exact_matches[0][0] >= 3:
        best = exact_matches[0][1]
        return f"**{best['question']}**\n\n{best['answer']}", "Keyword"

    # 2. Fallback to Vector DB (RAG)
    matches = rag_engine.query(user_input, n_results=3)

    if not matches:
        return kb["escalation"]["message"], "RAG Server"

    best_match = matches[0]
    
    # Check confidence (lower is better, depending on distance metric, but if old code used score < 0.3 as low confidence, I will use threshold)
    # distance metric usually has 0 as exact.
    if best_match.get('distance', 1.0) > 1.0:
        return f"ไม่แน่ใจว่าตรงกับที่คุณต้องการไหม แต่คุณอาจหมายถึง:\n\n**{best_match['question']}**\n{best_match['answer']}\n\nหากยังไม่ใช่ กรุณาติดต่อ {kb['escalation']['hotline']}", "RAG Server"

    # Try LLM for better response
    context_faqs = [(m.get('score', 0), m, m.get('category', '')) for m in matches]
    llm_response = llm_answer(user_input, context_faqs)
    
    if llm_response:
        return llm_response, "Gemini AI"

    # Fallback to direct FAQ match from RAG
    return f"**{best_match['question']}**\n\n{best_match['answer']}", "RAG Server"

# ============================================================
# MAIN LOOP
# ============================================================
def main():
    kb = load_kb()

    print("=" * 50)
    print("  IT Support Chatbot - Prototype")
    print("=" * 50)
    print("  Type your IT questions here")
    print("  Type 'quit' or 'exit' to leave")
    print("  Type 'help' to see all categories")
    print("=" * 50)
    print()

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

        response = get_response(user_input, kb)
        print(f"\nBot: {response}\n")

if __name__ == "__main__":
    main()
