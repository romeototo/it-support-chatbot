# 🤖 IT Support AI — Premium Intelligent HelpDesk

<div align="center">

<!-- <img src="screenshot.png" alt="IT Support AI Chatbot" width="49%"> <img src="screenshot-dashboard.png" alt="Admin Dashboard" width="49%"> -->
<img src="screenshot.png" alt="IT Support AI Chatbot" width="80%">

*(เพื่อความสมบูรณ์แบบ แนะนำให้แคปภาพหน้าจอ Admin Dashboard ตั้งชื่อไฟล์ว่า `screenshot-dashboard.png` มาไว้ในโฟลเดอร์นี้ แล้วลบ Comment โค้ดด้านบนออกครับ)*

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-GitHub_Pages-6366f1?style=for-the-badge)](https://romeototo.github.io/it-support-chatbot/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-RAG-ff6b35?style=for-the-badge)](https://www.trychroma.com)
[![Gemini AI](https://img.shields.io/badge/Gemini_AI-Optional-4285f4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![Chart.js](https://img.shields.io/badge/Chart.js-Analytics-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

**ระบบ IT HelpDesk อัจฉริยะ พร้อม Hybrid AI Search Engine, Premium Glassmorphism UI**  
**ฐานข้อมูล 222 FAQ / 50 หมวดหมู่ ภาษาไทย ครอบคลุมทุกปัญหา IT ในองค์กร**

### 🌐 Live Demo & Portfolio Showcase
- **[User Chatbot Interface](https://romeototo.github.io/it-support-chatbot/)** — หน้าแชทบอทสำหรับผู้ใช้งาน แจ้งปัญหาและรับการวิเคราะห์เบื้องต้น
- **[Admin Dashboard (HelpDesk Pro)](https://romeototo.github.io/it-support-chatbot/dashboard.html)** — แดชบอร์ดสำหรับเจ้าหน้าที่ IT เพื่อรับ Ticket และตอบกลับผู้ใช้
*(**Pro Tip:** เปิด 2 หน้าจอพร้อมกันเพื่อดูการซิงค์ข้อมูล **Real-Time Hybrid Sync** แบบสดๆ!)*

</div>

---

## 💼 Business Value & Impact

- **Cost Reduction (Zero Server Cost):** โหมด Hybrid Sync สื่อสารผ่าน Web Storage API ทำให้สามารถทำงานบน GitHub Pages ได้โดยไม่ต้องเสียค่าเช่า Server ประหยัดงบประมาณ IT 100%
- **Time Efficiency:** บอทช่วยตอบคำถามพื้นฐาน (Tier 1) กว่า 222 อาการ ทำให้เจ้าหน้าที่ IT มีเวลาไปโฟกัสกับปัญหาที่ซับซ้อนขึ้น
- **Seamless Handoff:** หากบอทแก้ปัญหาไม่ได้ ระบบจะเปิด Ticket และซิงค์ข้อมูลไปที่ Admin ทันที ผู้ใช้ไม่ต้องอธิบายปัญหาซ้ำ

---

## ✨ Features

| Feature | Description |
|---|---|
| 👨‍💻 **Admin Dashboard** | หน้าจอ HelpDesk Pro จัดการ Ticket คิวงานแบบ Enterprise |
| ⚡ **Real-Time Hybrid Sync** | ซิงค์ข้อมูลข้ามแท็บระหว่าง User และ Admin ด้วย LocalStorage |
| ⌨️ **Admin Typing Indicator** | สถานะ "Admin กำลังพิมพ์" ซิงค์ไปยังหน้าจอผู้ใช้แบบ Real-time |
| 📊 **Live Analytics** | สรุปข้อมูลหมวดหมู่ปัญหาและ Resolution Rate ด้วย Chart.js |
| 🔍 **Search & Filter** | ค้นหา Ticket ID/Keyword และกรองสถานะ (Open/Closed) ได้ทันที |
| ⚡ **Canned Responses** | ปุ่มตอบกลับด่วนสำหรับ Admin ลดเวลาในการพิมพ์ |
| 🔍 **Hybrid Search Engine** | Keyword Matching → RAG (ChromaDB) → Gemini AI — 3 ชั้นความแม่นยำ |
| 📚 **222 FAQ / 50 หมวดหมู่** | ครอบคลุมทุกปัญหา IT ในองค์กร ภาษาไทย 100% |
| 🤖 **Gemini AI Integration** | ใส่ API Key เพื่อเปิดโหมด AI ตอบแบบ Natural Language |
| 💎 **Premium Glassmorphism UI** | Dark Mode + Light Mode สลับได้ พร้อม Micro-animations |
| ⌨️ **Typewriter Animation** | บอทพิมพ์คำตอบทีละตัวอักษร เหมือน ChatGPT |
| 📖 **Smart Collapse** | คำตอบยาวๆ ย่อได้ พร้อมปุ่ม "ดูคำตอบเต็ม" |
| 📋 **Copy to Clipboard** | คัดลอกคำตอบได้ในคลิกเดียว |
| 👍👎 **Feedback System** | ให้คะแนนคำตอบได้ บันทึกใน LocalStorage |
| 🎫 **Ticket History** | บันทึกประวัติการสนทนาแบบ Real-time + Persist หลัง Refresh |
| 🌐 **Dual Deploy Mode** | รันได้ทั้งบน Flask (Full Stack) และ GitHub Pages (Static) |

---

## 🏗️ Tech Stack

```
Frontend:  HTML5 + Vanilla CSS (Glassmorphism) + JavaScript (ES6+)
Backend:   Python 3.10+ + Flask + ChromaDB (Vector DB)
AI Engine: Hybrid (Keyword Match → RAG → Gemini 2.0 Flash API)
Fonts:     Google Fonts — Outfit
Deploy:    GitHub Pages (Frontend) / Local Flask (Full Stack)
```

---

## 🧠 System Architecture

### 1. Hybrid Search Engine (Chatbot)
```
User Question
      │
      ▼
┌─────────────────────┐
│  Keyword Matching   │ ← เร็ว + แม่นยำสำหรับภาษาไทย (Score ≥ 3)
└──────────┬──────────┘
           │ ไม่พบ
           ▼
┌─────────────────────┐
│  RAG Vector Search  │ ← ChromaDB Semantic Search (sentence-transformers)
└──────────┬──────────┘
           │ ไม่พบ / ความมั่นใจต่ำ
           ▼
┌─────────────────────┐
│  Gemini AI (LLM)    │ ← Google Gemini 2.0 Flash (ถ้ามี API Key)
└──────────┬──────────┘
           │ ไม่พบ
           ▼
┌─────────────────────┐
│  Escalation Message │ ← เปิด Ticket ส่งให้ Admin
└─────────────────────┘
```

### 2. Real-Time Hybrid Sync (Admin Dashboard)
การทำงานแบบ **Serverless** บน GitHub Pages ที่ใช้ Web Storage API (`localStorage` + `storage event`) เพื่อจำลองระบบ Real-time Database

```
[ User Chatbot ] ──(Save to LocalStorage)──> [ Admin Dashboard ]
       ▲                                            │
       │                                            ▼
   (Event Triggered) ◄──(Reply & Sync Status)───────┘
```
- ⚡ ซิงค์การพิมพ์แบบสดๆ (Typing Indicator)
- ⚡ ซิงค์สถานะ Ticket (Open/Closed) อัตโนมัติ
- 📊 ดึงข้อมูล Ticket มาทำ Analytics แบบ Real-time

---

## 🚀 Quick Start

### Option A — GitHub Pages (ไม่ต้องติดตั้งอะไร)

👉 เข้า **[https://romeototo.github.io/it-support-chatbot/](https://romeototo.github.io/it-support-chatbot/)** ได้เลย

### Option B — Local Full Stack (พร้อม RAG Backend)

```bash
# 1. Clone repo
git clone https://github.com/romeototo/it-support-chatbot.git
cd it-support-chatbot

# 2. ติดตั้ง dependencies
pip install -r requirements.txt

# 3. สร้าง Vector Database จาก FAQ
python init_rag.py

# 4. รัน Server
python web_app.py

# 5. เปิด Browser
# http://localhost:5000
```

### Option C — เปิดใช้ Gemini AI Mode

1. รับ API Key ฟรีที่ [Google AI Studio](https://aistudio.google.com)
2. กดปุ่ม ⚙️ AI ที่มุมขวาบน
3. วาง API Key แล้วกด **Activate AI**

---

## 📂 Project Structure

```
it-support-chatbot/
├── index.html           # Frontend Chatbot (Glassmorphism UI)
├── dashboard.html       # Admin Dashboard (HelpDesk Pro + Chart.js)
├── kb.js                # Knowledge Base 222 FAQ สำหรับ GitHub Pages (Static)
├── knowledge_base.json  # Knowledge Base สำหรับ Flask Backend
├── requirements.txt     # Python dependencies
├── web_app.py           # Flask Server + REST API Routes สำหรับทำ Full-Stack
├── chatbot.py           # Hybrid Search Engine (Keyword + RAG + Gemini)
├── rag_engine.py        # ChromaDB Vector Search Engine
├── init_rag.py          # Script สำหรับ Ingest FAQ เข้า Vector DB
└── screenshot.png       # Demo Screenshot
```

---

## 📊 Knowledge Base Coverage (222 FAQs / 50 Categories)

| หมวดหมู่ | ตัวอย่างปัญหา |
|---|---|
| 🖨️ Printer | พิมพ์ไม่ออก, กระดาษติด, Toner หมด, Duplex |
| 📶 Network/WiFi | เชื่อมต่อไม่ได้, DNS Error, IP Address, Map Drive |
| 🔑 Password/Security | ลืมรหัสผ่าน, MFA/2FA, PDPA, Phishing |
| 💻 Hardware | คอมช้า, BSOD, USB ไม่ขึ้น, Dual Monitor |
| 📧 Email/Outlook | ส่งเมลไม่ได้, Signature, Calendar, Archive |
| 🔐 VPN/Remote | เชื่อมต่อไม่ได้, WFH Setup, RDP |
| 📹 Video Conference | Zoom/Teams, Google Meet, Share Screen, Virtual BG |
| 📊 Microsoft 365 | Office Activation, Excel, Word, PowerPoint |
| ☁️ Cloud Storage | OneDrive, SharePoint, Google Drive |
| 🛡️ Security | Antivirus, Ransomware, BitLocker, PDPA |
| 📱 Mobile/BYOD | Intune, Company Portal, Email บนมือถือ |
| 📈 Power BI | Dashboard, Report, Permissions |
| ☁️ Azure AD | SSO, Conditional Access, Entra ID |
| 🌐 Google Workspace | Gmail, Google Docs, Google Meet |
| + 36 หมวดอื่นๆ | Active Directory, Backup, IP Phone, Projector, ... |

---

## 🤝 Contributing

1. Fork repo นี้
2. สร้าง Branch ใหม่: `git checkout -b feature/add-faqs`
3. เพิ่ม FAQ ใน `knowledge_base.json` และ `kb.js`
4. รัน `python init_rag.py` เพื่อ Update Vector DB
5. Pull Request มาได้เลย!

---

## 📄 License

MIT License — ใช้งานได้ฟรีทั้งงาน Personal และ Commercial

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/romeototo">Romeo</a> | Powered by Python · ChromaDB · Gemini AI
</div>
