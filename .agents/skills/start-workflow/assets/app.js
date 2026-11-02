'use strict';
const $ = id => document.getElementById(id);
let state, pageId, busy = false, questionSet, pagesSignature;
let token = document.querySelector('meta[name=workflow-token]').content;
const node = (tag, text) => { const el = document.createElement(tag); if (text !== undefined) el.textContent = text; return el; };
function error(message) { $('error').textContent = message; $('error').hidden = !message; }
async function send(kind, payload) {
  if (busy) return;
  busy = true;
  document.querySelectorAll('button[type=submit]').forEach(b => b.disabled = true);
  error('');
  try {
    const response = await fetch('/api/events', {method:'POST', headers:{'Content-Type':'application/json','X-Workflow-Token':token},body:JSON.stringify({kind,key:crypto.randomUUID(),revision:state.revision,...payload})});
    const result = await response.json();
    if (!response.ok) throw new Error(result.error);
    await refresh();
  } catch(e) { error(e.message); }
  finally {busy = false; updateDisabled();}
}
function updateDisabled() { document.querySelectorAll('button[type=submit]').forEach(b => b.disabled = busy || !state || state.status === 'working' || (b.closest('#feedback-form') && !pageId)); }
function historyInto(id) {$(id).replaceChildren(...state.history.slice(-12).map(item => node('li', item.text)));}
function actionsInto(id) {
  $(id).replaceChildren(...(state.actions || []).map(action => {const b = node('button', action.label); b.type='button'; b.onclick=()=>send('action.requested',{action:action.id}); return b;}));
}
function showPage(id) {
  pageId=id;
  const page=state.pages.find(p=>p.id===id);
  $('preview').hidden=!page; $('empty-preview').hidden=!!page;
  if(page) {
    const relative=page.path.slice('docs/assets/prototype/'.length).split('/').map(encodeURIComponent).join('/');
    const url='/preview/'+relative;
    if($('preview').dataset.url!==url) {$('preview').src=url; $('preview').dataset.url=url;}
  }
  document.querySelectorAll('[role=tab]').forEach(b=>b.setAttribute('aria-selected',String(b.dataset.id===id)));
  updateDisabled();
}
function render() {
  const start=state.route==='/' || (state.status==='complete' && location.pathname==='/');
  const prototype=!start && state.route==='/prototype';
  $('new-workflow').hidden=state.status!=='complete'||start;
  $('previous-result').hidden=state.status!=='complete';
  $('previous-result').textContent=state.status==='complete'?state.message:'';
  $('start').hidden=!start; $('workflow').hidden=start||prototype; $('prototype').hidden=!prototype;
  if(!start && location.pathname!==state.route) history.replaceState(null,'',state.route);
  $('stage').textContent=state.stage;
  $('status').textContent=({working:'อยู่ระหว่างดำเนินงาน',waiting:'รอคำตอบ',blocked:'ต้องการข้อมูลเพิ่ม',complete:'เสร็จแล้ว',idle:'พร้อมเริ่ม'})[state.status];
  $('heading').textContent=state.route==='/grill'?'ทำความเข้าใจงาน':state.stage;
  $('section-label').textContent=state.route==='/grill'?'DISCOVERY':'WORKFLOW';
  $('message').textContent=state.message;
  $('prototype-message').textContent=state.message;
  $('project').textContent=state.project;
  const questionHost=prototype?document.querySelector('.prototype-layout aside'):$('workflow');
  questionHost.insertBefore($('questions-form'),prototype?$('feedback-form'):$('actions')); 
  historyInto('history'); historyInto('prototype-history');
  actionsInto('actions'); actionsInto('prototype-actions');
  if(questionSet!==state.questionSet || (!state.questions.length && $('questions').childElementCount)) {
    questionSet=state.questionSet;
    $('questions').replaceChildren(...state.questions.map(q=>{
      const field=node('fieldset'); field.append(node('legend',q.label+(q.required?' *':'')));
      if(q.help)field.append(node('p',q.help));
      if(q.type==='checkbox') {
        q.options.forEach(option=>{const label=node('label');label.className='choice';const input=node('input');input.type='checkbox';input.name=q.id;input.value=option;label.append(input,document.createTextNode(option));field.append(label);});
      } else {
        const input=node(q.type==='input'?'input':q.type==='select'?'select':'textarea');
        input.name=q.id;input.id='q-'+q.id;input.required=!!q.required;input.setAttribute('aria-label',q.label);
        if(q.type==='select') {const blank=node('option','เลือกคำตอบ');blank.value='';input.append(blank,...q.options.map(o=>{const opt=node('option',o);opt.value=o;return opt;}));}
        if(q.type==='textarea')input.rows=4;
        field.append(input);
      }
      return field;
    }));
  }
  $('answer-button').hidden=!state.questions.length;
  const signature=JSON.stringify(state.pages);
  if(pagesSignature!==signature) {
    pagesSignature=signature;
    $('page-tabs').replaceChildren(...state.pages.map(p=>{const b=node('button',p.title);b.type='button';b.dataset.id=p.id;b.setAttribute('role','tab');b.onclick=()=>showPage(p.id);return b;}));
    const previous=pageId;pageId=state.pages.some(p=>p.id===previous)?previous:state.pages[0]?.id;
    $('preview').dataset.url='';showPage(pageId);
  }
  updateDisabled();
}
async function refresh() {
  try {
    const response=await fetch('/api/state');if(!response.ok)throw new Error('เชื่อมต่อไม่ได้');
    const next=await response.json();
    if(next.sessionToken)token=next.sessionToken;
    delete next.sessionToken;
    $('connection').textContent='เชื่อมต่อแล้ว';
    if(!state||next.revision!==state.revision){state=next;render();}
  } catch(e) {$('connection').textContent='การเชื่อมต่อขาดหาย · กำลังลองใหม่';}
}
$('new-workflow').onclick=()=>{history.replaceState(null,'','/');$('request').value='';$('files').value='';$('files-list').textContent='';render();};
$('files').onchange=()=>{$('files-list').textContent=Array.from($('files').files).map(f=>f.name).join('\n');};
$('request-form').onsubmit=async e=>{
  e.preventDefault();
  const files=Array.from($('files').files);
  if(files.length>10||files.reduce((n,f)=>n+f.size,0)>20*1024*1024)return error('แนบได้ไม่เกิน 10 ไฟล์ และรวมไม่เกิน 20 MB');
  const encoded=[];
  try {for(const file of files){const data=await new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(reader.result.split(',')[1]);reader.onerror=reject;reader.readAsDataURL(file);});encoded.push({name:file.name,data});}}
  catch{return error('อ่านไฟล์ไม่สำเร็จ กรุณาลองใหม่');}
  await send('request.submitted',{text:$('request').value,files:encoded});
};
$('questions-form').onsubmit=e=>{e.preventDefault();const form=new FormData(e.target),answers={};for(const q of state.questions)answers[q.id]=q.type==='checkbox'?form.getAll(q.id):form.get(q.id);send('answers.submitted',{questionSet:state.questionSet,answers});};
$('feedback-form').onsubmit=async e=>{e.preventDefault();await send('prototype.feedback',{text:$('feedback').value,page:pageId});if(state.status==='working')$('feedback').value='';};
$('viewport').onchange=e=>{$('preview').style.width=e.target.value;};
$('reload').onclick=()=>{if($('preview').dataset.url)$('preview').src=$('preview').dataset.url+'?t='+Date.now();};
refresh();setInterval(refresh,1200);
