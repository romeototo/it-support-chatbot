#!/usr/bin/env python3
"""
IT Support Chatbot - Prototype
Simple FAQ-based chatbot with keyword matching + optional LLM
"""

import json
import re
import sys
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================
KB_FILE = Path(__file__).parent / "knowledge_base.json"

# Set to True to use LLM API for better responses (requires API key)
USE_LLM = False

# LLM Config (Xiaomi Token Plan)
LLM_API_URL = "https://token-plan-sgp.xiaomimimo.com/v1/chat/completions"
LLM_MODEL = "mimo-v2.5"
LLM_API_KEY = ""  # Add your tp-... key here

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
    """Generate response for user input."""
    matches = find_relevant_faqs(user_input, kb)

    if not matches:
        return kb["escalation"]["message"]

    best_score = matches[0][0]

    # Low confidence - suggest escalation
    if best_score < 2:
        return f"🤔 ไม่แน่ใจว่าตรงกับปัญหาหรือเปล่า ลองดูนี้:\n\n" + \
               "\n\n".join([f"💡 {faq['question']}\n{faq['answer']}" for _, faq, _ in matches]) + \
               f"\n\n❓ ถ้าไม่ตรง {kb['escalation']['message']}"

    # Try LLM for better response
    llm_response = llm_answer(user_input, matches)
    if llm_response:
        return llm_response

    # Return best FAQ match
    best_faq = matches[0][1]
    category = matches[0][2]

    response = f"📋 **{best_faq['question']}**\n\n{best_faq['answer']}"

    # Add related questions if available
    if len(matches) > 1:
        related = [f"• {faq['question']}" for _, faq, _ in matches[1:3]]
        response += f"\n\n🔗 คำถามที่เกี่ยวข้อง:\n" + "\n".join(related)

    return response

# ============================================================
# MAIN LOOP
# ============================================================
def main():
    kb = load_kb()

    print("=" * 50)
    print("  🖥️  IT Support Chatbot - Prototype")
    print("=" * 50)
    print("  พิมพ์คำถาม IT ของคุณได้เลย")
    print("  พิมพ์ 'quit' หรือ 'exit' เพื่อออก")
    print("  พิมพ์ 'help' เพื่อดูหมวดหมู่ทั้งหมด")
    print("=" * 50)
    print()

    while True:
        try:
            user_input = input("🧑 คุณ: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 ขอบคุณที่ใช้บริการ!")
            break

        if not user_input:
            continue

        if user_input.lower() in ["quit", "exit", "ออก", "q"]:
            print("👋 ขอบคุณที่ใช้บริการ!")
            break

        if user_input.lower() in ["help", "ช่วย", "หมวดหมู่"]:
            print("\n📂 หมวดหมู่ที่มี:")
            for cat in kb["categories"]:
                print(f"  • {cat['name']} ({len(cat['faqs'])} FAQ)")
            print(f"\n📞 ติดต่อ IT Support: {kb['escalation']['hotline']}")
            print()
            continue

        response = get_response(user_input, kb)
        print(f"\n🤖 Bot: {response}\n")

if __name__ == "__main__":
    main()
