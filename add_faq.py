import json, re

with open('kb.js', 'r', encoding='utf-8-sig') as f:
    raw = f.read()

# Extract JSON
json_str = raw.replace('window.KB = ', '').rstrip('\r\n;')
kb = json.loads(json_str)

# New categories to add
new_cats = [
  {
    "name": "Power BI",
    "keywords": ["power bi", "powerbi", "dashboard", "report", "bi", "analytics", "กราฟ", "รายงาน"],
    "faqs": [
      {"question": "Power BI เปิด Report ไม่ได้", "answer": "1. ตรวจว่า Login ด้วยบัญชีบริษัท\n2. ตรวจว่ามีสิทธิ์ดู Report\n3. ล้าง Browser Cache\n4. ลอง Browser อื่น\n5. ติดต่อ IT ext.1234"},
      {"question": "Power BI Data ไม่อัปเดต", "answer": "1. กด Refresh บน Report\n2. ตรวจ Scheduled Refresh ใน Settings\n3. ตรวจ Data Source Connection\n4. ติดต่อ IT ext.1234 หรือ Admin BI"},
      {"question": "ขอสิทธิ์ดู Power BI Dashboard ยังไง?", "answer": "1. ขอจากเจ้าของ Report โดยตรง\n2. หรือส่ง Request ผ่าน IT Service Desk\n3. แจ้งชื่อ Report + เหตุผล\n4. Manager Approve\n5. ติดต่อ IT ext.1234"},
      {"question": "Power BI Desktop ติดตั้งยังไง?", "answer": "1. ส่ง Request ขอติดตั้งผ่าน IT Service Desk\n2. IT จะ Install Power BI Desktop ให้\n3. Login ด้วยบัญชีบริษัท\n4. ใช้งานได้ฟรีสำหรับพนักงาน\n5. ติดต่อ IT ext.1234"}
    ]
  },
  {
    "name": "Azure AD / Entra ID",
    "keywords": ["azure", "azure ad", "entra", "sso", "single sign on", "conditional access", "cloud account", "identity"],
    "faqs": [
      {"question": "Azure AD SSO Login ไม่ได้", "answer": "1. ตรวจ Internet Connection\n2. ล้าง Browser Cache / Cookie\n3. ลอง Incognito Mode\n4. ตรวจว่า Password ไม่หมดอายุ\n5. ติดต่อ IT ext.1234"},
      {"question": "Conditional Access บล็อค Login", "answer": "1. อาจเกิดจาก: เครื่องไม่ Compliant หรือ VPN ไม่ได้เปิด\n2. ตรวจว่า VPN เปิดอยู่\n3. ลง Company Portal / Intune\n4. ตรวจ MFA ว่าผ่านหรือไม่\n5. ติดต่อ IT ext.1234"},
      {"question": "Account ถูก Disabled ใน Azure AD", "answer": "1. ติดต่อ IT ext.1234 ทันที\n2. แจ้ง Email + ชื่อพนักงาน\n3. อาจเกิดจาก: ลาออก, Suspicious Login, หรือ Admin Disable\n4. IT จะตรวจสอบและแก้ไขให้"},
      {"question": "ลงทะเบียนเครื่องใน Azure AD ยังไง?", "answer": "1. Settings > Accounts > Access work or school\n2. Connect > เชื่อมต่อบัญชีบริษัท\n3. หรือผ่าน Company Portal App\n4. IT จะ Push Policy ให้อัตโนมัติ\n5. ติดต่อ IT ext.1234"}
    ]
  },
  {
    "name": "IT Security Awareness",
    "keywords": ["security", "ความปลอดภัย", "phishing", "social engineering", "pdpa", "policy", "awareness", "zero trust"],
    "faqs": [
      {"question": "รู้ได้ยังไงว่าอีเมลนี้เป็น Phishing?", "answer": "1. ตรวจ Sender Email ให้ละเอียด (ไม่ใช่แค่ชื่อ)\n2. Hover Link ดู URL จริงก่อนคลิก\n3. มีการขอ Password / ข้อมูลส่วนตัว\n4. มี Urgency เช่น ด่วน! บัญชีจะถูกลบ\n5. ไฟล์แนบ .exe .zip แปลกๆ\n6. แจ้ง IT ext.1234 ถ้าสงสัย"},
      {"question": "Password ที่ดีควรเป็นยังไง?", "answer": "1. ยาวอย่างน้อย 12 ตัวอักษร\n2. มีตัวใหญ่+ตัวเล็ก+ตัวเลข+อักขระพิเศษ\n3. ไม่ซ้ำกับ Account อื่น\n4. ใช้ Password Manager\n5. เปลี่ยนทุก 90 วัน"},
      {"question": "ข้อมูลส่วนตัว PDPA ต้องระวังอะไร?", "answer": "1. อย่าเก็บข้อมูลส่วนตัวมากกว่าจำเป็น\n2. ลบข้อมูลเมื่อหมดความจำเป็น\n3. ไม่แชร์ข้อมูลลูกค้าออกภายนอก\n4. Lock Computer เมื่อเดินออกจากโต๊ะ\n5. ติดต่อ IT ถ้าสงสัยว่าข้อมูลรั่ว"},
      {"question": "ทำงาน Public WiFi ปลอดภัยไหม?", "answer": "1. ต้องต่อ VPN บริษัทก่อนเสมอ\n2. อย่าเข้าระบบบริษัทโดยไม่มี VPN\n3. ระวัง Shoulder Surfing (คนมองหน้าจอ)\n4. ล็อคหน้าจอเมื่อไม่ใช้\n5. ติดต่อ IT ext.1234"},
      {"question": "Social Engineering คืออะไร?", "answer": "1. การหลอกลวงให้เปิดเผยข้อมูล\n2. ตัวอย่าง: แอบอ้างเป็น IT / CEO\n3. ห้ามบอก Password แม้ IT จริงขอ\n4. ตรวจสอบ Identity ก่อนให้ข้อมูล\n5. แจ้ง IT ext.1234 ถ้าสงสัย"}
    ]
  },
  {
    "name": "Google Workspace",
    "keywords": ["google", "gmail", "google drive", "google docs", "google sheets", "google meet", "workspace", "g suite"],
    "faqs": [
      {"question": "Gmail บริษัทเข้าไม่ได้", "answer": "1. ตรวจ Internet Connection\n2. ล้าง Browser Cache\n3. ลอง Incognito Mode\n4. ตรวจว่าใช้ Email บริษัทถูกต้อง\n5. ติดต่อ IT ext.1234"},
      {"question": "Google Drive แชร์ไฟล์ยังไง?", "answer": "1. คลิกขวาไฟล์ > Share\n2. กรอกอีเมลผู้รับ\n3. เลือกสิทธิ์: Viewer / Commenter / Editor\n4. กด Send\n5. หรือ Copy Link สำหรับแชร์"},
      {"question": "Google Docs แก้ไขพร้อมกันหลายคนยังไง?", "answer": "1. แชร์ Link ให้ผู้ร่วมงาน (Editor)\n2. ทุกคนเปิด Link เดียวกัน\n3. เห็น Cursor ของกันและกัน Real-time\n4. Comment: Insert > Comment\n5. ประวัติแก้ไข: File > Version History"},
      {"question": "Google Meet กล้องหรือไมค์ไม่ทำงาน", "answer": "1. ตรวจ Permission ใน Browser\n2. Settings > Privacy > Camera/Microphone > เปิด\n3. Restart Browser\n4. ลอง Browser อื่น\n5. ติดต่อ IT ext.1234"}
    ]
  },
  {
    "name": "Microsoft Intune / MDM",
    "keywords": ["intune", "mdm", "company portal", "device compliance", "mobile device", "enrollment", "ลงทะเบียนเครื่อง"],
    "faqs": [
      {"question": "Company Portal ลงทะเบียนเครื่องยังไง?", "answer": "1. Download Company Portal จาก App Store\n2. Login ด้วยบัญชีบริษัท\n3. ทำตามขั้นตอนในแอป\n4. IT จะ Push App + Policy ให้อัตโนมัติ\n5. ติดต่อ IT ext.1234"},
      {"question": "Device Not Compliant แก้ยังไง?", "answer": "1. ตรวจ Company Portal > Device Details\n2. ดูว่าขาด Requirement ใด\n3. อาจต้อง: เปิด BitLocker, อัปเดต Windows\n4. ทำตามที่แนะนำ แล้วกด Check Compliance\n5. ติดต่อ IT ext.1234"},
      {"question": "IT Remote Wipe เครื่องได้ไหม?", "answer": "1. ได้ ถ้าเครื่องลงทะเบียน Intune\n2. ใช้เมื่อเครื่องสูญหายหรือถูกขโมย\n3. IT จะ Wipe เฉพาะข้อมูลบริษัท (Corporate Wipe)\n4. หรือ Full Wipe ถ้าเครื่องบริษัท\n5. แจ้ง IT ext.1234 ทันทีถ้าเครื่องหาย"}
    ]
  }
]

# Add new categories if not already there
existing_names = [c['name'] for c in kb['categories']]
added = 0
for cat in new_cats:
    if cat['name'] not in existing_names:
        kb['categories'].append(cat)
        added += 1

print(f"Added {added} new categories. Total: {len(kb['categories'])} categories")
total_faqs = sum(len(c['faqs']) for c in kb['categories'])
print(f"Total FAQs: {total_faqs}")

with open('kb.js', 'w', encoding='utf-8') as f:
    f.write('window.KB = ' + json.dumps(kb, ensure_ascii=False) + ';\n')

print("kb.js updated successfully!")
