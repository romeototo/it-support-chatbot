#!/usr/bin/env python3
"""
IT Support Chatbot - Web UI
Simple Flask web interface for the chatbot
"""

from flask import Flask, request, jsonify, render_template_string
from chatbot import load_kb, get_response
import json

app = Flask(__name__)
kb = load_kb()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IT Support Chatbot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .chat-container {
            width: 450px;
            height: 650px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .chat-header h1 { font-size: 1.3em; }
        .chat-header p { font-size: 0.85em; opacity: 0.9; margin-top: 5px; }
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .message {
            margin-bottom: 15px;
            display: flex;
        }
        .message.user { justify-content: flex-end; }
        .message.bot { justify-content: flex-start; }
        .message-content {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 18px;
            font-size: 14px;
            line-height: 1.5;
            white-space: pre-wrap;
        }
        .message.user .message-content {
            background: #667eea;
            color: white;
            border-bottom-right-radius: 5px;
        }
        .message.bot .message-content {
            background: white;
            color: #333;
            border-bottom-left-radius: 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .quick-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            padding: 10px 20px;
            background: white;
            border-top: 1px solid #eee;
        }
        .quick-btn {
            padding: 6px 14px;
            background: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 20px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.2s;
        }
        .quick-btn:hover {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        .chat-input {
            display: flex;
            padding: 15px;
            background: white;
            border-top: 1px solid #eee;
        }
        .chat-input input {
            flex: 1;
            padding: 12px 16px;
            border: 1px solid #ddd;
            border-radius: 25px;
            outline: none;
            font-size: 14px;
        }
        .chat-input input:focus { border-color: #667eea; }
        .chat-input button {
            margin-left: 10px;
            padding: 12px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.2s;
        }
        .chat-input button:hover { background: #5a6fd6; }
        .typing { opacity: 0.5; font-style: italic; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>🖥️ IT Support Chatbot</h1>
            <p>Prototype - พร้อมช่วยเหลือปัญหา IT ของคุณ</p>
        </div>
        <div class="chat-messages" id="messages">
            <div class="message bot">
                <div class="message-content">สวัสดีครับ! 👋 ผมเป็น IT Support Chatbot\nพิมพ์ปัญหา IT ของคุณได้เลย\nหรือกดปุ่มด้านล่างเพื่อเลือกหมวดหมู่</div>
            </div>
        </div>
        <div class="quick-buttons">
            <button class="quick-btn" onclick="askQuestion('เครื่องพิมพ์พิมพ์ไม่ออก')">🖨️ เครื่องพิมพ์</button>
            <button class="quick-btn" onclick="askQuestion('เชื่อมต่อ WiFi ไม่ได้')">📶 WiFi</button>
            <button class="quick-btn" onclick="askQuestion('ลืมรหัสผ่าน')">🔑 ลืมรหัส</button>
            <button class="quick-btn" onclick="askQuestion('คอมช้ามาก')">💻 คอมช้า</button>
            <button class="quick-btn" onclick="askQuestion('ส่งอีเมลไม่ได้')">📧 อีเมล</button>
            <button class="quick-btn" onclick="askQuestion('ติดตั้งโปรแกรม')">📦 ลงโปรแกรม</button>
        </div>
        <div class="chat-input">
            <input type="text" id="userInput" placeholder="พิมพ์ปัญหา IT ของคุณ..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">ส่ง</button>
        </div>
    </div>

    <script>
        function handleKeyPress(e) {
            if (e.key === 'Enter') sendMessage();
        }

        function askQuestion(q) {
            document.getElementById('userInput').value = q;
            sendMessage();
        }

        function sendMessage() {
            const input = document.getElementById('userInput');
            const text = input.value.trim();
            if (!text) return;

            addMessage(text, 'user');
            input.value = '';

            // Show typing indicator
            const typingDiv = addMessage('กำลังคิด...', 'bot typing');

            fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: text})
            })
            .then(r => r.json())
            .then(data => {
                typingDiv.remove();
                addMessage(data.response, 'bot');
            })
            .catch(() => {
                typingDiv.remove();
                addMessage('เกิดข้อผิดพลาด กรุณาลองใหม่', 'bot');
            });
        }

        function addMessage(text, className) {
            const div = document.createElement('div');
            div.className = `message ${className}`;
            div.innerHTML = `<div class="message-content">${text}</div>`;
            document.getElementById('messages').appendChild(div);
            div.scrollIntoView({behavior: 'smooth'});
            return div;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()
    if not user_input:
        return jsonify({"response": "กรุณาพิมพ์คำถาม"})
    
    response = get_response(user_input, kb)
    return jsonify({"response": response})

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "faqs": sum(len(c["faqs"]) for c in kb["categories"])})

if __name__ == "__main__":
    print("🚀 Starting IT Support Chatbot Web UI...")
    print("🌐 Open: http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
