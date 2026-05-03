# 🤖 IT Support AI — Premium Intelligent HelpDesk

<div align="center">

![IT Support AI Demo](https://romeototo.github.io/it-support-chatbot/screenshot.png)

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-GitHub_Pages-6366f1?style=for-the-badge)](https://romeototo.github.io/it-support-chatbot/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-RAG-orange?style=for-the-badge)](https://www.trychroma.com)
[![Gemini AI](https://img.shields.io/badge/Gemini_AI-Optional-4285f4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**ระบบ IT HelpDesk อัจฉริยะ พร้อม Hybrid AI Search Engine, Premium Glassmorphism UI และฐานข้อมูล 202 FAQ ภาษาไทย**

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Hybrid Search** | ค้นหาด้วย Keyword ก่อน → ถ้าไม่เจอจึง fallback ไป RAG (ChromaDB Vector DB) |
| 📚 **202 FAQ / 45 หมวด** | ฐานข้อมูลครอบคลุมปัญหา IT ทุกประเภทในองค์กร |
| 🤖 **Gemini AI Integration** | ใส่ API Key เพื่อเปิดโหมด AI ตอบแบบ Natural Language |
| 💎 **Premium Glassmorphism UI** | ดีไซน์ Dark Mode ระดับ Premium พร้อม Micro-animations |
| 📋 **Copy Answer Button** | คัดลอกคำตอบได้ในคลิกเดียว |
| 👍👎 **Feedback System** | พนักงานให้คะแนนคำตอบได้ บอท Track ความแม่นยำ |
| 🎫 **Ticket Tracking** | บันทึก Ticket History แบบ Real-time |
| 📱 **Responsive Design** | รองรับทุกขนาดหน้าจอ (Desktop / Tablet) |
| 🌐 **Dual Mode** | รันได้ทั้งบน Flask (Local) และ GitHub Pages (Static) |

---

## 🏗️ Tech Stack

```
Frontend:  HTML5 + Vanilla CSS (Glassmorphism) + JavaScript
Backend:   Python 3 + Flask + ChromaDB (Vector DB)
AI Engine: Hybrid (Keyword Match → RAG → Gemini API)
Deploy:    GitHub Pages (Frontend) / Local Flask (Full Stack)
```

---

## 🚀 Quick Start

### Option A — GitHub Pages (Frontend Only, ไม่ต้องติดตั้งอะไร)
เข้า **[https://romeototo.github.io/it-support-chatbot/](https://romeototo.github.io/it-support-chatbot/)** ได้เลยครับ

### Option B — Local Full Stack (พร้อม RAG Backend)

```bash
# 1. Clone repo
git clone https://github.com/romeototo/it-support-chatbot.git
cd it-support-chatbot

# 2. ติดตั้ง dependencies
pip install flask chromadb sentence-transformers

# 3. สร้าง Vector Database จาก FAQ
python init_rag.py

# 4. รัน Server
python web_app.py

# 5. เปิด Browser
http://localhost:5000
```

---

## 📂 Project Structure

```
it-support-chatbot/
├── index.html          # Frontend (Glassmorphism UI + Chat Logic)
├── kb.js               # Knowledge Base (202 FAQ สำหรับ GitHub Pages)
├── knowledge_base.json # Knowledge Base (สำหรับ Flask Backend)
├── web_app.py          # Flask Server + API Routes
├── chatbot.py          # Hybrid Search Engine (Keyword + RAG)
├── rag_engine.py       # ChromaDB Vector Search Engine
└── init_rag.py         # Script สำหรับ Ingest ข้อมูลเข้า Vector DB
```

---

## 🧠 How the AI Works

```
User Question
      │
      ▼
┌─────────────────────┐
│  Keyword Matching   │ ← เร็ว + แม่นยำสำหรับภาษาไทย
│  (Score ≥ 3)        │
└──────────┬──────────┘
           │ ไม่พบ
           ▼
┌─────────────────────┐
│  RAG Vector Search  │ ← ChromaDB Semantic Search
│  (ChromaDB)         │
└──────────┬──────────┘
           │ ไม่พบ
           ▼
┌─────────────────────┐
│  Gemini AI (LLM)    │ ← ถ้ามี API Key
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Escalation Message │ ← ติดต่อ IT ext.1234
└─────────────────────┘
```

---

## 📊 Knowledge Base Coverage (202 FAQs)

| หมวดหมู่ | ตัวอย่างปัญหา |
|---|---|
| 🖨️ Printer | พิมพ์ไม่ออก, กระดาษติด, ตั้ง Default Printer |
| 📶 Network/WiFi | เชื่อมต่อไม่ได้, ช้า, Map Drive |
| 🔑 Password/Security | ลืมรหัสผ่าน, MFA/2FA, Account Lock |
| 💻 Hardware | คอมช้า, USB ไม่ขึ้น, Dual Monitor |
| 📧 Email/Outlook | ส่งเมลไม่ได้, Attachment ใหญ่, Signature |
| 🔐 VPN/Remote | เชื่อมต่อไม่ได้, WFH Setup, RDP |
| 📹 Video Conference | Zoom/Teams กล้องไม่ทำงาน, Share Screen |
| 📊 Microsoft 365 | Office หมดอายุ, Excel ค้าง, Teams |
| 👤 HR/Onboarding | พนักงานใหม่, ลาออก, Account สิทธิ์ |
| + 36 หมวดอื่นๆ | ... |

---

## 🤝 Contributing

1. Fork repo นี้
2. สร้าง Branch ใหม่: `git checkout -b feature/add-faqs`
3. เพิ่ม FAQ ใน `knowledge_base.json` และ `kb.js`
4. รัน `python init_rag.py` เพื่อ Update Vector DB
5. Pull Request มาได้เลย!

---

## 📄 License

MIT License — ใช้งานได้ฟรีทั้งงาน Personal และ Commercial ครับ

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/romeototo">Romeo</a> | Powered by Python + ChromaDB + Gemini AI
</div>
