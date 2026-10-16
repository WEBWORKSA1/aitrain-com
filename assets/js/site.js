/* AiTrain.com site script — no dependencies */
(function(){
  'use strict';
  var d=document, root=d.documentElement;

  /* ---------- Contact address: never present in page source ---------- */
  var K=[122,120,116,57,123,126,118,122,112,87,38,118,100,124,101,120,96,117,114,96];
  function addr(){return K.slice().reverse().map(function(n){return String.fromCharCode(n^23);}).join('');}
  function endpoint(){return 'https://formsubmit.co/ajax/'+addr();}
  d.querySelectorAll('[data-mail]').forEach(function(a){
    a.addEventListener('click',function(ev){
      ev.preventDefault();
      var subj=a.getAttribute('data-mail')||'AiTrain.com inquiry';
      window.location.href='mailto:'+addr()+'?subject='+encodeURIComponent(subj);
    });
  });

  /* ---------- Theme ---------- */
  try{var t=localStorage.getItem('at-theme'); if(t) root.setAttribute('data-theme',t);}catch(e){}
  var tb=d.querySelector('.theme-btn');
  if(tb) tb.addEventListener('click',function(){
    var dark=root.getAttribute('data-theme')==='dark'||(!root.getAttribute('data-theme')&&matchMedia('(prefers-color-scheme: dark)').matches);
    var next=dark?'light':'dark'; root.setAttribute('data-theme',next);
    try{localStorage.setItem('at-theme',next);}catch(e){}
  });

  /* ---------- Mobile menu ---------- */
  var mb=d.querySelector('.menu-btn'), nav=d.querySelector('.nav');
  if(mb&&nav) mb.addEventListener('click',function(){
    var open=nav.classList.toggle('open'); mb.setAttribute('aria-expanded',open);
  });

  /* ---------- Forms → FormSubmit (AJAX) ---------- */
  d.querySelectorAll('form[data-form]').forEach(function(f){
    f.addEventListener('submit',function(ev){
      ev.preventDefault();
      var msg=f.querySelector('.form-msg');
      if(!f.checkValidity()){f.reportValidity();return;}
      if(f.querySelector('.hp input') && f.querySelector('.hp input').value) return; // bot
      var data={};
      new FormData(f).forEach(function(v,k){ if(k==='_hp') return; data[k]=data[k]?data[k]+', '+v:v; });
      data._subject='AiTrain.com — '+(f.getAttribute('data-form')||'Form')+' submission';
      data._template='table'; data._captcha='false';
      data.page=location.pathname;
      var btn=f.querySelector('[type=submit]'); if(btn){btn.disabled=true;btn.dataset.l=btn.textContent;btn.textContent='Sending…';}
      if(msg){msg.className='form-msg';msg.textContent='';}
      fetch(endpoint(),{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(data)})
        .then(function(r){return r.json().catch(function(){return {};}).then(function(j){return {ok:r.ok,j:j};});})
        .then(function(res){
          if(res.ok && String(res.j.success)!=='false'){
            var next=f.getAttribute('data-next');
            if(next){location.href=next;return;}
            f.reset(); if(msg){msg.className='form-msg ok';msg.textContent='Sent. We reply within 2 business days.';}
          } else throw new Error();
        })
        .catch(function(){ if(msg){msg.className='form-msg err';msg.textContent='Not sent — check your connection and try again.';} })
        .finally(function(){ if(btn){btn.disabled=false;btn.textContent=btn.dataset.l;} });
    });
  });

  /* ---------- Multi-step lead form ---------- */
  d.querySelectorAll('[data-steps]').forEach(function(f){
    var steps=[].slice.call(f.querySelectorAll('.step')), bars=[].slice.call(f.querySelectorAll('.steps-bar span')), i=0;
    function show(n){steps.forEach(function(s,k){s.classList.toggle('on',k===n);}); bars.forEach(function(b,k){b.classList.toggle('on',k<=n);}); i=n;
      var first=steps[n].querySelector('input,select,textarea'); if(first&&n>0) first.focus();}
    f.querySelectorAll('[data-next-step]').forEach(function(b){b.addEventListener('click',function(){
      var ok=true; steps[i].querySelectorAll('input,select,textarea').forEach(function(el){ if(ok&&!el.checkValidity()){el.reportValidity();ok=false;} });
      if(ok&&i<steps.length-1) show(i+1);
    });});
    f.querySelectorAll('[data-prev-step]').forEach(function(b){b.addEventListener('click',function(){ if(i>0) show(i-1); });});
    show(0);
  });

  /* ---------- Copy buttons ---------- */
  d.querySelectorAll('[data-copy]').forEach(function(b){
    b.addEventListener('click',function(){
      var el=d.getElementById(b.getAttribute('data-copy')); if(!el) return;
      var txt=el.innerText;
      (navigator.clipboard?navigator.clipboard.writeText(txt):Promise.reject()).then(function(){b.textContent='Copied';setTimeout(function(){b.textContent='Copy prompt';},1600);})
      .catch(function(){var r=d.createRange();r.selectNodeContents(el);var s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Selected — press Ctrl+C';});
    });
  });

  /* ---------- Filterable lists (tools, prompts, guides) ---------- */
  d.querySelectorAll('[data-filter]').forEach(function(box){
    var list=d.getElementById(box.getAttribute('data-filter')); if(!list) return;
    var q=box.querySelector('input[type=search]'), btns=[].slice.call(box.querySelectorAll('button[data-cat]')), cat='all';
    var empty=list.parentNode.querySelector('.empty');
    function run(){
      var term=(q&&q.value||'').toLowerCase().trim(), shown=0;
      [].forEach.call(list.children,function(it){
        var hit=(cat==='all'||it.getAttribute('data-cat')===cat)&&(!term||it.textContent.toLowerCase().indexOf(term)>-1);
        it.hidden=!hit; if(hit) shown++;
      });
      if(empty) empty.hidden=shown>0;
    }
    btns.forEach(function(b){b.addEventListener('click',function(){cat=b.getAttribute('data-cat');btns.forEach(function(x){x.setAttribute('aria-pressed',x===b);});run();});});
    if(q) q.addEventListener('input',run);
    run();
  });

  /* ---------- Lazy YouTube (privacy-enhanced) ---------- */
  d.querySelectorAll('.vid button[data-yt]').forEach(function(b){
    b.addEventListener('click',function(){
      var f=d.createElement('iframe');
      f.src='https://www.youtube-nocookie.com/embed/'+b.getAttribute('data-yt')+'?autoplay=1&rel=0';
      f.title=b.getAttribute('aria-label')||'Video'; f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'; f.allowFullscreen=true;
      b.parentNode.replaceChild(f,b);
    });
  });

  /* ---------- Line map captions ---------- */
  var cap=d.getElementById('map-cap');
  if(cap) d.querySelectorAll('.map .st').forEach(function(s){
    function on(){cap.innerHTML='<span><b>'+s.getAttribute('data-line')+'</b> — '+s.getAttribute('data-name')+'</span><a href="'+s.getAttribute('data-href')+'">Open this line</a>';}
    s.addEventListener('mouseenter',on); s.addEventListener('focus',on);
    s.addEventListener('click',function(){location.href=s.getAttribute('data-href');});
    s.addEventListener('keydown',function(e){if(e.key==='Enter')location.href=s.getAttribute('data-href');});
  });

  /* ---------- AI readiness quiz ---------- */
  var quiz=d.getElementById('quiz');
  if(quiz) quiz.addEventListener('submit',function(ev){
    ev.preventDefault();
    var total=0,n=0,missing=false;
    quiz.querySelectorAll('fieldset.q').forEach(function(fs){var c=fs.querySelector('input:checked'); if(!c) missing=true; else {total+=+c.value;n++;}});
    if(missing){alert('Answer every question to see your score.');return;}
    var pct=Math.round(total/(n*3)*100), lvl, rec;
    if(pct<35){lvl='Boarding';rec='Start with the Foundations line and the free AI Essentials guides. A 2-hour team kickoff would remove most of the friction you described.';}
    else if(pct<65){lvl='Moving';rec='You have pockets of use but no system. The Prompt Craft and Workflow Automation lines will turn scattered wins into repeatable processes.';}
    else {lvl='Express';rec='You are ahead of most teams. Focus on Build with AI and Responsible AI, and consider a custom cohort for advanced use cases.';}
    var r=d.getElementById('quiz-result');
    r.querySelector('.out').textContent=pct+'/100 — '+lvl;
    r.querySelector('.meter i').style.width=pct+'%';
    r.querySelector('.rec').textContent=rec;
    var hidden=d.getElementById('score-field'); if(hidden) hidden.value=pct+' ('+lvl+')';
    r.classList.add('on'); r.scrollIntoView({behavior:'smooth',block:'start'});
  });

  /* ---------- Training ROI calculator ---------- */
  var roi=d.getElementById('roi');
  if(roi){
    function money(v){return '$'+Math.round(v).toLocaleString('en-US');}
    function calc(){
      var p=+roi.people.value||0, w=+roi.wage.value||0, h=+roi.hours.value||0, a=(+roi.adopt.value||0)/100, c=+roi.cost.value||0;
      var annual=p*a*h*w*46, invest=p*c, net=annual-invest, mult=invest?annual/invest:0;
      d.getElementById('roi-save').textContent=money(annual);
      d.getElementById('roi-net').textContent=money(net);
      d.getElementById('roi-mult').textContent=invest?mult.toFixed(1)+'×':'—';
      d.getElementById('roi-hours').textContent=Math.round(p*a*h*46).toLocaleString('en-US')+' hours';
      var hf=d.getElementById('roi-field'); if(hf) hf.value='People '+p+', est. annual value '+money(annual)+', ROI '+(invest?mult.toFixed(1)+'x':'n/a');
    }
    roi.addEventListener('input',calc); calc();
  }

  /* ---------- Cookie consent ---------- */
  var ck=d.querySelector('.cookie');
  try{ if(ck && !localStorage.getItem('at-consent')) ck.classList.add('on'); }catch(e){ if(ck) ck.classList.add('on'); }
  d.querySelectorAll('[data-consent]').forEach(function(b){b.addEventListener('click',function(){
    try{localStorage.setItem('at-consent',b.getAttribute('data-consent'));}catch(e){}
    if(b.getAttribute('data-consent')==='essential'){ (window.adsbygoogle=window.adsbygoogle||[]).requestNonPersonalizedAds=1; }
    ck.classList.remove('on');
  });});

  /* ---------- Back to top ---------- */
  var tt=d.querySelector('.to-top');
  if(tt){ addEventListener('scroll',function(){tt.style.display=scrollY>900?'block':'none';},{passive:true}); tt.addEventListener('click',function(){scrollTo({top:0});}); }

  /* ---------- Prefill source fields from ?topic= / ?plan= ---------- */
  try{
    var qs=new URLSearchParams(location.search);
    d.querySelectorAll('input[name="source_topic"]').forEach(function(i){ i.value=(qs.get('topic')||'')+(qs.get('utm_source')?' | utm:'+qs.get('utm_source'):'')+(document.referrer?' | ref:'+document.referrer:''); });
    var pl=qs.get('plan'); if(pl){ var sel=d.querySelector('select[name="tier"]'); if(sel){ [].forEach.call(sel.options,function(o){ if(o.value===pl) sel.value=pl; }); } }
  }catch(e){}

  var y=d.getElementById('yr'); if(y) y.textContent=new Date().getFullYear();
})();
