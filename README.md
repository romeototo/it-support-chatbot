# 🖥️ IT Support AI Chatbot

[![GitHub Pages](https://img.shields.io/badge/Demo-Live-brightgreen?style=for-the-badge&logo=github)](https://romeototo.github.io/it-support-chatbot/)
[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

> ระบบ AI Chatbot สำหรับช่วยงาน IT Support ภายในองค์กร  
> ตอบคำถามปัญหาไอทีได้ทันที ลด Ticket และประหยัดเวลา IT Team

---

## 📋 Case Study — ทำไมถึงสร้างโปรเจกต์นี้?

### ❓ ปัญหา (Problem)

ทีม IT Support ในองค์กรทั่วไปใช้เวลา **30-40%** ไปกับการตอบคำถามซ้ำๆ เช่น:
- "WiFi เชื่อมไม่ได้"
- "ลืมรหัสผ่าน"
- "เครื่องพิมพ์ใช้ไม่ได้"

สิ่งเหล่านี้เป็นปัญหาที่มี **ขั้นตอนการแก้ไขตายตัว** แต่ต้องรอ IT มาช่วยทุกครั้ง ทำให้:
- พนักงานรอนาน → ผลิตภาพลดลง
- IT Team เหนื่อยกับงานซ้ำซาก → ไม่มีเวลาทำงาน Infrastructure
- Ticket สะสม → SLA ไม่ผ่าน

### 💡 แนวทางแก้ไข (Solution)

สร้าง **AI Chatbot** ที่พนักงานเปิดใช้งานได้ทันทีผ่าน Browser โดย:

| องค์ประกอบ | รายละเอียด |
|---|---|
| 📚 Knowledge Base | รวบรวม **202 FAQ** จากปัญหาจริงใน **45 หมวดหมู่** |
| 🤖 AI Engine | ใช้ **Google Gemini API** วิเคราะห์คำถามและตอบอัจฉริยะ |
| ⚡ Keyword Fallback | ทำงานได้แม้ไม่มี Internet (Offline Mode) |
| 🎫 Ticket Tracking | ออกหมายเลข Ticket + ประวัติสนทนา |
| 📊 Feedback Loop | ระบบ 👍👎 เพื่อปรับปรุง FAQ ต่อเนื่อง |

### 📈 ผลลัพธ์ที่คาดหวัง (Expected Impact)

```
🎯 ลด Ticket ซ้ำซาก        → ประมาณ 40%
⏱️ ลดเวลารอ IT            → จาก 30 นาที เหลือ 30 วินาที
📊 เพิ่มเวลา IT Team       → ไปทำ Infrastructure + Security
🌐 เข้าถึงได้ 24/7         → ไม่ต้องรอเวลาทำการ
```

### 🔮 ขั้นตอนถัดไป (Next Phase)

1. เชื่อมต่อ **LINE OA / Telegram** เพื่อเข้าถึงพนักงานในช่องทางที่ใช้อยู่แล้ว
2. ใช้ **RAG + Vector Database** เพื่อค้นหาจากเอกสาร IT จริง (PDF, Wiki)
3. สร้าง **Admin Dashboard** เพื่อวิเคราะห์ปัญหาที่เกิดบ่อย และปรับปรุงเชิงรุก

---

## 🚀 Live Demo

**👉 [เปิด Demo ได้เลย](https://romeototo.github.io/it-support-chatbot/)**

![IT Support Chatbot Screenshot](screenshot.png)

---

## ✨ Features

| Feature | รายละเอียด |
|---|---|
| 💬 Chat Interface | UI สวย Dark Theme พร้อม Typing Animation |
| 🤖 Gemini AI | เชื่อมต่อ Google Gemini API ตอบอัจฉริยะ |
| 🔍 Keyword Fallback | Keyword Matching เมื่อไม่มี API Key |
| 📋 202 FAQ | ครอบคลุม 45 หมวดหมู่ปัญหา IT ทั่วไป |
| ⚡ Quick Actions | ปุ่มลัด 16 หัวข้อ กดได้เลย |
| 🎫 Ticket System | ออก Ticket Number + History Panel |
| 👍👎 Feedback | ปุ่มให้คะแนนทุก Ticket |
| 📊 Stats Bar | สถิติ Ticket / Helpful / Mode แบบ Real-time |
| 📱 Responsive | รองรับ Desktop + Mobile |
| 🌐 Standalone | ทำงานได้ใน Browser ไม่ต้อง Server |

---

## 📂 หมวดหมู่ FAQ (45 หมวด / 202 ข้อ)

```
🖨️ เครื่องพิมพ์          📶 WiFi / Network       📧 อีเมล / Outlook
💻 คอมพิวเตอร์            🔑 Password / Security  📦 Software
🔐 VPN / Remote Work     📹 Video Conference     📱 Mobile / BYOD
💾 Backup / Recovery      👤 Account / AD          💬 Microsoft Teams
🔌 Hardware / USB         🗂️ Network Drive        📊 Office 365
🪟 Windows System         🛡️ Antivirus / PDPA     🌐 Browser / Chrome
🖥️ Remote Desktop        💥 Blue Screen / BSOD    📞 IP Phone
📽️ Projector             ☁️ Cloud Storage         🔐 MFA / 2FA
📊 Excel / Word / PPT    🔊 Audio / ลำโพง        ⚡ Power / UPS
```

---

## 🛠️ Tech Stack

```
Frontend   → HTML5 + Vanilla CSS + JavaScript (ES6+)
Backend    → Python 3 + Flask
AI Engine  → Keyword Matching + Optional LLM API
Data       → JSON Knowledge Base (knowledge_base.json)
Deploy     → GitHub Pages (Frontend) / Any Server (Backend)
```

---

## ⚡ วิธีใช้งาน

### วิธีที่ 1 — เปิดใน Browser (ง่ายสุด)
```bash
# เปิดไฟล์ index.html ใน Browser โดยตรง
# ไม่ต้อง Install อะไรเพิ่ม
```

### วิธีที่ 2 — Web Mode (Flask)
```bash
# Clone โปรเจกต์
git clone https://github.com/romeototo/it-support-chatbot.git
cd it-support-chatbot

# ติดตั้ง Flask
pip install flask

# รัน Web App
python web_app.py
# เปิด http://localhost:5000
```

### วิธีที่ 3 — Terminal Mode
```bash
python chatbot.py
```

---

## 📁 โครงสร้างโปรเจกต์

```
it-support-chatbot/
├── 🌟 index.html              # Standalone Demo (GitHub Pages)
├── 🐍 chatbot.py              # Terminal Chatbot
├── 🌐 web_app.py              # Flask Web Application
├── 📚 knowledge_base.json     # FAQ Database (202 ข้อ / 45 หมวด)
├── 📄 README.md               # คู่มือนี้
├── 📄 GUIDE.md                # คู่มือการใช้งาน
└── 📄 requirements.txt        # Python Dependencies
```

---

## 🔧 การเพิ่ม FAQ

แก้ไขไฟล์ `knowledge_base.json`:

```json
{
  "name": "หมวดหมู่ใหม่",
  "keywords": ["keyword1", "keyword2"],
  "faqs": [
    {
      "question": "คำถาม?",
      "answer": "1. ขั้นตอนที่ 1\n2. ขั้นตอนที่ 2"
    }
  ]
}
```

---

## 🗺️ Roadmap

- [x] Keyword Matching Engine
- [x] Flask Web UI
- [x] 202 FAQ / 45 หมวดหมู่
- [x] Standalone HTML Demo
- [x] GitHub Pages Deploy
- [x] Gemini AI Integration
- [x] Ticket History Panel
- [x] Feedback System (👍👎)
- [x] Mobile Responsive
- [x] Stats Dashboard
- [ ] LINE OA Bot
- [ ] Telegram Bot
- [ ] Admin Dashboard
- [ ] RAG + Vector Database

---

## 📞 ติดต่อ IT Support

```
📞 โทร: ext. 1234
📧 อีเมล: it-support@company.com
💬 Line: @company-it
🕐 จันทร์-ศุกร์ 8:30-17:30
```

---

## 👨‍💻 Author

**romeototo** — IT Support & Developer  
[![GitHub](https://img.shields.io/badge/GitHub-romeototo-black?style=flat&logo=github)](https://github.com/romeototo)

---

*สร้างด้วย ❤️ เพื่อลด Ticket และช่วยให้ทีม IT ทำงานได้มีประสิทธิภาพมากขึ้น*
