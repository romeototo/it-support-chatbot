import json

with open("knowledge_base.json","r",encoding="utf-8") as f:
    kb = json.load(f)

js_kb = json.dumps(kb, ensure_ascii=False)

html = """<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IT Support AI — HelpDesk</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',sans-serif;background:#0f1117;color:#e2e8f0;height:100vh;display:flex;flex-direction:column;overflow:hidden}
header{background:#0d1117;border-bottom:1px solid #1e293b;padding:12px 20px;display:flex;align-items:center;gap:12px;z-index:100}
.logo{width:38px;height:38px;background:linear-gradient(135deg,#3b82f6,#8b5cf6);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0}
.hinfo{flex:1}.hinfo h1{font-size:1rem;font-weight:700}.hinfo p{font-size:.72rem;color:#64748b}
.hbadge{background:#1e40af22;border:1px solid #1e40af55;color:#60a5fa;padding:3px 10px;border-radius:20px;font-size:.7rem}
.dot{width:8px;height:8px;background:#22c55e;border-radius:50%;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.gemini-bar{background:#0d1117;border-bottom:1px solid #1e293b;padding:8px 20px;display:flex;gap:8px;align-items:center}
.gemini-bar label{font-size:.75rem;color:#64748b;white-space:nowrap}
.gemini-bar input{flex:1;background:#1e293b;border:1px solid #334155;color:#f1f5f9;padding:7px 12px;border-radius:8px;font-size:.78rem;outline:none;font-family:monospace}
.gemini-bar input:focus{border-color:#3b82f6}
.gemini-bar button{background:#1d4ed8;border:none;color:#fff;padding:7px 14px;border-radius:8px;cursor:pointer;font-size:.78rem;white-space:nowrap}
.main{display:flex;flex:1;overflow:hidden}
.sidebar{width:200px;background:#0d1117;border-right:1px solid #1e293b;padding:12px;display:flex;flex-direction:column;gap:6px;overflow-y:auto;flex-shrink:0}
.sidebar::-webkit-scrollbar{width:3px}.sidebar::-webkit-scrollbar-thumb{background:#334155;border-radius:3px}
.stitle{font-size:.65rem;color:#475569;font-weight:600;text-transform:uppercase;margin:4px 0 2px}
.qbtn{background:#1e293b;border:none;color:#94a3b8;padding:8px 10px;border-radius:8px;cursor:pointer;font-size:.78rem;text-align:left;display:flex;align-items:center;gap:6px;transition:.2s;width:100%}
.qbtn:hover{background:#1e40af;color:#fff}
.chat-wrap{flex:1;display:flex;flex-direction:column;min-width:0}
.messages{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px}
.messages::-webkit-scrollbar{width:4px}.messages::-webkit-scrollbar-thumb{background:#334155;border-radius:4px}
.msg{display:flex;gap:8px;max-width:85%}
.msg.user{align-self:flex-end;flex-direction:row-reverse}
.av{width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0}
.bot .av{background:linear-gradient(135deg,#3b82f6,#8b5cf6)}
.user .av{background:linear-gradient(135deg,#10b981,#3b82f6)}
.bub{padding:10px 14px;border-radius:12px;font-size:.85rem;line-height:1.6;white-space:pre-wrap}
.bot .bub{background:#1e293b;border:1px solid #334155;border-top-left-radius:3px}
.user .bub{background:linear-gradient(135deg,#1d4ed8,#7c3aed);border-top-right-radius:3px}
.msg-footer{display:flex;gap:6px;margin-top:4px;padding-left:38px}
.fb-btn{background:none;border:1px solid #334155;color:#64748b;padding:3px 10px;border-radius:20px;cursor:pointer;font-size:.72rem;transition:.2s}
.fb-btn:hover{background:#1e293b;color:#fff}
.fb-btn.active-good{background:#16a34a22;border-color:#16a34a;color:#4ade80}
.fb-btn.active-bad{background:#dc262622;border-color:#dc2626;color:#f87171}
.ticket-tag{font-size:.68rem;color:#475569}
.typing-dots span{display:inline-block;width:6px;height:6px;background:#64748b;border-radius:50%;margin:0 2px;animation:dot .8s infinite}
.typing-dots span:nth-child(2){animation-delay:.2s}
.typing-dots span:nth-child(3){animation-delay:.4s}
@keyframes dot{0%,80%,100%{transform:scale(1)}40%{transform:scale(1.4)}}
.input-area{background:#0d1117;border-top:1px solid #1e293b;padding:12px 16px;display:flex;gap:8px}
.input-area input{flex:1;background:#1e293b;border:1px solid #334155;color:#f1f5f9;padding:10px 14px;border-radius:10px;font-size:.88rem;outline:none;font-family:'Inter',sans-serif;transition:.2s}
.input-area input:focus{border-color:#3b82f6}
.input-area input::placeholder{color:#475569}
.send-btn{background:linear-gradient(135deg,#3b82f6,#7c3aed);border:none;color:#fff;padding:10px 18px;border-radius:10px;cursor:pointer;font-size:.88rem;font-weight:600;transition:.2s}
.send-btn:hover{transform:scale(1.04)}
.stats-bar{background:#0d1117;border-top:1px solid #1e293b;padding:8px 16px;display:flex;gap:16px;font-size:.72rem;color:#475569}
.stat{display:flex;align-items:center;gap:4px}.stat span{color:#60a5fa;font-weight:600}
.history-panel{width:260px;background:#0d1117;border-left:1px solid #1e293b;display:flex;flex-direction:column;flex-shrink:0}
.hp-title{padding:12px 14px;font-size:.78rem;font-weight:600;border-bottom:1px solid #1e293b;color:#94a3b8}
.hp-list{flex:1;overflow-y:auto;padding:8px}
.hp-item{background:#1e293b;border-radius:8px;padding:8px 10px;margin-bottom:6px;cursor:pointer;transition:.2s}
.hp-item:hover{background:#1e3a5f}
.hp-item .hn{font-size:.72rem;color:#94a3b8;margin-bottom:3px}
.hp-item .hq{font-size:.78rem;color:#e2e8f0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hp-item .hr{font-size:.68rem;color:#475569;margin-top:3px}
.gemini-badge{background:#7c3aed22;border:1px solid #7c3aed55;color:#a78bfa;padding:2px 8px;border-radius:20px;font-size:.65rem;margin-left:auto}
@media(max-width:768px){
  .sidebar{display:none}
  .history-panel{display:none}
  .gemini-bar label{display:none}
}
</style>
</head>
<body>
<header>
  <div class="logo">🖥️</div>
  <div class="hinfo"><h1>IT Support AI</h1><p>ระบบช่วยเหลือไอทีอัจฉริยะ</p></div>
  <span class="hbadge" id="faqCount">86 FAQ | 17 หมวด</span>
  <div class="gemini-badge" id="aiLabel">Keyword AI</div>
  <div class="dot"></div>
</header>
<div class="gemini-bar">
  <label>🤖 Gemini API Key:</label>
  <input type="password" id="geminiKey" placeholder="AIza... (ใส่เพื่อใช้ AI จริง)">
  <button onclick="saveKey()">เปิดใช้ AI</button>
</div>
<div class="main">
  <div class="sidebar">
    <div class="stitle">หัวข้อด่วน</div>
    <button class="qbtn" onclick="ask('เครื่องพิมพ์พิมพ์ไม่ออก')">🖨️ เครื่องพิมพ์</button>
    <button class="qbtn" onclick="ask('เชื่อมต่อ WiFi ไม่ได้')">📶 WiFi/เน็ต</button>
    <button class="qbtn" onclick="ask('ลืมรหัสผ่าน')">🔑 ลืมรหัสผ่าน</button>
    <button class="qbtn" onclick="ask('คอมช้ามาก')">💻 คอมช้า</button>
    <button class="qbtn" onclick="ask('ส่งอีเมลไม่ได้')">📧 อีเมล</button>
    <button class="qbtn" onclick="ask('VPN เชื่อมต่อไม่ได้')">🔐 VPN</button>
    <button class="qbtn" onclick="ask('Zoom กล้องไม่ทำงาน')">📹 Video Call</button>
    <button class="qbtn" onclick="ask('ไฟล์ถูกลบกู้คืนยังไง')">💾 กู้ไฟล์</button>
    <button class="qbtn" onclick="ask('Teams เปิดไม่ขึ้น')">💬 Teams</button>
    <button class="qbtn" onclick="ask('เสียบ USB แล้วไม่ขึ้น')">🔌 USB/Hardware</button>
    <button class="qbtn" onclick="ask('Map Network Drive ทำยังไง')">🗂️ Network Drive</button>
    <button class="qbtn" onclick="ask('Office 365 activation failed')">📊 Office 365</button>
    <button class="qbtn" onclick="ask('C Drive เต็ม')">🪟 Windows</button>
    <button class="qbtn" onclick="ask('ต่อ 2 จอ Dual Monitor')">🖥️ Dual Monitor</button>
    <button class="qbtn" onclick="ask('พนักงานใหม่ต้องทำอะไร')">👤 New Employee</button>
    <button class="qbtn" onclick="ask('ติดตั้งโปรแกรมใหม่')">📦 ลงโปรแกรม</button>
  </div>
  <div class="chat-wrap">
    <div class="messages" id="messages">
      <div class="msg bot"><div class="av">🤖</div><div class="bub">สวัสดีครับ! 👋 ผม <strong>IT Support AI</strong> พร้อมช่วยแก้ปัญหาไอทีให้คุณ\\n\\n💡 พิมพ์ปัญหา หรือกดปุ่มด้านซ้ายได้เลยครับ\\n🤖 ใส่ Gemini API Key ด้านบนเพื่อให้ AI ตอบอัจฉริยะยิ่งขึ้น</div></div>
    </div>
    <div class="input-area">
      <input id="inp" placeholder="พิมพ์ปัญหา IT เช่น WiFi เชื่อมไม่ได้, ลืมรหัสผ่าน..." onkeydown="if(event.key==='Enter')send()">
      <button class="send-btn" onclick="send()">ส่ง ➤</button>
    </div>
    <div class="stats-bar">
      <div class="stat">🎫 Tickets: <span id="sTicket">0</span></div>
      <div class="stat">👍 Helpful: <span id="sGood">0</span></div>
      <div class="stat">👎 Not helpful: <span id="sBad">0</span></div>
      <div class="stat" style="margin-left:auto">⚡ <span id="sMode">Keyword Mode</span></div>
    </div>
  </div>
  <div class="history-panel">
    <div class="hp-title">📋 Ticket History</div>
    <div class="hp-list" id="histList"><div style="padding:20px;text-align:center;color:#475569;font-size:.78rem">ยังไม่มี Ticket</div></div>
  </div>
</div>
<script>
const KB = """ + js_kb + """;

let geminiKey = localStorage.getItem('geminiKey') || '';
let ticketNum = 1000 + Math.floor(Math.random()*1000);
let stats = {tickets:0, good:0, bad:0};
let history = [];

if(geminiKey){ document.getElementById('geminiKey').value=geminiKey; setAIMode(true); }

function saveKey(){
  geminiKey = document.getElementById('geminiKey').value.trim();
  if(geminiKey){ localStorage.setItem('geminiKey',geminiKey); setAIMode(true); addSys('✅ เปิดใช้ Gemini AI แล้วครับ! ตอนนี้จะตอบด้วย AI จริง'); }
  else{ localStorage.removeItem('geminiKey'); setAIMode(false); addSys('ℹ️ ปิด Gemini AI แล้ว กลับเป็น Keyword Mode'); }
}
function setAIMode(on){
  document.getElementById('aiLabel').textContent = on ? 'Gemini AI' : 'Keyword AI';
  document.getElementById('aiLabel').style.background = on ? '#7c3aed22' : '#1e40af22';
  document.getElementById('aiLabel').style.borderColor = on ? '#7c3aed55' : '#1e40af55';
  document.getElementById('aiLabel').style.color = on ? '#a78bfa' : '#60a5fa';
  document.getElementById('sMode').textContent = on ? 'Gemini AI Mode' : 'Keyword Mode';
}

function scoreKB(input){
  const u=input.toLowerCase(); let best=null,top=0;
  for(const cat of KB.categories){
    for(const faq of cat.faqs){
      let s=0;
      for(const kw of cat.keywords) if(u.includes(kw.toLowerCase())) s+=3;
      for(const w of u.split(' ')) if(faq.question.toLowerCase().includes(w)&&w.length>1) s+=1;
      if(s>top){top=s;best={faq,cat:cat.name};}
    }
  }
  return top>=1?best:null;
}

async function callGemini(userInput){
  const top3=[]; const u=userInput.toLowerCase();
  for(const cat of KB.categories){
    for(const faq of cat.faqs){
      let s=0;
      for(const kw of cat.keywords) if(u.includes(kw.toLowerCase())) s+=3;
      if(s>0) top3.push(faq);
      if(top3.length>=3) break;
    }
    if(top3.length>=3) break;
  }
  const ctx = top3.map(f=>`Q: ${f.question}\\nA: ${f.answer}`).join('\\n\\n');
  const prompt = `คุณเป็น IT Support AI ขององค์กร ตอบคำถามสั้น ชัดเจน เป็นภาษาไทย ใช้ขั้นตอนแบบ numbered list\\nถ้าไม่มีข้อมูล ให้แจ้ง: ติดต่อ IT Support ext.1234\\n\\nFAQ Reference:\\n${ctx}\\n\\nคำถาม: ${userInput}\\n\\nตอบ:`;
  const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${geminiKey}`,{
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({contents:[{parts:[{text:prompt}]}]})
  });
  if(!res.ok) throw new Error('API Error '+res.status);
  const d = await res.json();
  return d.candidates[0].content.parts[0].text;
}

function addSys(text){
  const w=document.getElementById('messages');
  const d=document.createElement('div');
  d.style.cssText='text-align:center;font-size:.72rem;color:#475569;padding:4px';
  d.textContent=text; w.appendChild(d); w.scrollTop=w.scrollHeight;
}
function addMsg(text,role){
  const w=document.getElementById('messages');
  const d=document.createElement('div');
  d.className='msg '+role;
  d.innerHTML=`<div class="av">${role==='bot'?'🤖':'👤'}</div><div class="bub">${text.replace(/</g,'&lt;').replace(/\\n/g,'<br>')}</div>`;
  w.appendChild(d); w.scrollTop=w.scrollHeight; return d;
}
function addFeedback(tNum){
  const w=document.getElementById('messages');
  const d=document.createElement('div');
  d.className='msg-footer';
  d.innerHTML=`<button class="fb-btn" id="g${tNum}" onclick="feedback('${tNum}',1)">👍 มีประโยชน์</button><button class="fb-btn" id="b${tNum}" onclick="feedback('${tNum}',-1)">👎 ไม่ตรง</button><span class="ticket-tag">#${tNum}</span>`;
  w.appendChild(d); w.scrollTop=w.scrollHeight;
}
function feedback(tNum,val){
  const g=document.getElementById('g'+tNum), b=document.getElementById('b'+tNum);
  if(!g||!b) return;
  g.className='fb-btn'+(val===1?' active-good':'');
  b.className='fb-btn'+(val===-1?' active-bad':'');
  if(val===1){stats.good++;document.getElementById('sGood').textContent=stats.good;}
  else{stats.bad++;document.getElementById('sBad').textContent=stats.bad;}
  const h=history.find(x=>x.ticket==tNum);
  if(h) h.feedback=val>0?'👍':'👎';
  renderHistory();
}
function addTyping(){
  const w=document.getElementById('messages');
  const d=document.createElement('div');
  d.className='msg bot'; d.id='typing';
  d.innerHTML='<div class="av">🤖</div><div class="bub"><div class="typing-dots"><span></span><span></span><span></span></div></div>';
  w.appendChild(d); w.scrollTop=w.scrollHeight;
}
function renderHistory(){
  const el=document.getElementById('histList');
  if(!history.length){el.innerHTML='<div style="padding:20px;text-align:center;color:#475569;font-size:.78rem">ยังไม่มี Ticket</div>';return;}
  el.innerHTML=[...history].reverse().map(h=>`<div class="hp-item"><div class="hn">#${h.ticket} • ${h.time} ${h.feedback||''}</div><div class="hq">${h.question}</div><div class="hr">${h.mode}</div></div>`).join('');
}
function ask(q){document.getElementById('inp').value=q;send();}
async function send(){
  const inp=document.getElementById('inp');
  const text=inp.value.trim(); if(!text) return;
  inp.value=''; addMsg(text,'user');
  const tNum=++ticketNum; stats.tickets++;
  document.getElementById('sTicket').textContent=stats.tickets;
  addTyping();
  const now=new Date().toLocaleTimeString('th-TH',{hour:'2-digit',minute:'2-digit'});
  let reply='', mode='Keyword';
  try{
    if(geminiKey){
      mode='Gemini AI';
      reply=await callGemini(text);
    } else {
      await new Promise(r=>setTimeout(r,700+Math.random()*500));
      const m=scoreKB(text);
      reply=m?`📋 **${m.faq.question}**\\n\\n${m.faq.answer}`:KB.escalation.message;
    }
  } catch(e){
    reply='⚠️ Gemini API Error: '+e.message+'\\n\\nใช้ Keyword Mode แทน:\\n'+(scoreKB(text)?.faq.answer||KB.escalation.message);
    mode='Fallback';
  }
  document.getElementById('typing')?.remove();
  addMsg(reply,'bot');
  addFeedback(tNum);
  history.push({ticket:tNum,question:text,time:now,mode,feedback:''});
  renderHistory();
}
document.getElementById('inp').addEventListener('keydown',e=>{if(e.key==='Enter')send();});
</script>
</body>
</html>"""

with open("index.html","w",encoding="utf-8") as f:
    f.write(html)

print(f"Done! {len(html)} chars")
