"""
Template สำหรับเชื่อมต่อ IT Support AI กับ LINE Official Account
ต้องติดตั้ง: pip install flask line-bot-sdk google-generativeai
"""
import json
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai

app = Flask(__name__)

# TODO: ใส่ Token ของคุณจาก LINE Developers Console
LINE_CHANNEL_ACCESS_TOKEN = 'YOUR_LINE_CHANNEL_ACCESS_TOKEN'
LINE_CHANNEL_SECRET = 'YOUR_LINE_CHANNEL_SECRET'
GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# โหลด Knowledge Base
with open('knowledge_base.json', 'r', encoding='utf-8') as f:
    KB = json.load(f)

def get_relevant_faq(user_text):
    """ค้นหา FAQ ที่ตรงกับคำถามเบื้องต้น (แบบเดียวกับเว็บ)"""
    user_text = user_text.lower()
    best_match = None
    top_score = 0
    for cat in KB['categories']:
        for faq in cat['faqs']:
            score = 0
            for kw in cat['keywords']:
                if kw.lower() in user_text: score += 3
            for word in user_text.split():
                if word in faq['question'].lower() and len(word) > 1: score += 1
            if score > top_score:
                top_score = score
                best_match = faq
    return best_match if top_score > 0 else None

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    
    # 1. ลองให้ Gemini ตอบโดยใช้ Context จาก KB
    faq = get_relevant_faq(user_message)
    
    if faq:
        # มีข้อมูลใน KB ส่งให้ Gemini สรุป
        prompt = f"คุณคือ IT Support AI ของบริษัท ตอบคำถามพนักงานสั้นๆ และเป็นกันเอง\nอ้างอิงจากข้อมูลนี้:\nQ: {faq['question']}\nA: {faq['answer']}\n\nคำถามจากพนักงาน: {user_message}"
        try:
            response = model.generate_content(prompt)
            reply_text = response.text
        except Exception as e:
            reply_text = f"📋 {faq['question']}\n\n{faq['answer']}" # Fallback
    else:
        # ไม่มีข้อมูลใน KB
        reply_text = KB['escalation']['message']

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(port=5000, debug=True)
