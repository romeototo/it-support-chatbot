import json

new_categories = [
  {
    "name": "Microsoft Teams",
    "keywords": ["teams","microsoft teams","แชท","channel","ช่อง","notification","แจ้งเตือน","status","สถานะ","meeting teams"],
    "faqs": [
      {"question":"Teams เปิดไม่ขึ้น / ค้าง ทำยังไง?","answer":"1. ปิดจาก Task Manager (Ctrl+Shift+Esc)\n2. ลบ Cache: %AppData%\\Microsoft\\Teams\\Cache\n3. Restart Teams\n4. Update เป็น Version ล่าสุด\n5. ถ้ายังไม่ได้ ติดต่อ IT ext.1234"},
      {"question":"Teams แจ้งเตือนไม่ขึ้น ทำยังไง?","answer":"1. Teams > Settings > Notifications\n2. ตรวจ Windows Focus Assist ว่าปิดอยู่\n3. Settings > System > Notifications > Teams ให้เปิด\n4. Restart Teams\n5. ติดต่อ IT ext.1234"},
      {"question":"ตั้งค่า Status Teams ยังไง?","answer":"1. คลิกรูปโปรไฟล์มุมบนขวา\n2. เลือก Status: Available / Busy / Do not disturb / Away\n3. ตั้ง Status Message ได้ที่ 'Set status message'\n4. Duration Message หมดอายุอัตโนมัติได้"},
      {"question":"ส่งไฟล์ใน Teams ทำยังไง?","answer":"1. คลิก Attach (📎) ใน Chat\n2. เลือก Upload from computer หรือ OneDrive\n3. ขนาดสูงสุด 250MB ต่อไฟล์\n4. ลาก Drop ไฟล์เข้า Chat ได้เลย\n5. ไฟล์จะเก็บใน SharePoint อัตโนมัติ"},
      {"question":"Teams ไม่ยอม Login ทำยังไง?","answer":"1. Sign out แล้ว Sign in ใหม่\n2. ล้าง Cache: %AppData%\\Microsoft\\Teams\n3. ลอง Teams Web: teams.microsoft.com\n4. ตรวจ Password ว่าไม่หมดอายุ\n5. ติดต่อ IT ext.1234"},
    ]
  },
  {
    "name": "Hardware / อุปกรณ์",
    "keywords": ["usb","port","จอ","monitor","display","hdmi","vga","hub","dock","docking","keyboard","mouse","เมาส์","คีย์บอร์ด","webcam","กล้อง","headset","หูฟัง","speaker","ลำโพง","charger","adapter"],
    "faqs": [
      {"question":"เสียบ USB แล้วไม่ขึ้น ทำยังไง?","answer":"1. ลองเสียบช่อง USB อื่น\n2. Restart เครื่อง\n3. Device Manager > Action > Scan for hardware changes\n4. ลองเสียบเครื่องอื่นว่าใช้ได้ไหม\n5. ถ้าพอร์ต USB เสีย ติดต่อ IT ext.1234"},
      {"question":"จอแสดงสีผิดเพี้ยน / แสงกะพริบ","answer":"1. ตรวจสาย HDMI/DP ว่าเสียบแน่น\n2. ลองเปลี่ยนสาย\n3. อัปเดต Graphics Driver\n4. ลด Refresh Rate: Display Settings > Advanced\n5. ถ้าจอเสีย ติดต่อ IT ext.1234"},
      {"question":"ต่อ 2 จอ (Dual Monitor) ทำยังไง?","answer":"1. เสียบสายจอที่ 2 เข้า HDMI/DP/VGA\n2. คลิกขวา Desktop > Display Settings\n3. เลือก Extend these displays\n4. ลาก Position จอให้ถูกต้อง\n5. ถ้าไม่พบ ตรวจ Driver หรือติดต่อ IT ext.1234"},
      {"question":"Docking Station ใช้ไม่ได้ ทำยังไง?","answer":"1. ตรวจสาย Power Dock ว่าเสียบแน่น\n2. ถอด-เสียบ USB-C/Thunderbolt ใหม่\n3. Restart เครื่องขณะเสียบ Dock อยู่\n4. อัปเดต Dock Firmware\n5. ติดต่อ IT ext.1234"},
      {"question":"Webcam ภาพมืด / พร่ามัว ทำยังไง?","answer":"1. ตรวจแสงในห้องว่าเพียงพอ\n2. ล้างเลนส์ด้วยผ้านุ่ม\n3. เปิด Camera App ทดสอบ\n4. Update Webcam Driver\n5. ตรวจ Privacy Settings > Camera\n6. ติดต่อ IT ext.1234"},
    ]
  },
  {
    "name": "File / Folder / Network Drive",
    "keywords": ["folder","ไฟล์","file","share","shared drive","network drive","map drive","z:","เชื่อมไดร์ฟ","sharepoint","onedrive","permission","สิทธิ์ไฟล์","เข้าโฟลเดอร์ไม่ได้"],
    "faqs": [
      {"question":"Map Network Drive ทำยังไง?","answer":"1. เปิด File Explorer\n2. คลิก This PC > Map network drive\n3. เลือก Drive Letter (เช่น Z:)\n4. กรอก Path: \\\\server\\foldername\n5. ติ๊ก Reconnect at sign-in\n6. ถ้าไม่รู้ Path ติดต่อ IT ext.1234"},
      {"question":"เข้า Network Drive ไม่ได้ ทำยังไง?","answer":"1. ตรวจว่าต่อ VPN แล้ว (ถ้า WFH)\n2. Disconnect แล้ว Map ใหม่\n3. ตรวจ Username/Password\n4. Restart เครื่อง\n5. ติดต่อ IT ext.1234 เพื่อตรวจสิทธิ์"},
      {"question":"ไฟล์ใน SharePoint เปิดไม่ได้","answer":"1. ตรวจ Internet Connection\n2. Login ด้วยบัญชีบริษัทใหม่\n3. Clear Browser Cache\n4. ลอง Browser อื่น\n5. ดาวน์โหลดมาเปิดแทน\n6. ติดต่อ IT ext.1234"},
      {"question":"ไฟล์ถูกล็อค / เปิดพร้อมกันไม่ได้","answer":"1. ตรวจว่าคนอื่นเปิดไฟล์อยู่หรือเปล่า\n2. รอให้คนนั้นปิดก่อน\n3. ถ้าล็อคค้าง ติดต่อ IT ext.1234\n4. ใช้ OneDrive จะ Co-edit พร้อมกันได้\n5. ลองเปิดแบบ Read-Only ชั่วคราว"},
      {"question":"ขนาด Folder ดูยังไง?","answer":"1. Right-click Folder > Properties\n2. ดูที่ Size on disk\n3. ถ้าช้า ใช้ WinDirStat (ขอจาก IT)\n4. ถ้า Quota เต็ม ลบไฟล์เก่าหรือย้ายไป Archive\n5. ติดต่อ IT ext.1234 เพื่อขอเพิ่ม Space"},
    ]
  },
  {
    "name": "Office 365 / Microsoft 365",
    "keywords": ["office 365","microsoft 365","m365","word","excel","powerpoint","onenote","onedrive","sharepoint","activation","activate","ลงทะเบียน","license office"],
    "faqs": [
      {"question":"Office 365 ขึ้น Product Activation Failed ทำยังไง?","answer":"1. Sign out แล้ว Sign in ด้วยบัญชีบริษัท\n2. File > Account > Sign In\n3. ตรวจ Internet Connection\n4. Repair Office: Settings > Apps > Microsoft 365 > Modify\n5. ติดต่อ IT ext.1234 เพื่อ Renew License"},
      {"question":"Excel ไฟล์ใหญ่เปิดช้า ทำยังไง?","answer":"1. ปิด Auto-Calculate: Formulas > Calculation Options > Manual\n2. ลบ Conditional Formatting ที่ไม่ใช้\n3. ลด Pivot Cache\n4. แยกไฟล์เป็น Sheet ย่อย\n5. เพิ่ม RAM ติดต่อ IT ext.1234"},
      {"question":"Word ไม่ยอม Save ทำยังไง?","answer":"1. ลอง Save As ชื่อใหม่\n2. ตรวจ Disk Space ว่าเหลือพอ\n3. Save เป็น .docx ไม่ใช่ .doc\n4. ปิด OneDrive Sync ชั่วคราวแล้ว Save\n5. ติดต่อ IT ext.1234"},
      {"question":"PowerPoint เล่น Presentation แบบเต็มจอยังไง?","answer":"1. กด F5 เล่นตั้งแต่ Slide แรก\n2. กด Shift+F5 เล่นจาก Slide ปัจจุบัน\n3. ถ้าต่อโปรเจกเตอร์ กด Win+P เลือก Extend\n4. Presenter View: Slide Show > Use Presenter View\n5. กด Esc เพื่อออก"},
      {"question":"OneDrive Sync ไฟล์ขึ้น Error ทำยังไง?","answer":"1. คลิกขวา OneDrive Icon > View sync errors\n2. ตรวจชื่อไฟล์ว่ามีอักขระพิเศษ (: * ? < > | )\n3. ตรวจ Disk Space\n4. Pause แล้ว Resume Sync\n5. Unlink แล้ว Link บัญชีใหม่\n6. ติดต่อ IT ext.1234"},
    ]
  },
  {
    "name": "Windows / System",
    "keywords": ["windows","windows 10","windows 11","update","อัพเดท","driver","ไดร์เวอร์","activation windows","disk","storage","ดิสก์เต็ม","c drive","task manager","registry","startup","บูต","boot slow"],
    "faqs": [
      {"question":"Windows Update ค้าง ทำยังไง?","answer":"1. รอให้ครบ อย่าปิดเครื่อง\n2. ถ้าค้างนาน Restart แล้วลอง Update ใหม่\n3. Run Windows Update Troubleshooter\n4. ตรวจ Disk Space C: ต้องเหลือ > 10GB\n5. ติดต่อ IT ext.1234"},
      {"question":"C Drive เต็ม ทำยังไง?","answer":"1. Disk Cleanup: คลิกขวา C: > Properties > Disk Cleanup\n2. ลบไฟล์ Temp: Win+R พิมพ์ %temp%\n3. Uninstall Program ที่ไม่ใช้\n4. ย้ายไฟล์ใหญ่ไป D: หรือ OneDrive\n5. ติดต่อ IT ext.1234 เพื่อขยาย Disk"},
      {"question":"Windows Boot ช้ามาก ทำยังไง?","answer":"1. Task Manager > Startup > Disable โปรแกรมที่ไม่จำเป็น\n2. Settings > System > Power & Sleep > Shutdown Settings > Fast Startup ON\n3. ตรวจ SSD/HDD ว่า Health ดี\n4. Scan Malware\n5. ติดต่อ IT ext.1234"},
      {"question":"Windows ขึ้น 'Not Genuine' ทำยังไง?","answer":"1. ตรวจว่า Sign in ด้วย Microsoft Account บริษัทหรือยัง\n2. Settings > Update & Security > Activation\n3. ติดต่อ IT ext.1234 เพื่อใส่ Product Key\n4. อย่าซื้อ Key นอกหรือ Crack (ผิด Policy)"},
      {"question":"Task Manager เปิดไม่ได้ ทำยังไง?","answer":"1. กด Ctrl+Shift+Esc\n2. คลิกขวา Taskbar > Task Manager\n3. Win+R พิมพ์ taskmgr\n4. ถ้าเปิดไม่ได้อาจมี Malware\n5. ติดต่อ IT ext.1234 ทันที"},
    ]
  },
  {
    "name": "Line / Communication App",
    "keywords": ["line","ไลน์","line oa","แจ้งเตือน","sticker","สติ๊กเกอร์","line pc","facebook","messenger","whatsapp","slack"],
    "faqs": [
      {"question":"Line PC แจ้งเตือนไม่ขึ้น ทำยังไง?","answer":"1. Line > Settings > Notifications > เปิดทั้งหมด\n2. Windows Settings > Notifications > Line > เปิด\n3. ตรวจว่า Focus Assist ปิดอยู่\n4. Restart Line\n5. Update Line เป็น Version ล่าสุด"},
      {"question":"Line Login บนเครื่องใหม่ ทำยังไง?","answer":"1. Download Line PC จาก line.me\n2. เปิด Line บนมือถือ\n3. Setting > Devices > Scan QR Code\n4. ยืนยัน OTP\n5. ข้อความจะ Sync มา (แต่ไม่ย้อนหลัง)"},
    ]
  }
]

with open("knowledge_base.json", "r", encoding="utf-8") as f:
    kb = json.load(f)

existing_names = [c["name"] for c in kb["categories"]]
added = 0
for cat in new_categories:
    if cat["name"] not in existing_names:
        kb["categories"].append(cat)
        added += 1
        print(f"เพิ่มหมวด: {cat['name']} ({len(cat['faqs'])} FAQ)")
    else:
        # เพิ่ม FAQ เข้าหมวดที่มีอยู่แล้ว
        for c in kb["categories"]:
            if c["name"] == cat["name"]:
                existing_qs = [f["question"] for f in c["faqs"]]
                for faq in cat["faqs"]:
                    if faq["question"] not in existing_qs:
                        c["faqs"].append(faq)
                        added += 1
                        print(f"เพิ่ม FAQ: {faq['question'][:40]}...")

total = sum(len(c["faqs"]) for c in kb["categories"])
with open("knowledge_base.json", "w", encoding="utf-8") as f:
    json.dump(kb, f, ensure_ascii=False, indent=2)

print(f"\n✅ เสร็จ! เพิ่ม {added} รายการ | รวมทั้งหมด: {total} FAQ | {len(kb['categories'])} หมวด")
