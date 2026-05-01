#!/usr/bin/env python3
"""
IT Support Chatbot - สร้างไฟล์คู่มือ PDF แบบ Text-based
รัน: python3 create_guide.py
"""

import os

def create_text_guide():
    """สร้างไฟล์ Text สำหรับแชร์"""
    
    guide = """
════════════════════════════════════════════════════════════════════
                    🖥️  IT SUPPORT CHATBOT
                      คู่มือการใช้งาน
════════════════════════════════════════════════════════════════════


🚀 วิธีเปิดใช้งาน (3 ขั้นตอน)
──────────────────────────────────────────────────────────────────

    1. เปิด Terminal
    2. cd ~/it-support-chatbot
    3. python3 chatbot.py

    ✅ เสร็จ! เริ่มถามได้เลย


💬 ตัวอย่างการใช้
──────────────────────────────────────────────────────────────────

    🧑 คุณ: WiFi เชื่อมต่อไม่ได้
    🤖 Bot:  1. ตรวจว่าเปิด WiFi แล้ว
             2. Forget network แล้วเชื่อมต่อใหม่
             3. Restart เครื่อง
             4. ติดต่อ IT Support ext. 1234

    🧑 คุณ: ลืมรหัสผ่าน
    🤖 Bot:  1. กด Forgot Password
             2. ติดต่อ IT Support ext. 1234
             3. รหัสต้องมี 8 ตัว+ตัวใหญ่+ตัวเล็ก+ตัวเลข


⌨️  คำสั่งใน Chatbot
──────────────────────────────────────────────────────────────────

    คำถาม IT          → ถามได้เลย เช่น "คอมช้ามาก"
    help              → ดูหมวดหมู่ทั้งหมด
    quit / exit       → ออกจากโปรแกรม


📂 หมวดหมู่ที่มี (59 FAQ)
──────────────────────────────────────────────────────────────────

    🖨️  เครื่องพิมพ์           📶  Network/WiFi
    📧  อีเมล                 💻  คอมพิวเตอร์
    🔑  Password              📦  Software
    🔐  VPN                   📹  Video Conference
    📱  Mobile                💾  Backup/Restore
    👤  Account/Permission


💡 เคล็ดลับ
──────────────────────────────────────────────────────────────────

    ✅ พิมพ์คำถามสั้นๆ ได้ เช่น "WiFi", "printer", "ลืมรหัส"
    ✅ Chatbot จะแสดงคำตอบ + คำถามที่เกี่ยวข้อง
    ✅ ถ้าไม่พบคำตอบ จะแนะนำช่องทางติดต่อ IT Support
    ✅ FAQ แก้ไขได้ในไฟล์ knowledge_base.json


📞 ติดต่อ IT Support
──────────────────────────────────────────────────────────────────

    📞 โทร: ext. 1234
    📧 อีเมล: it-support@company.com
    💬 Line: @company-it
    🕐 เวลา: จันทร์-ศุกร์ 8:30-17:30


════════════════════════════════════════════════════════════════════
    IT Support Chatbot v1.0 | Prototype | สร้างด้วย Python
════════════════════════════════════════════════════════════════════
"""
    
    return guide

def create_html_guide():
    """สร้าง HTML สำหรับพิมพ์เป็น PDF"""
    
    html = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>IT Support Chatbot - คู่มือ</title>
    <style>
        body {
            font-family: Tahoma, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px;
            color: #333;
        }
        h1 { color: #667eea; text-align: center; }
        h2 { color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 5px; }
        .step { 
            background: #f5f5f5; 
            padding: 15px; 
            border-radius: 8px;
            margin: 10px 0;
        }
        code {
            background: #e0e0e0;
            padding: 2px 8px;
            border-radius: 4px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }
        th {
            background: #667eea;
            color: white;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
        }
    </style>
</head>
<body>
    <h1>🖥️ IT Support Chatbot</h1>
    <p style="text-align: center; color: #666;">คู่มือการใช้งาน</p>
    
    <h2>🚀 วิธีเปิดใช้งาน</h2>
    <div class="step">
        <strong>1.</strong> เปิด Terminal<br>
        <strong>2.</strong> พิมพ์: <code>cd ~/it-support-chatbot</code><br>
        <strong>3.</strong> รัน: <code>python3 chatbot.py</code><br>
        <strong>4.</strong> เสร็จ! เริ่มถามได้เลย 🎉
    </div>
    
    <h2>⌨️ คำสั่งใน Chatbot</h2>
    <table>
        <tr><th>พิมพ์</th><th>ทำอะไร</th></tr>
        <tr><td>คำถาม IT</td><td>ถามได้เลย เช่น "คอมช้ามาก"</td></tr>
        <tr><td><code>help</code></td><td>ดูหมวดหมู่ทั้งหมด</td></tr>
        <tr><td><code>quit</code> หรือ <code>exit</code></td><td>ออกจากโปรแกรม</td></tr>
    </table>
    
    <h2>📂 หมวดหมู่ที่มี (59 FAQ)</h2>
    <div class="step">
        🖨️ เครื่องพิมพ์ | 📶 Network | 📧 อีเมล | 💻 คอมพิวเตอร์<br>
        🔑 Password | 📦 Software | 🔐 VPN | 📹 Video Conference<br>
        📱 Mobile | 💾 Backup | 👤 Account
    </div>
    
    <h2>📞 ติดต่อ IT Support</h2>
    <div class="step">
        📞 โทร: ext. 1234<br>
        📧 อีเมล: it-support@company.com<br>
        💬 Line: @company-it<br>
        🕐 เวลา: จันทร์-ศุกร์ 8:30-17:30
    </div>
    
    <div class="footer">
        <p>IT Support Chatbot v1.0 | Prototype</p>
    </div>
</body>
</html>"""
    
    return html

if __name__ == "__main__":
    # สร้างไฟล์ Text
    text_guide = create_text_guide()
    with open("คู่มือใช้งาน.txt", "w", encoding="utf-8") as f:
        f.write(text_guide)
    print("✅ สร้างไฟล์: คู่มือใช้งาน.txt")
    
    # สร้างไฟล์ HTML
    html_guide = create_html_guide()
    with open("คู่มือใช้งาน.html", "w", encoding="utf-8") as f:
        f.write(html_guide)
    print("✅ สร้างไฟล์: คู่มือใช้งาน.html")
    
    print("\n📄 วิธีสร้าง PDF:")
    print("   1. เปิดไฟล์ คู่มือใช้งาน.html ใน Browser")
    print("   2. กด Ctrl+P (พิมพ์)")
    print("   3. เลือก 'Save as PDF'")
    print("   4. กด Save")
    
    print("\n💡 หรือแชร์ไฟล์ คู่มือใช้งาน.txt ได้เลย!")
