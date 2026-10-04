'use strict';
const {translate: t, localize, searchText} = window.PHAT_I18N;
const skills = window.PHAT_SKILLS || [];
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const escapeHTML = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const source = 'https://github.com/phatysddev/skills';
const baseCommand = `npx skills@latest add ${source}`;
const code = (text, label = 'TERMINAL') => `<div class="code-block"><div class="code-label">${escapeHTML(label)}</div><button data-copy="${escapeHTML(text)}" aria-label="คัดลอก ${escapeHTML(label)}">Copy</button><pre><code>${escapeHTML(text)}</code></pre></div>`;
const section = (id, title, content) => `<h2 id="${id}">${title}</h2>${content}`;
const next = (hash, title) => `<a class="doc-next" href="#${hash}"><div><small>Continue reading</small>${title}</div><span>→</span></a>`;
let toastTimer;
function toast(message) { const el = $('.toast'); el.textContent = t(message); el.classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => el.classList.remove('show'), 2800); }
document.addEventListener('click', async event => {
  const button = event.target.closest('[data-copy]');
  if (!button) return;
  const text = button.dataset.copy;
  try {
    if (navigator.clipboard && window.isSecureContext) await navigator.clipboard.writeText(text);
    else {
      const area = document.createElement('textarea'); area.value = text; area.style.cssText = 'position:fixed;opacity:0'; document.body.append(area); area.select();
      const copied = document.execCommand('copy'); area.remove(); button.focus(); if (!copied) throw new Error('Copy unavailable');
    }
    const old = button.textContent; button.textContent = t('Copied ✓'); toast('คัดลอกแล้ว — พร้อมนำไปใช้งาน'); setTimeout(() => {button.textContent = t(old);}, 1800);
  } catch { toast('คัดลอกอัตโนมัติไม่ได้ กรุณาเลือกและคัดลอกข้อความคำสั่ง'); }
});
const menu = $('.menu-button');
function closeMenu() { $('#navigation').classList.remove('open'); menu.setAttribute('aria-expanded', 'false'); menu.setAttribute('aria-label', t('เปิดเมนู')); }
menu.addEventListener('click', () => { const open = menu.getAttribute('aria-expanded') !== 'true'; $('#navigation').classList.toggle('open', open); menu.setAttribute('aria-expanded', String(open)); menu.setAttribute('aria-label', t(open ? 'ปิดเมนู' : 'เปิดเมนู')); });
$$('#navigation a').forEach(a => a.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); if (event.key === '/' && !/INPUT|TEXTAREA|SELECT/.test(event.target.tagName) && !event.target.isContentEditable) { const input = $('#skill-search') || $('#docs-search'); if (input) {event.preventDefault(); input.focus();} } });

