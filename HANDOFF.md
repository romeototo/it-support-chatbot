# 🖥️ IT Support Chatbot - Project Handoff

> **สร้างโดย:** Hermes Agent
> **วันที่:** 1 พฤษภาคม 2026
> **สถานะ:** Prototype พร้อมใช้งาน

---

## 📍 ข้อมูลโปรเจค

```
Path: /home/dmin/it-support-chatbot/
Language: Python 3
Dependencies: flask (optional)
Total Files: 9 ไฟล์
FAQ Count: 59 ข้อ / 11 หมวด
```

---

## 📁 โครงสร้างไฟล์

```
/home/dmin/it-support-chatbot/
│
├── 📄 chatbot.py              # ⭐ Chatbot หลัก (Terminal Mode)
├── 📄 web_app.py              # Web UI (Flask) - สวย มีปุ่มกด
├── 📄 knowledge_base.json     # ฐานความรู้ FAQ 59 ข้อ
├── 📄 create_guide.py         # สคริปต์สร้างคู่มือ
│
├── 📄 คู่มือใช้งาน.txt        # คู่มือ Text (แชร์ได้เลย)
├── 📄 คู่มือใช้งาน.html       # คู่มือ HTML (พิมพ์ PDF)
├── 📄 guide.html              # คู่มือแบบสวย (มีสีสัน)
├── 📄 GUIDE.md                # คู่มือ Markdown
└── 📄 README.md               # คู่มือ Developer
```

---

## 🎯 สิ่งที่ทำแล้ว

### 1. Chatbot Terminal (`chatbot.py`)
- ✅ Keyword Matching (ไม่ต้องมี API Key)
- ✅ รองรับภาษาไทย
- ✅ แสดงคำถามที่เกี่ยวข้อง
- ✅ Escalation เมื่อไม่พบคำตอบ
- ✅ Optional LLM API (Xiaomi Token Plan)

### 2. Web UI (`web_app.py`)
- ✅ Flask Web App
- ✅ Chat Interface สวยๆ
- ✅ Quick Buttons (ปุ่มลัด)
- ✅ API Endpoint (`/api/chat`)

### 3. Knowledge Base (`knowledge_base.json`)
- ✅ 11 หมวดหมู่
- ✅ 59 FAQ ครอบคลุมปัญหา IT ทั่วไป
- ✅ Keywords สำหรับค้นหา
- ✅ Escalation Contact

### 4. คู่มือใช้งาน
- ✅ ไฟล์ Text (แชร์ผ่าน Line/Email)
- ✅ ไฟล์ HTML (พิมพ์เป็น PDF)
- ✅ Markdown (สำหรับ GitHub)

---

## 📂 หมวดหมู่ FAQ (11 หมวด)

| # | หมวด | จำนวน FAQ | Keywords ตัวอย่าง |
|---|------|-----------|-------------------|
| 1 | 🖨️ เครื่องพิมพ์ | 6 | printer, พิมพ์, กระดาษติด |
| 2 | 📶 Network/WiFi | 6 | wifi, internet, เน็ตช้า |
| 3 | 📧 อีเมล | 7 | outlook, email, ส่งเมล |
| 4 | 💻 คอมพิวเตอร์ | 9 | คอมช้า, blue screen, แบต |
| 5 | 🔑 Password | 6 | ลืมรหัส, reset, 2fa |
| 6 | 📦 Software | 7 | install, zoom, teams |
| 7 | 🔐 VPN | 4 | vpn, remote, wfh |
| 8 | 📹 Video Conference | 4 | zoom, กล้อง, ไมค์ |
| 9 | 📱 Mobile | 3 | มือถือ, app, sync |
| 10 | 💾 Backup | 3 | ไฟล์หาย, backup, restore |
| 11 | 👤 Account | 4 | onboarding, permission |

---

## 🚀 วิธีรัน

### Terminal Mode
```bash
cd /home/dmin/it-support-chatbot
python3 chatbot.py
```

### Web Mode
```bash
cd /home/dmin/it-support-chatbot
pip install flask
python3 web_app.py
# เปิด http://localhost:5000
```

---

## 📊 Token Usage

| รายการ | จำนวน |
|--------|-------|
| Knowledge Base | ~5K tokens |
| ต่อ 1 คำถาม | ~500 tokens |
| 1,000 คำถาม/เดือน | ~500K tokens |
| Xiaomi 200M credits | ใช้ได้ ~400 เดือน |

---

## 🎯 สิ่งที่ทำต่อได้

### Priority 1: ปรับปรุงใช้งานจริง
- [ ] เปลี่ยน FAQ เป็นของบริษัทจริง
- [ ] เปลี่ยน Contact (เบอร์โทร, Email, Line)
- [ ] Deploy บน Server

### Priority 2: เพิ่มฟีเจอร์
- [ ] เชื่อม LLM API (ให้ตอบฉลาดขึ้น)
- [ ] เชื่อม Line OA Bot
- [ ] เชื่อม Telegram Bot
- [ ] เพิ่ม Feedback System (👍/👎)
- [ ] บันทึกคำถามที่ถามบ่อย

### Priority 3: ขั้นสูง
- [ ] RAG (Retrieval-Augmented Generation)
- [ ] Vector Database (FAISS/Pinecone)
- [ ] Admin Dashboard
- [ ] Analytics Dashboard
- [ ] Multi-language Support

---

## 🔧 การแก้ไข FAQ

แก้ไขไฟล์ `knowledge_base.json`:

```json
{
  "name": "หมวดหมู่",
  "keywords": ["คำค้น1", "คำค้น2"],
  "faqs": [
    {
      "question": "คำถาม?",
      "answer": "คำตอบ"
    }
  ]
}
```

---

## 📞 Contact Template

แก้ไขใน `knowledge_base.json`:

```json
"escalation": {
  "message": "ติดต่อ IT Support:\n📞 โทร: ext. 1234\n📧 อีเมล: it-support@company.com",
  "hotline": "ext. 1234"
}
```

---

## 🧪 ทดสอบ Chatbot

```bash
cd /home/dmin/it-support-chatbot

# ทดสอบ Terminal
echo "WiFi เชื่อมต่อไม่ได้
ลืมรหัสผ่าน
help
quit" | python3 chatbot.py

# ทดสอบ API
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "WiFi เชื่อมต่อไม่ได้"}'
```

---

## 📝 Notes

- ใช้ Python 3 ไม่ต้อง install อะไรเพิ่ม (除了 flask ถ้าอยากใช้ Web Mode)
- Keyword Matching ทำงานได้เลย ไม่ต้องมี API Key
- LLM API เป็น Optional (ตั้งค่าใน chatbot.py)
- แก้ไข FAQ ได้โดยตรงใน knowledge_base.json

---

## 🤝 Handoff Checklist

- [x] โค้ดพร้อมใช้งาน
- [x] FAQ ครบถ้วน
- [x] คู่มือใช้งาน
- [x] คู่มือ Developer
- [x] ตัวอย่างการทดสอบ
- [ ] ปรับแต่ง FAQ ตามบริษัท
- [ ] Deploy Server
- [ ] เชื่อม Chat Platform

---

**สร้างโดย Hermes Agent | 1 พฤษภาคม 2026**
**Path: /home/dmin/it-support-chatbot/**
