import {readFileSync, writeFileSync} from 'node:fs';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read=name=>readFileSync(path.join(root,name),'utf8');
const write=(name,value)=>writeFileSync(path.join(root,name),value);
const script=read('script.js');
const context=vm.createContext({window:{}});
vm.runInContext(read('catalog.js'),context);
// Evaluate only the shared content definitions; browser event handlers stay in the browser.
const helpers=script.slice(script.indexOf('const escapeHTML'),script.indexOf('let toastTimer;'));
const definitions=script.slice(script.indexOf('const docs ='),script.indexOf("if ($('#doc-article'))"));
vm.runInContext(`${helpers}\n${definitions}\nglobalThis.content={docs,skills:window.PHAT_SKILLS};`,context);
const {docs,skills}=context.content;
const escape=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const domain='https://phatysd.me';
const source='https://github.com/phatysddev/skills';
function block(html,key,body){
  const start=`<!-- ${key}:start -->`,end=`<!-- ${key}:end -->`;
  const expression=new RegExp(`${start}[\\s\\S]*?${end}`);
  if(!expression.test(html)) throw new Error(`Missing marker ${key}`);
  return html.replace(expression,()=>`${start}\n${body}\n${end}`);
}
function meta(title,description,url,type='WebPage',extra=[]){
  const graph=[{'@type':'Person','@id':`${domain}/#creator`,name:'PhatYSD'},
    {'@type':'WebSite','@id':`${domain}/#website`,url:domain+'/',name:'Phat Skills',inLanguage:['th','en'],creator:{'@id':`${domain}/#creator`}},
    {'@type':type,'@id':url+'#page',url,name:title,description,inLanguage:['th','en'],isPartOf:{'@id':`${domain}/#website`},about:{'@id':`${domain}/#software`}},
    {'@type':'SoftwareSourceCode','@id':`${domain}/#software`,name:'Phat Skills',description:'23 open-source skills for AI coding agents: product decisions, context, specifications, implementation, verification, and review.',codeRepository:source,url:domain+'/',license:source+'/blob/main/LICENSE',author:{'@id':`${domain}/#creator`}},...extra];
  const image=domain+'/assets/brand/phatysd-icon.png';
  return `<title>${escape(title)}</title>\n<meta name="description" content="${escape(description)}">\n<link rel="canonical" href="${url}">\n<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">\n<meta name="author" content="PhatYSD">\n<meta property="og:type" content="website">\n<meta property="og:site_name" content="Phat Skills">\n<meta property="og:title" content="${escape(title)}">\n<meta property="og:description" content="${escape(description)}">\n<meta property="og:url" content="${url}">\n<meta property="og:locale" content="th_TH">\n<meta property="og:locale:alternate" content="en_US">\n<meta property="og:image" content="${image}">\n<meta property="og:image:alt" content="PhatYSD logo">\n<meta name="twitter:card" content="summary">\n<meta name="twitter:title" content="${escape(title)}">\n<meta name="twitter:description" content="${escape(description)}">\n<meta name="twitter:image" content="${image}">\n<script type="application/ld+json">${JSON.stringify({'@context':'https://schema.org','@graph':graph}).replace(/</g,'\\u003c')}</script>`;
}
let home=read('index.html');
home=block(home,'seo-head',meta('Phat Skills — 23 Agent Skills สำหรับ AI Coding Agents','Phat Skills ชุด 23 skills แบบโอเพนซอร์สสำหรับ Codex และ coding agents: ตัดสินใจ วางสเปก พัฒนา ทดสอบ และรีวิว พร้อมคู่มือติดตั้งและตัวอย่างใช้งาน',domain+'/'));
home=block(home,'static-skills',skills.map((s,i)=>`<a class="skill-row" href="docs.html#skill-${s.name}"><span class="skill-index">${String(i+1).padStart(2,'0')}</span><div><h3>${s.name}</h3><span class="skill-category">${escape(s.category)}</span></div><p>${escape(s.description)}</p><span class="row-arrow" aria-hidden="true">↗</span></a>`).join('\n'));
const sequence=['ask-workflow','grill-workflow','setup-project','write-spec','to-tasks'];
home=block(home,'static-workflow',sequence.map((name,i)=>`<div class="workflow-step"><span class="step-num">0${i+1}<span>→</span></span><div><h3><a href="docs.html#skill-${name}">${name}</a></h3><p>${escape(skills.find(s=>s.name===name).title)}</p></div></div>`).join('\n'));
write('index.html',home);
let doc=read('docs.html');
doc=block(doc,'seo-head',meta('เอกสาร Phat Skills — ติดตั้งและใช้งาน Agent Skills','คู่มือ Phat Skills สำหรับ coding agents: การติดตั้ง 23 skills เลือก workflow จัดทำ context และ spec พร้อมนโยบายทดสอบและ code review',domain+'/docs.html'));
doc=block(doc,'static-introduction',`<h1 tabindex="-1">${docs.introduction.title}</h1>${docs.introduction.body()}<p><a href="guide.html">อ่านคู่มือฉบับเต็ม: ติดตั้ง เวิร์กโฟลว์ และคำถามที่พบบ่อย →</a></p>`);
write('docs.html',doc);
const labels={installation:'วิธีติดตั้ง Phat Skills',workflow:'เลือกเวิร์กโฟลว์ให้ตรงกับโปรเจกต์',verification:'การทดสอบและรีวิว',security:'ใช้ agent-security ร่วมกับ workflow',faq:'คำถามที่พบบ่อยเกี่ยวกับ Phat Skills'};
const answers=[...docs.faq.body().matchAll(/<details[^>]*><summary>(.*?)<\/summary><p>(.*?)<\/p><\/details>/gs)].map(m=>({'@type':'Question',name:m[1],acceptedAnswer:{'@type':'Answer',text:m[2]}}));
const guideSchema=[{'@type':'FAQPage','@id':domain+'/guide.html#faq',mainEntity:answers}];
const sections=Object.entries(labels).map(([key,label])=>{
  let body=docs[key].body().replace(/<a class="doc-next"[\s\S]*?<\/a>/g,'');
  body=body.replace(/id="([^"]+)"/g,(_,id)=>`id="${key}-${id}"`).replace(/href="#([^"]+)"/g,(_,id)=>`href="docs.html#${id}"`).replace(/<h3/g,'<h4').replace(/<\/h3>/g,'</h4>').replace(/<h2/g,'<h3').replace(/<\/h2>/g,'</h3>');
  return `<section id="${key}"><h2>${label}</h2>${body}</section>`;
}).join('\n');
const catalog=`<section id="skills"><h2>รายการ Agent Skills ทั้ง ${skills.length} ตัว</h2>${skills.map(s=>`<section id="skill-${s.name}"><h3>${s.name}</h3><p>${escape(s.description)}</p><p><strong>ใช้เมื่อ:</strong> ${escape(s.when)}</p><p><a href="docs.html#skill-${s.name}">ตัวอย่างและวิธีใช้ ${s.name}</a> · <a href="${source}/blob/main/.agents/skills/${s.name}/SKILL.md">อ่าน SKILL.md ต้นฉบับ</a></p></section>`).join('\n')}</section>`;
const header=home.match(/<header[\s\S]*?<\/header>/)[0];
const footer=home.match(/<footer[\s\S]*?<\/footer>/)[0];
write('guide.html',`<!doctype html>\n<html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#f7f8f2">${meta('คู่มือ Phat Skills — ติดตั้ง Workflow และคำถามที่พบบ่อย','Phat Skills คืออะไร ติดตั้งอย่างไร เริ่ม skill ไหน และตรวจงานอย่างไร อ่านคู่มือ 23 Agent Skills พร้อมคำตอบ ตัวอย่าง และลิงก์ต้นฉบับ',domain+'/guide.html','WebPage',guideSchema)}<link rel="icon" href="assets/brand/phatysd-icon.png"><script src="preferences.js"></script><link rel="stylesheet" href="styles.css">${['catalog.js','translations.js','i18n.js','controls.js','script.js'].map(name=>`<script src="${name}" defer></script>`).join('')}</head><body class="docs-page"><a class="skip-link" href="#main">ข้ามไปเนื้อหา</a>${header}<div class="docs-layout wrap"><aside class="docs-sidebar"><p class="eyebrow">คู่มือฉบับเต็ม</p><nav aria-label="หัวข้อคู่มือ"><a href="#about">Phat Skills คืออะไร?</a>${Object.entries(labels).map(([id,label])=>`<a href="#${id}">${label}</a>`).join('')}<a href="#skills">รายการ 23 Skills</a><a href="docs.html">เอกสารแบบ Interactive →</a></nav></aside><main id="main" class="docs-content"><article><h1>คู่มือ Phat Skills สำหรับ AI Coding Agents</h1><section id="about"><h2>Phat Skills คืออะไร?</h2><p class="doc-lead">Phat Skills คือชุด ${skills.length} Agent Skills แบบโอเพนซอร์สสำหรับ Codex และ coding agents ที่รองรับ Agent Skills format ช่วยเชื่อมการตัดสินใจเรื่องโปรดักต์ การเก็บ context การเขียน spec การพัฒนา การทดสอบ และ code review</p><p>เริ่มด้วย <code>$ask-workflow</code> เพื่อเลือกขั้นตอนถัดไปจากสถานะโปรเจกต์จริง แต่ละ skill เก็บคำแนะนำในไฟล์ <code>SKILL.md</code> และเผยแพร่ภายใต้ <a href="${source}/blob/main/LICENSE">MIT License</a></p><p>ผู้จัดทำ: PhatYSD · <a href="${source}">Source repository</a> · ข้อกำหนดการทำงานให้ยึด <a href="${source}/blob/main/docs/workflow.md">workflow contract</a> และ SKILL.md ต้นฉบับ</p></section>${sections}${catalog}</article></main></div>${footer}<div class="toast" role="status" aria-live="polite"></div></body></html>\n`);
write('robots.txt',`User-agent: *\nAllow: /\n\nSitemap: ${domain}/sitemap.xml\n`);
write('sitemap.xml',`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${['/','/docs.html','/guide.html'].map(url=>`  <url><loc>${domain}${url}</loc></url>`).join('\n')}\n</urlset>\n`);
write('404.html',`<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>ไม่พบหน้า — Phat Skills</title><link rel="stylesheet" href="/styles.css"></head><body><main class="section wrap"><h1>ไม่พบหน้านี้</h1><p>ลิงก์อาจเปลี่ยนไป เลือกอ่านเอกสารหรือกลับไปหน้าแรก</p><a href="/">หน้าแรก Phat Skills</a> · <a href="/guide.html">คู่มือฉบับเต็ม</a></main></body></html>\n`);
console.log(`Built crawlable homepage, introduction, full guide, metadata, robots, sitemap and 404 (${skills.length} skills, ${answers.length} answers).`);
