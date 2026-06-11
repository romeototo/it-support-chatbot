# 🖥️ IT Support Chatbot v0.3.0 — คู่มือใช้งาน

---

## 🚀 วิธีเปิดใช้งาน

### วิธีที่ 1 — เปิดหน้าเว็บโดยตรง (Static Mode)
1. ดับเบิลคลิกไฟล์ `index.html`
2. เปิดในเว็บเบราว์เซอร์ได้ทันที
3. ใช้งาน Keyword Search + Gemini AI (ถ้ามี API Key)

### วิธีที่ 2 — รัน Backend Server (Full Mode)
```bash
# ติดตั้ง dependencies
pip install -r requirements.txt

# (Optional) ตั้งค่า environment variables
copy .env.example .env
# แก้ไขค่าใน .env ตามต้องการ

# รัน Server
python web_app.py
```
- เปิดเว็บ: http://localhost:5000
- Admin Dashboard: http://localhost:5000/dashboard

### วิธีที่ 3 — เปิดบน GitHub Pages
- เข้า https://romeototo.github.io/it-support-chatbot/
- ใช้งานได้ทันทีโดยไม่ต้องติดตั้ง

---

## 💡 ฟีเจอร์หลัก

| ฟีเจอร์ | รายละเอียด |
|---|---|
| 🔍 **Keyword Search** | ค้นหา FAQ อัตโนมัติจาก 202+ FAQ ใน 45+ หมวดหมู่ |
| 🤖 **Gemini AI Mode** | ใส่ API Key เพื่อใช้ AI ตอบคำถามอัจฉริยะ |
| 📊 **RAG Engine** | ค้นหาเชิงความหมาย (Semantic Search) ด้วย ChromaDB |
| 🎫 **Ticket System** | สร้าง/ติดตาม/ตอบกลับ ticket ผ่าน Admin Dashboard |
| 📈 **Analytics** | แสดงสถิติ กราฟ ข้อมูลเชิงลึกสำหรับ Admin |
| 🌐 **2 ภาษา** | ไทย / English |
| 🌗 **Dark/Light Mode** | สลับธีมได้ |
| 📱 **PWA** | ติดตั้งเป็นแอปบนมือถือ/เดสก์ท็อปได้ |
| 💬 **LINE Integration** | เชื่อมต่อ LINE Official Account (template) |

---

## 🎫 Admin Dashboard

1. เข้า http://localhost:5000/dashboard
2. Login ด้วย username/password ที่ตั้งไว้ใน `.env`
3. ฟีเจอร์:
   - ดู/ค้นหา/กรอง tickets
   - ตอบกลับ ticket
   - ปิด/เปิด ticket
   - ดู Analytics (กราฟสถิติ)

---

## ⚙️ การตั้งค่า

### Environment Variables
ดูตัวอย่างใน `.env.example`:

| ตัวแปร | รายละเอียด | ค่าเริ่มต้น |
|---|---|---|
| `GOOGLE_API_KEY` | Gemini API Key | (ว่าง) |
| `FLASK_SECRET_KEY` | Flask session secret | auto-generate |
| `FLASK_DEBUG` | เปิด debug mode | false |
| `ADMIN_USER` | ชื่อผู้ใช้ admin | admin |
| `ADMIN_PASS` | รหัสผ่าน admin | changeme |

### Gemini AI (Frontend)
1. คลิกปุ่ม ⚡ AI ที่ header
2. ใส่ Gemini API Key
3. กด Save — เปลี่ยนเป็น AI Mode ทันที

---

## 📂 โครงสร้างไฟล์

```
it-support-chatbot/
├── index.html              # หน้า Chatbot หลัก
├── dashboard.html          # Admin Dashboard
├── guide.html              # คู่มือพิมพ์ได้
├── web_app.py              # Flask Backend Server
├── chatbot.py              # Keyword + RAG + LLM Engine
├── rag_engine.py           # ChromaDB Vector Search
├── init_rag.py             # Script สร้าง RAG Database
├── add_faq.py              # Script เพิ่ม FAQ ใหม่
├── line_webhook_template.py # Template เชื่อม LINE
├── knowledge_base.json     # ฐานข้อมูล FAQ (JSON)
├── kb.js                   # ฐานข้อมูล FAQ (JS สำหรับ frontend)
├── requirements.txt        # Python dependencies
├── .env.example            # ตัวอย่าง environment variables
├── manifest.json           # PWA manifest
├── sw.js                   # Service Worker
└── config.json             # Config (gitignored)
```

---

## 🆘 แก้ปัญหาเบื้องต้น

| ปัญหา | วิธีแก้ |
|---|---|
| Bot ตอบไม่ตรง | ลองพิมพ์คำถามใหม่ให้ชัดเจนขึ้น |
| Gemini AI ไม่ทำงาน | ตรวจสอบ API Key + Internet |
| Dashboard เข้าไม่ได้ | ตรวจ username/password ใน .env |
| ข้อมูลไม่อัปเดต | Restart server: `python web_app.py` |
| RAG ค้นไม่เจอ | รัน `python init_rag.py` เพื่อ re-index |

---

## 📞 ติดต่อ IT Support
- 📧 Email: it-support@company.com
- 📞 โทร: ext. 1234
- 💬 LINE: @company-it
