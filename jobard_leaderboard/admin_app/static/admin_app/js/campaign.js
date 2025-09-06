// --- Sentinel ---
console.log('[campaign.js] v7 loaded');

// ---------- Utils ----------
function getCookie(name){
  let v=null;
  if(document.cookie&&document.cookie!==''){
    for(const c of document.cookie.split(';')){
      const ck=c.trim();
      if(ck.startsWith(name+'=')){ v=decodeURIComponent(ck.slice(name.length+1)); break; }
    }
  }
  if(!v){
    const t=document.querySelector('input[name="csrfmiddlewaretoken"]');
    if(t) v=t.value;
  }
  return v;
}

function updateHiddenInputs(){
  const cars=[...document.querySelectorAll('#cars-selected li')].map(li=>li.dataset.id);
  const layouts=[...document.querySelectorAll('#layouts-selected li')].map(li=>li.dataset.id);
  const ci=document.getElementById('cars-input'), li=document.getElementById('layouts-input');
  if(ci) ci.value=cars.join(',');
  if(li) li.value=layouts.join(',');
}

async function saveCampaignItems(campaignId, silent=true){
  const cars=[...document.querySelectorAll('#cars-selected li')].map(el=>Number(el.dataset.id));
  const layouts=[...document.querySelectorAll('#layouts-selected li')].map(el=>Number(el.dataset.id));
  try{
    const res=await fetch(`/campaigns/${campaignId}/update_items/`,{
      method:'POST',
      headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':getCookie('csrftoken'),
        'X-Requested-With':'XMLHttpRequest'
      },
      body:JSON.stringify({cars,layouts})
    });
    if(!res.ok) throw new Error('HTTP '+res.status);
    if(!silent) console.debug('Campagne mise à jour');
  }catch(e){
    console.error('Échec maj',e);
    if(!silent) alert('Maj échouée (voir console).');
  }
}

// Trouver le nom d'une voiture à partir de son id (si on doit créer un <li>)
function getCarNameById(id){
  const el=document.querySelector(`#cars-available [data-id="${CSS.escape(String(id))}"]`);
  if(el) return (el.textContent||'').trim();
  return `Voiture #${id}`;
}

// Création d'un LI voiture standard
function createCarLi(id, name){
  const li=document.createElement('li');
  li.className='list-group-item draggable';
  li.setAttribute('draggable','true');
  li.dataset.id=String(id);
  li.dataset.type='car';
  li.textContent=name;
  return li;
}

// ---------- DnD délégué & bidirectionnel ----------
let dragPayload=null; // {kind:'car'|'class', ids:number[]|string[], label?:string, name?:string, id?:string}

document.addEventListener('dragstart', (e)=>{
  const handle=e.target.closest('.draggable');
  if(!handle) return;

  // type 'car' (li) ou 'class' (badge)
  const kind = handle.dataset.type || (handle.tagName==='LI' ? 'car' : 'car');
  let payload = { kind };

  if (kind === 'class') {
    const raw = (handle.dataset.ids || '').split(',').map(s => s.trim()).filter(Boolean);
    payload.ids = raw;
    payload.label = handle.dataset.label || 'Classe';
  } else {
    payload.kind = 'car';
    payload.id = handle.dataset.id;
    payload.name = (handle.textContent||'').trim();
  }

  dragPayload = payload;

  try{
    // on pousse un JSON et un plain fallback
    e.dataTransfer.setData('application/json', JSON.stringify(payload));
    e.dataTransfer.setData('text/plain', payload.kind === 'class' ? (payload.ids||[]).join(',') : String(payload.id));
    e.dataTransfer.effectAllowed='move';
  }catch{}

  // petit effet "move"
  setTimeout(()=>{ if(handle) handle.style.opacity='0.4'; }, 0);
});

document.addEventListener('dragend', (e)=>{
  const handle=e.target.closest('.draggable');
  if(handle) handle.style.opacity='1';
  dragPayload=null;
});

// Résout la dropzone même si on droppe sur un conteneur
function resolveDropzone(target){
  let dz = target.closest('.droppable');
  if (dz) return dz;
  const byId = id => document.getElementById(id);
  if (target.closest('#cars-selected') || target.id==='cars-selected') return byId('cars-selected');
  if (target.closest('#cars-available') || target.id==='cars-available') return byId('cars-available');
  if (target.closest('#layouts-selected') || target.id==='layouts-selected') return byId('layouts-selected');
  if (target.closest('#layouts-available') || target.id==='layouts-available') return byId('layouts-available');
  return null;
}

document.addEventListener('dragover', (e)=>{
  const dz=resolveDropzone(e.target);
  if(!dz) return;
  e.preventDefault();
  try{ e.dataTransfer.dropEffect='move'; }catch{}
});

document.addEventListener('drop', (e)=>{
  const dropzone=resolveDropzone(e.target);
  if(!dropzone) return;
  e.preventDefault();

  // Récup du payload
  let payload=null;
  try{
    const raw=e.dataTransfer.getData('application/json');
    if(raw) payload=JSON.parse(raw);
  }catch{}
  if(!payload){
    // fallback ultra-simple
    const ids=(e.dataTransfer.getData('text/plain')||'').split(',').filter(Boolean);
    payload = ids.length>1 ? {kind:'class', ids} : {kind:'car', id:ids[0]};
  }
  if(!payload && dragPayload) payload=dragPayload;
  if(!payload) return;

  // MOVE strict : on retire les anciens exemplaires des ids concernées
  const removeByIds = (idsArr) => {
    idsArr.forEach(id=>{
      document.querySelectorAll(`[data-id="${CSS.escape(String(id))}"]`).forEach(el=>el.remove());
    });
  };

  if (payload.kind === 'class') {
    const idsArr = (payload.ids||[]).map(x=>String(x));
    removeByIds(idsArr);
    // insère chaque voiture dans la dropzone
    idsArr.forEach(id=>{
      const name=getCarNameById(id);
      dropzone.appendChild(createCarLi(id, name));
    });
  } else {
    const id = String(payload.id);
    removeByIds([id]);
    const name = payload.name || getCarNameById(id);
    dropzone.appendChild(createCarLi(id, name));
  }

  // MAJ + envoi serveur
  updateHiddenInputs();
  const campaignId=document.getElementById('campaign-id')?.value;
  if(campaignId) saveCampaignItems(campaignId,true);
});

// ---------- Ready ----------
document.addEventListener('DOMContentLoaded', ()=>{
  console.log('[campaign.js] DOM ready');
  // s’assurer que tout ce qui est voiture est draggable
  document.querySelectorAll('#cars-available li, #cars-selected li').forEach(li=>{
    li.setAttribute('draggable','true');
    li.dataset.type='car';
  });
  // badges de classe déjà marqués draggable dans le template
  updateHiddenInputs();
});