const paths = {
  new: {steps:['ask-workflow','grill-workflow','setup-project','write-spec','to-tasks'], note:'จากนั้น implement-task → verification ที่เกี่ยวข้อง → code-review · เลือก grill-design เพิ่มได้เมื่อต้องการกำหนด UI direction'},
  existing: {steps:['ask-workflow','code-to-context','setup-project','write-spec','to-tasks'], note:'เมื่อ repo มีโค้ดอยู่แล้ว ให้สร้างหรือปรับ generated context ก่อน setup แล้วจึงพัฒนาตาม task และ review'},
  prototype: {steps:['setup-project','to-prototype','edit-prototype','spec-with-prototype','to-tasks'], note:'ใช้เมื่อเห็นหน้าจอแล้วจะตัดสินใจได้ดีขึ้น · ปรับ prototype ได้หลายรอบ และ reconcile กับ spec ก่อนเริ่ม tasks'}
};
if ($('#workflow-steps')) {
  const renderPath = key => { const path = paths[key]; $('#workflow-steps').innerHTML = path.steps.map((name, i) => { const skill = skills.find(s => s.name === name); return `<div class="workflow-step"><span class="step-num">0${i+1}<span>→</span></span><div><h3><a href="docs.html#skill-${name}">${name}</a></h3><p>${skill.title}</p></div></div>`; }).join(''); $('#path-note').textContent = path.note; localize($('#workflow'));  };
  renderPath('new');
  $$('[data-path]').forEach(button => button.addEventListener('click', () => { $$('[data-path]').forEach(b => {b.classList.toggle('active', b === button); b.setAttribute('aria-pressed', String(b === button));}); renderPath(button.dataset.path); }));
}
if ($('#skill-list')) {
  let filter = 'All';
  const renderSkills = () => { const query = $('#skill-search').value.trim().toLowerCase(); const results = skills.filter(s => (filter === 'All' || s.category === filter) && `${s.name} ${searchText(s.title)} ${searchText(s.description)} ${searchText(s.category)}`.toLowerCase().includes(query));
    $('#result-count').textContent = `พบ ${results.length} skills`;
    $('#skill-list').innerHTML = results.length ? results.map(s => `<a class="skill-row" href="docs.html#skill-${s.name}"><span class="skill-index">${String(skills.indexOf(s)+1).padStart(2,'0')}</span><div><h3>${s.name}</h3><span class="skill-category">${s.category}</span></div><p>${s.description}</p><span class="row-arrow" aria-hidden="true">↗</span></a>`).join('') : '<p class="empty-state">ไม่พบ skill ที่ตรงกับคำค้น ลองเปลี่ยนคำค้นหรือเลือกหมวด All</p>';
    localize($('#skills'));
  };
  $$('[data-filter]').forEach(button => button.addEventListener('click', () => { filter = button.dataset.filter; $$('[data-filter]').forEach(b => {b.classList.toggle('active', b === button); b.setAttribute('aria-pressed', String(b === button));}); renderSkills(); }));
  $('#skill-search').addEventListener('input', renderSkills); renderSkills();
}
const docs = {
  introduction: {title:'A little structure. A lot more clarity.', label:'Introduction', body: () => `<p class="doc-lead">Phat Skills คือชุด 19 skills สำหรับ coding agents ที่เชื่อมการตัดสินใจเรื่องโปรดักต์เข้ากับการเขียนโค้ดและหลักฐานการตรวจสอบ</p><div class="doc-callout"><p>เริ่มตรงนี้ได้เลย: ติดตั้ง skill pack แล้วเรียก <code>$ask-workflow</code> เพื่อให้ agent แนะนำขั้นตอนถัดไปจากสถานะจริงของโปรเจกต์</p></div>${section('what-is-a-skill','What is a skill?','<p>Skill คือชุดคำแนะนำที่นำกลับมาใช้ซ้ำได้ เก็บในไฟล์ <code>SKILL.md</code> แต่ละตัวมีหน้าที่ชัดเจน ตั้งแต่ตั้งคำถามก่อนพัฒนา ไปจนถึง review งานที่ทำเสร็จ เหมาะกับ Codex และ agents ที่รองรับ Agent Skills format</p>')}${section('why-phat','One connected workflow','<p>การตัดสินใจไม่ควรหายไปเมื่อจบบทสนทนา Phat ใช้เอกสารใน repository เป็นจุดเชื่อมระหว่างแต่ละขั้นตอน เพื่อให้ agent อ่านขอบเขตและเหตุผลเดิมก่อนทำงานต่อ</p><ul><li><strong>Decide before spec.</strong> คลี่คลายข้อสงสัยเรื่องโปรดักต์ก่อนลงรายละเอียด</li><li><strong>Spec before tasks.</strong> นิยามพฤติกรรมก่อนแยกงาน</li><li><strong>Tasks before code.</strong> ทำงานในขอบเขตที่ตกลงไว้</li><li><strong>Evidence before done.</strong> ตรวจและ review ก่อนสรุปว่างานเสร็จ</li></ul>')}${section('source-of-truth','Your repository is the memory', '<table><thead><tr><th>Document</th><th>Responsibility</th></tr></thead><tbody><tr><td><code>docs/requirement.md</code></td><td>เป้าหมายและขอบเขตโปรดักต์</td></tr><tr><td><code>CONTEXT.md</code></td><td>บริบท repository และ domain</td></tr><tr><td><code>AGENTS.md</code></td><td>กติกาและทางเดินของ agent</td></tr><tr><td><code>docs/specs/</code></td><td>Behavioral contracts</td></tr><tr><td><code>docs/tasks/</code></td><td>Implementation scope และสถานะ</td></tr></tbody></table>')}${next('installation','Install your first skill')}`},
  installation: {title:'Up and running.',label:'Installation',body:() => `<p class="doc-lead">ติดตั้งจาก canonical GitHub repository ผ่าน skills CLI โดยตัวอย่างนี้ใช้ Codex เป็น agent เป้าหมาย</p>${section('before-you-start','Before you start','<p>ต้องมี Node.js และ npm ที่เรียก <code>npx</code> ได้ พร้อม internet สำหรับดาวน์โหลด package และ repository เปิด terminal ในโปรเจกต์ที่ต้องการใช้งาน</p>')}${section('discover','01 / Discover the pack', '<p>ดูรายการ skills ก่อนติดตั้ง คำสั่งนี้แสดง catalog โดยไม่ติดตั้ง skills</p>'+code(baseCommand+' --list'))}${section('install','02 / Choose your installation', '<h3>Start with one skill</h3><p>ติดตั้ง router เพื่อแนะนำขั้นตอนถัดไป เมื่อใช้ subset ให้ติดตั้ง workflow และ utility ที่งานนั้นต้องใช้เพิ่มด้วย</p>'+code(baseCommand+' --skill ask-workflow --agent codex --yes')+'<h3>Install the complete pack</h3><p>ติดตั้งทั้ง 19 skills สำหรับโปรเจกต์ปัจจุบัน ครอบคลุม workflow, utilities, prototype และ verification</p>'+code(baseCommand+" --skill '*' --agent codex --yes")+'<h3>Use it across projects</h3><p>เพิ่ม <code>--global</code> เมื่อต้องการติดตั้งระดับผู้ใช้แทนโปรเจกต์ปัจจุบัน</p>'+code(baseCommand+' --skill ask-workflow --agent codex --global --yes'))}${section('first-prompt','03 / Start a conversation','<p>เปิด coding agent ในโปรเจกต์ที่ติดตั้ง แล้วเริ่มด้วย prompt นี้ ตัวอย่างใช้รูปแบบเรียก skill ของ Codex</p>'+code('$ask-workflow\nอ่านสถานะโปรเจกต์นี้ แล้วแนะนำขั้นตอนถัดไปพร้อมเหตุผล','AGENT PROMPT')+'<p>ถ้า agent ไม่เห็น skill ให้ตรวจ agent เป้าหมายและ scope การติดตั้ง จากนั้นเปิด session ใหม่ หากใช้ agent อื่น ให้ใช้รูปแบบ invocation ที่ agent นั้นรองรับ</p>')}${section('installation-notes','Installation notes','<p><code>--yes</code> ข้ามคำถามยืนยันของ installer ส่วนคำสั่งไม่มี flags จะให้เลือก skill และ agent ระหว่างติดตั้ง การติดตั้ง skill ไม่ได้ติดตั้ง test runner หรือ dependency ของโปรเจกต์ให้เอง</p><p>อ้างอิง: <a href="https://github.com/vercel-labs/skills#readme">skills CLI documentation ↗</a> และ <a href="https://github.com/phatysddev/skills/blob/main/README.md">Phat Skills README ↗</a></p>')}${next('workflow','Choose your workflow')}`},
  workflow: {title:'Follow the work, not a checklist.',label:'Workflow guide',body:() => `<p class="doc-lead">เลือกเส้นทางตามสถานะของโปรเจกต์ ไม่จำเป็นต้องเรียกทุก skill ทุกครั้ง</p>${section('new-project','A new project',code('ask-workflow → grill-workflow\n  → grill-design (optional)\n  → setup-project → write-spec → to-tasks\n  → implement-task → selected verification → code-review','DEFAULT PATH')+'<p><code>grill-workflow</code> ช่วยคลี่คลายการตัดสินใจ ส่วน <code>setup-project</code> บันทึกบริบทถาวร เมื่อ spec พร้อมแล้วจึงแยก tasks และเริ่ม implementation</p>')}${section('existing-project','An existing codebase',code('ask-workflow → code-to-context\n  → setup-project → write-spec → to-tasks','BROWNFIELD PATH')+'<p>ถ้ามีโค้ดอยู่แล้ว แต่ generated context หายไปหรือล้าสมัย ให้ <code>code-to-context</code> อ่าน repo ก่อน โดยแก้เฉพาะ generated Codebase Context และรักษาบริบทที่มนุษย์เขียนไว้</p>')}${section('prototype-path','When seeing the UI helps',code('setup-project → to-prototype\n  → edit-prototype (repeat as needed)\n  → spec-with-prototype → to-tasks','OPTIONAL PROTOTYPE PATH')+'<p>ใช้ prototype เพื่อตรวจ navigation, hierarchy, states หรือ interaction แล้วนำสิ่งที่ยอมรับกลับเข้า spec ก่อนแยก tasks โดย <code>grill-design</code> เป็นตัวเลือกสำหรับกำหนดทิศทาง UI และ <code>ui-design</code> เป็น utility ที่ช่วยภายในงาน</p>')}${section('task-states','From ready to reviewed',code('todo → in_progress → in_review → done\n                    ↘ blocked (record the unblock condition)','TASK LIFECYCLE')+'<p><code>implement-task</code> ทำทีละงาน ตรวจสอบตาม policy แล้วส่งเข้า <code>in_review</code> ส่วน <code>code-review</code> เป็นผู้ตัดสินว่า ready for done หรือส่ง findings กลับไปแก้</p>')}${section('batch-work','Working through a batch','<p>เรียก <code>$auto-implement</code> เมื่อมี tasks อยู่แล้วและอนุญาตขอบเขตชัดเจน ระบบตรวจ user-action blockers ทั้งชุดก่อนเริ่ม จากนั้นทำทีละ task ตาม dependency โดยยังรักษา verification และ review เดิม การอนุญาต batch ไม่ได้อนุญาต commit, push หรือ deploy โดยอัตโนมัติ</p>')}${next('verification','Understand verification policy')}`},
  verification: {title:'Evidence before done.',label:'Verification policy',body:() => `<p class="doc-lead">กำหนดระดับการตรวจให้เข้ากับโปรเจกต์ โดยแยก unit tests, integration tests, E2E และ code review ออกจากกัน</p>${section('modes','Three modes, per capability','<p><code>setup-project</code> ถามนโยบายหนึ่งครั้งและบันทึกเป็นค่าเริ่มต้นให้ <code>implement-task</code> โดยสามารถระบุ override สำหรับ task ได้</p><table><thead><tr><th>Mode</th><th>Behavior</th></tr></thead><tbody><tr><td><code>auto</code></td><td>ทำเมื่อเกี่ยวข้องและมี installed skill กับ runner ที่รองรับ มิฉะนั้นบันทึกเหตุผลที่ข้าม</td></tr><tr><td><code>required</code></td><td>เมื่อเกี่ยวข้อง ต้องมี capability พร้อมใช้งานและผ่านการตรวจ ไม่เช่นนั้น block</td></tr><tr><td><code>off</code></td><td>ไม่เรียก capability นั้นและบันทึกว่า policy กำหนดให้ข้าม</td></tr></tbody></table>')}${section('sequence','One final review',code('implement-task\n  → selected test sub-agents\n  → integrate fixes + final checks\n  → in_review\n  → one final code-review\n  → done (only after approval)','VERIFICATION SEQUENCE')+'<p>แต่ละ test capability ที่เลือกทำงานผ่าน sub-agent ของตัวเองตามลำดับ ตัวหลักรวมผลและแก้ implementation ก่อนส่ง final reviewer เพียงหนึ่งครั้งหลังเข้า <code>in_review</code></p>')}${section('boundaries','Clear ownership','<ul><li>Test sub-agents แก้เฉพาะ test files ที่อยู่ในขอบเขต task</li><li>Main agent เป็นเจ้าของ implementation fixes และ final verification</li><li>Final reviewer แก้ได้เฉพาะ review evidence และสถานะ task ที่เลือก</li><li>ไม่ติดตั้ง capability ที่หายไปเอง หาก delegation ใช้ไม่ได้ ให้จัดการตาม auto/required policy</li><li>Review เป็นขั้นตอนสุดท้ายเสมอเมื่อ policy อนุญาตให้เรียก และไม่ถูกแทนด้วยผล tests</li></ul>')}${section('relevance','Select tests by relevance','<p>Unit tests ตรวจ logic แยกส่วน Integration tests ตรวจ boundary ระหว่างส่วนของระบบ E2E ตรวจเส้นทางใช้งานสำคัญ ไม่ต้องเรียกทุกตัวกับทุกงาน การข้ามต้องมีเหตุผล ส่วน code review ที่ไม่ใช่ off ใช้กับทุก implementation task</p>')}${next('skill-code-review','Explore code-review')}`},
  faq: {title:'Good questions.',label:'FAQ',body:() => `<p class="doc-lead">คำตอบก่อนเริ่มใช้ Phat Skills กับโปรเจกต์ของคุณ</p>${section('common-questions','Frequently asked questions',[
    ['ต้องติดตั้งทั้ง 19 skills ไหม?','ไม่จำเป็น เลือกติดตั้งด้วย --skill ได้ แต่ workflow บางตัวใช้ utility ร่วมกัน เช่น ui-design ในงาน UI ควรติดตั้ง skill ที่เกี่ยวข้องกับเส้นทางที่จะใช้ให้ครบ'],
    ['ใช้กับโปรเจกต์ที่มีโค้ดอยู่แล้วได้ไหม?','ได้ เริ่มด้วย ask-workflow ถ้า generated context ยังไม่มีหรือล้าสมัย จะให้ code-to-context อ่าน repository ก่อน setup และ specification'],
    ['ต้องทำ prototype ทุกครั้งไหม?','ไม่ต้อง Prototype เป็นทางเลือกเมื่อการเห็น UI ช่วยลดความไม่แน่ใจเรื่อง flow, states หรือโครงหน้า ถ้าพฤติกรรมชัดแล้วไป write-spec ได้เลย'],
    ['auto-implement จะ push หรือ deploy ให้ไหม?','การอนุญาตให้ทำ task batch ไม่ได้อนุญาต commit, push หรือ deploy งานเหล่านี้ต้องเป็นไปตามคำสั่งผู้ใช้และ policy ที่เกี่ยวข้อง'],
    ['ถ้าไม่มี test runner จะเกิดอะไรขึ้น?','โหมด auto บันทึกเหตุผลที่ข้ามเมื่อ capability ไม่พร้อม โหมด required จะ block เมื่อการตรวจนั้นเกี่ยวข้องแต่ทำไม่ได้ และไม่ติดตั้ง missing capability ให้เอง'],
    ['ใช้ในงานเชิงพาณิชย์ได้ไหม?','ได้ โปรเจกต์เผยแพร่ภายใต้ MIT License ให้รักษา copyright และ license notice ตามเงื่อนไข รายละเอียดอ่านได้ที่ LICENSE ใน source repository'],
    ['Skill รุ่นเก่าชื่อไม่ตรงกับเอกสารนี้?','ชื่อปัจจุบันใช้ neutral identifiers เช่น ask-workflow และ code-review ชื่อเก่าไม่ใช่ aliases ดู mapping ใน docs/migrations/skill-identifier-migration.md ของ repository']
  ].map(([q,a],i)=>`<details${i === 0 ? ' open' : ''}><summary>${q}</summary><p>${a}</p></details>`).join(''))}${section('more-resources','Go to the source','<ul><li><a href="https://github.com/phatysddev/skills/blob/main/README.md">README และ install examples ↗</a></li><li><a href="https://github.com/phatysddev/skills/blob/main/docs/workflow.md">Canonical workflow contract ↗</a></li><li><a href="https://github.com/phatysddev/skills/blob/main/docs/migrations/skill-identifier-migration.md">Skill identifier migration ↗</a></li><li><a href="https://github.com/phatysddev/skills/blob/main/LICENSE">MIT License ↗</a></li></ul>')}`}
};
if ($('#doc-article')) {
  let currentPage = '';
  const renderNavigation = () => {
    const query = $('#docs-search').value.trim().toLowerCase();
    const found = skills.filter(s => `${s.name} ${searchText(s.category)} ${searchText(s.description)}`.toLowerCase().includes(query));
    $('#docs-skill-nav').classList.toggle('searching', Boolean(query));
    $('#docs-skill-nav').innerHTML = [...new Set(found.map(s => s.category))].map(category => `<p class="nav-group">${category}</p>${found.filter(s=>s.category===category).map(s => `<a href="#skill-${s.name}" ${currentPage === `skill-${s.name}` ? 'class="active" aria-current="page"' : ''}>${s.name}</a>`).join('')}`).join('') || '<p class="empty-state" role="status">ไม่พบ skill ที่ตรงกับคำค้น</p>';
    localize($('.docs-sidebar'));
  };
  function renderDocument() {
    const hash = location.hash.slice(1) || 'introduction';
    if (hash === 'main') {
      if (!currentPage) { location.replace('#introduction'); return; }
      $('#doc-article h1')?.focus({preventScroll:true});
      $('#main').scrollIntoView();
      return;
    }
    // Heading links retain the owning page for shareable, reload-safe anchors.
    const [page, anchor] = hash.split('/');
    if (page === currentPage && anchor) { requestAnimationFrame(() => document.getElementById(anchor)?.scrollIntoView()); return; }
    const skill = page.startsWith('skill-') && skills.find(s => `skill-${s.name}` === page);
    const doc = docs[page]; currentPage = page;
    let title, body, label;
    if (skill) {
      title = skill.name; label = skill.name;
      const isTest = skill.category === 'Verification';
      body = `<p class="eyebrow">${skill.category.toUpperCase()}</p><p class="doc-lead">${skill.title}. ${skill.description}</p>${section('when-to-use','When to use it',`<p>${skill.when}</p>`)}${section('example','Try this prompt',code(`$${skill.name}\n${skill.prompt}`,'AGENT PROMPT')+`<p>ตัวอย่าง prompt เป็นจุดเริ่มต้น ปรับชื่อ spec, task และขอบเขตให้ตรงกับโปรเจกต์จริง${isTest ? ' โดยการเรียกอัตโนมัติเป็นหน้าที่ของ implement-task ตาม policy และ relevance' : ''}</p>`)}${section('install-skill','Install this skill',code(`${baseCommand} --skill ${skill.name} --agent codex --yes`))}${section('workflow-context','How it fits',`<p>${skill.category === 'Utilities' ? 'เป็น utility ที่สนับสนุนงานของ parent workflow ไม่ได้เพิ่ม workflow stage ใหม่หรือแทน canonical documents' : isTest ? 'เป็น verification capability ที่ implement-task เลือกตามขอบเขตและ policy ทำก่อน in_review และไม่แทน final code-review' : 'ใช้ร่วมกับบริบท requirements, spec และ task ของโปรเจกต์ อ่าน workflow guide เพื่อเลือกเส้นทางที่ตรงกับสถานะงาน'}</p><p><a href="#workflow">Read the workflow guide →</a></p>`)}${section('canonical-source','Read the full contract',`<p>หน้านี้สรุปการใช้งาน สำหรับรายละเอียด ข้อจำกัด และ output contract ให้ยึด SKILL.md เป็นหลัก</p><p><a href="${source}/blob/main/.agents/skills/${skill.name}/SKILL.md">Open ${skill.name}/SKILL.md ↗</a></p>`)}${next('workflow','Back to the workflow guide')}`;
    } else if (doc) {title = doc.title; label = doc.label; body = doc.body();}
    else {title = 'Page not found'; label = 'Not found'; body = '<p>ไม่พบหน้าเอกสารนี้ เลือกจากเมนูหรือกลับไปที่ Introduction</p>'+next('introduction','Back to introduction');}
    $('#doc-article').innerHTML = `<h1 tabindex="-1">${title}</h1>${body}`;
    $('#breadcrumb-label').textContent = label; document.title = `${label} · Phat Skills`;
    $('#on-this-page').innerHTML = $$('#doc-article h2').map(h => `<a href="#${page}/${h.id}">${h.textContent}</a>`).join('');
    $$('.docs-sidebar nav>a').forEach(a => { const active = a.hash === `#${page}`; a.classList.toggle('active', active); if(active) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current'); });
    renderNavigation();
    localize();
    if (anchor) requestAnimationFrame(() => document.getElementById(anchor)?.scrollIntoView()); else window.scrollTo({top:0,behavior:'instant'});
  }
  $('#docs-search').addEventListener('input', renderNavigation);
  $('#docs-skill-nav').addEventListener('click', event => {if(event.target.closest('a')) {$('#docs-search').value='';$('#docs-search').dispatchEvent(new Event('input', {bubbles:true}));$('#docs-search').blur();$('#docs-skill-nav').classList.remove('searching');}});
  window.addEventListener('hashchange', renderDocument); renderDocument();
}
if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.documentElement.classList.add('js-motion');
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {if(entry.isIntersecting){entry.target.classList.add('visible');observer.unobserve(entry.target);}}), {threshold:.08});
  $$('.section-heading,.example-grid,.principles-inner').forEach(el=>{el.classList.add('reveal');observer.observe(el);});
}

localize();
