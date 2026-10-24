(function(){
  const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const LIVE=/(^|\.)zondags\.be$/.test(location.hostname);
  if(/\/boeken(\.html)?\/?$/.test(location.pathname)) document.documentElement.classList.add('pg-boeken');

  /* B2B-focus: buiten de jobpagina's geen sollicitanten-pil in de chat-teaser (zie .zd-b2b in site.css) */
  if(!/\/(jobs|zondag-worden|studentenjob|flexi|werken)/.test(location.pathname)) document.documentElement.classList.add('zd-b2b');

  /* Mobiel menu */
  const burger=$('.burger');
  if(burger) burger.addEventListener('click',()=>{const o=document.body.classList.toggle('menu-open');burger.setAttribute('aria-expanded',o);});

  /* Nav */
  const nav=$('#nav'); let lastY=0;
  addEventListener('scroll',()=>{const y=scrollY;nav.classList.toggle('is-scrolled',y>40);nav.classList.toggle('is-hidden',y>lastY&&y>400&&!document.body.classList.contains('menu-open'));lastY=y;},{passive:true});

  /* Formulieren */
  const lead=$('#leadForm');
  if(lead) lead.addEventListener('submit',e=>{
    let first=null;
    [['l-naam','e-naam',v=>v.trim().length>1],['l-mail','e-mail',v=>/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)],['l-gsm','e-gsm',v=>v.replace(/\D/g,'').length>=9]].forEach(([i,er,ok])=>{
      const el=document.getElementById(i), bad=!ok(el.value);
      el.setAttribute('aria-invalid',bad); document.getElementById(er).hidden=!bad; if(bad&&!first) first=el;
    });
    if(first){e.preventDefault();first.focus();return;}
    if(!LIVE){e.preventDefault();$('#leadFields').hidden=true;const t=$('#leadThanks');t.hidden=false;t.focus();}
  });
  const job=$('#jobForm');
  if(job) job.addEventListener('submit',e=>{
    const ok=$('#j-ok');
    if(!ok.checked){e.preventDefault();$('#e-ok').hidden=false;ok.focus();return;}
    if(!LIVE){e.preventDefault();$('#jobFields').hidden=true;$('#jobThanks').hidden=false;}
  });

  /* Korte formulieren op contentpagina's */
  $$('form[data-quick]').forEach(f=>f.addEventListener('submit',e=>{
    let bad=false;
    f.querySelectorAll('[required]').forEach(el=>{
      const v=el.type==='checkbox'?el.checked:el.value.trim();
      const ok=el.type==='email'?/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value):!!v;
      el.setAttribute('aria-invalid',!ok); if(!ok&&!bad){bad=true;el.focus();}
    });
    f.querySelector('[data-err]').hidden=!bad;
    if(bad){e.preventDefault();return;}
    if(!LIVE){e.preventDefault();f.innerHTML='<p class="thanks">Dank je. We nemen snel contact op.</p>';}
  }));

  /* Keuzelijst met data-other (Waarvoor?): bij 'Iets anders' verschijnt het tekstveld met die naam */
  $$('select[data-other]').forEach(s=>{const o=s.form&&s.form.querySelector('[name="'+s.dataset.other+'"]'),w=o&&o.closest('.f');if(!w)return;const t=e=>{const on=s.value==='Iets anders';w.hidden=!on;if(on&&e)o.focus();};s.addEventListener('change',t);t();});

  /* Aangevinkte keuzes samenvoegen tot één veld (leesbaar in de mail) */
  $$('form[action*="formsubmit"]').forEach(f=>f.addEventListener('submit',e=>{
    if(e.defaultPrevented) return;
    const groups={};
    f.querySelectorAll('select[data-other]').forEach(s=>{const o=f.querySelector('[name="'+s.dataset.other+'"]');if(o&&s.value!=='Iets anders')o.value='';});
    f.querySelectorAll('input[type=checkbox][data-group]').forEach(c=>{(groups[c.dataset.group]=groups[c.dataset.group]||[]);const o=c.dataset.other?f.querySelector('[name="'+c.dataset.other+'"]'):null;if(o&&!c.checked)o.value='';if(c.checked)groups[c.dataset.group].push(o&&o.value.trim()?c.value+': '+o.value.trim():c.value);});
    Object.entries(groups).forEach(([k,v])=>{let h=f.querySelector('input[type=hidden][name="'+k+'"]');if(!h){h=document.createElement('input');h.type='hidden';h.name=k;f.appendChild(h);}h.value=v.join(', ')||'niets aangeduid';});
  }));

  /* Herkomst van de bezoeker: kanaal (SEO, SEA, ChatGPT, social, direct, ...) van het laatste niet-rechtstreekse bezoek, zodat elke aanvraag toont waar ze vandaan komt */
  const SRC=(function(){
    let s=null; try{s=JSON.parse(localStorage.getItem('zd_src')||'null');}catch(e){}
    const q=new URLSearchParams(location.search), g=k=>(q.get(k)||'').toLowerCase();
    const src=g('utm_source'), med=g('utm_medium'), camp=q.get('utm_campaign')||'';
    const host=document.referrer&&document.referrer.indexOf(location.host)<0?document.referrer.replace(/^https?:\/\//,'').split('/')[0].replace(/^www\./,'').toLowerCase():'';
    const paid=/^(cpc|ppc|paid|paidsearch|paid_search|paid-search|paid_social|paid-social|cpm|display)$/.test(med)||q.has('gclid')||q.has('gbraid')||q.has('wbraid')||q.has('msclkid');
    let kanaal='Direct';
    if(q.has('gclid')||q.has('gbraid')||q.has('wbraid')||(paid&&/google/.test(src))) kanaal='SEA (Google Ads)';
    else if(q.has('msclkid')||(paid&&/bing|microsoft/.test(src))) kanaal='SEA (Bing)';
    else if(/(^|\.)(chatgpt\.com|chat\.openai\.com|openai\.com)$/.test(host)||/chatgpt|openai/.test(src)) kanaal=paid?'ChatGPT Ads':'ChatGPT (organisch)';
    else if(/(^|\.)(perplexity\.ai|claude\.ai|gemini\.google\.com|copilot\.microsoft\.com|you\.com|poe\.com|mistral\.ai)$/.test(host)||/perplexity|claude|gemini|copilot/.test(src)) kanaal='AI-zoekmachine';
    else if(med==='email'||/^(email|e-mail|nieuwsbrief|newsletter|klaviyo)$/.test(src)) kanaal='E-mail';
    else if(paid&&/facebook|instagram|meta|linkedin|tiktok|pinterest/.test(src)) kanaal='Social (betaald)';
    else if(paid) kanaal='Betaald (andere)';
    else if(/(^|\.)google\.[a-z.]+$/.test(host)) kanaal='SEO (Google)';
    else if(/(^|\.)(bing\.com|duckduckgo\.com|ecosia\.org|yahoo\.com|qwant\.com|startpage\.com|search\.brave\.com)$/.test(host)) kanaal='SEO (andere zoekmachine)';
    else if(/(^|\.)(facebook\.com|instagram\.com|linkedin\.com|lnkd\.in|t\.co|twitter\.com|x\.com|tiktok\.com|pinterest\.[a-z]+|youtube\.com|whatsapp\.com|l\.messenger\.com)$/.test(host)||/facebook|instagram|linkedin|tiktok|whatsapp/.test(src)) kanaal='Social';
    else if(host) kanaal='Verwijzing';
    else if(src) kanaal='Campagne ('+src+')';
    if(kanaal!=='Direct'||!s){
      const detail=[src,med,camp].filter(Boolean).join(' / ')||host||(q.has('gclid')?'gclid':'');
      const now={kanaal:kanaal,detail:detail,campagne:camp,verwijzer:host,landing:location.pathname,datum:new Date().toISOString().slice(0,10)};
      now.bron=kanaal+(detail?' | '+detail:'');
      if(!s||kanaal!=='Direct'){s=now;try{localStorage.setItem('zd_src',JSON.stringify(s));}catch(e){}}
    }
    if(s&&!s.kanaal){s.kanaal='Onbekend (oud)';s.bron=s.kanaal+(s.bron?' | '+s.bron:'');}
    window.ZD_SRC=s;
    return s;
  })();

  /* Meting voor Google Ads (conversie "Aanvraag verzonden"), alleen na toestemming van de bezoeker */
  const AW='AW-18500746602', CONV='AW-18500746602/yeOuCKajopUdEOr66_VE';
  const GA4=''; /* INVUL: GA4-meet-ID van Zondags (G-...). Leeg = enkel Google Ads en dataLayer */
  window.ZD_CONV=CONV;
  window.dataLayer=window.dataLayer||[];
  if(!window.gtag) window.gtag=function(){window.dataLayer.push(arguments);};
  if(LIVE){
    const grant={ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted',analytics_storage:'granted'};
    let ok=null; try{ok=localStorage.getItem('zd_consent');}catch(e){}
    gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',wait_for_update:400});
    if(ok==='ja') gtag('consent','update',grant);
    gtag('js',new Date()); gtag('config',AW); if(GA4) gtag('config',GA4);
    const gs=document.createElement('script'); gs.async=true; gs.src='https://www.googletagmanager.com/gtag/js?id='+AW; document.head.appendChild(gs);
    if(/^\/bedankt(\.html)?\/?$/.test(location.pathname)){
      let done=null; try{done=sessionStorage.getItem('zd_conv');}catch(e){}
      let lt=null; try{lt=sessionStorage.getItem('zd_lead');}catch(e){}
      /* Enkel een klantaanvraag telt als conversie. Kandidaten komen op /bedankt-kandidaat en tellen niet mee. */
      if(!done&&lt==='klant'){gtag('event','conversion',{send_to:CONV});try{sessionStorage.setItem('zd_conv','1');}catch(e){}}
    }
    if(ok===null){
      const bar=document.createElement('div'); bar.className='consent'; bar.setAttribute('role','dialog'); bar.setAttribute('aria-label','Cookies');
      bar.innerHTML='<p>We meten anoniem of onze advertenties werken. Mag dat?</p><div><button type="button" data-c="ja">Ja, prima</button><button type="button" data-c="nee">Nee, bedankt</button></div>';
      bar.addEventListener('click',e=>{const c=e.target.getAttribute&&e.target.getAttribute('data-c'); if(!c) return;
        try{localStorage.setItem('zd_consent',c);}catch(err){}
        if(c==='ja') gtag('consent','update',grant);
        bar.remove();});
      document.body.appendChild(bar);
    }
  }

  /* Elke formulieraanvraag ook meteen naar WhatsApp en de leadsheet (zelfde koppeling als de chat) */
  const HOOK='https://hook.eu2.make.com/kxqukx7dzzc666hvuefito1g4uytlvad';
  const waNum=v=>{let d=String(v).replace(/[^0-9+]/g,'');if(d.indexOf('+')===0)return d.slice(1);if(d.indexOf('00')===0)return d.slice(2);if(d.indexOf('0')===0)return '32'+d.slice(1);return d;};
  $$('form[action*="formsubmit"]').forEach(f=>f.addEventListener('submit',e=>{
    if(e.defaultPrevented) return;
    const add=(n,v)=>{let h=f.querySelector('input[type=hidden][name="'+n+'"]');if(!h){h=document.createElement('input');h.type='hidden';h.name=n;f.appendChild(h);}h.value=v;};
    if(SRC){add('Bron',SRC.bron);add('Kanaal',SRC.kanaal);add('Eerste pagina',SRC.landing);}
    const fd=new FormData(f), g=ns=>{for(const n of ns){const v=fd.get(n);if(v&&String(v).trim())return String(v).trim();}return '';};
    const subj=g(['_subject']), kand=f.dataset.lead==='kandidaat'||/kandidaat|sollicit/i.test(subj)||!!f.querySelector('[name="Statuut"]');
    /* Leadmeting: generate_lead enkel voor klantformulieren */
    const lt=kand?'kandidaat':'klant';
    try{sessionStorage.setItem('zd_lead',lt);sessionStorage.removeItem('zd_conv');}catch(err){}
    window.dataLayer=window.dataLayer||[];
    window.dataLayer.push({event:kand?'kandidaat_aanmelding':'generate_lead',lead_type:lt,form_id:f.id||'formulier',page_path:location.pathname,kanaal:SRC?SRC.kanaal:'Direct'});
    if(!kand&&typeof GA4!=='undefined'&&GA4&&window.gtag) gtag('event','generate_lead',{lead_type:'klant',form_id:f.id||'formulier',page_path:location.pathname,transport_type:'beacon'});
    const tel=g(['GSM','gsm','Telefoon','telefoon']), naam=g(['Naam','naam'])||(g(['voornaam'])+' '+g(['achternaam'])).trim();
    const p={source:'zondags-chat',type:kand?'Kandidaat via formulier':'Bedrijf via formulier',naam:naam,bedrijf:g(['Bedrijf','bedrijf']),statuut:g(['Statuut']),
      telefoon:tel,e_mail:g(['E-mail','email']),gemeente:g(['Gemeente','gemeente','Woonplaats','woonplaats']),wat:g(['Taken','waarvoor']),uren:g(['uren','Dagen per week','dagen']),
      iets_anders:g(['Iets anders']),vraag:g(['Bericht','bericht','motivatie']),pagina:location.href.split('#')[0],bron:SRC?SRC.bron:'Direct',kanaal:SRC?SRC.kanaal:'Direct',campagne:SRC?SRC.campagne:'',verwijzer:SRC?SRC.verwijzer:'',eerste_bezoek:SRC?SRC.datum:'',eerste_pagina:SRC?SRC.landing:'',
      tijdstip:new Date().toLocaleString('nl-BE',{timeZone:'Europe/Brussels'}),
      wa_link:tel?'https://wa.me/'+waNum(tel)+'?text='+encodeURIComponent('Hallo '+naam.split(' ')[0]+', met Mieke van Zondags. Bedankt voor je aanvraag via onze website.'):''};
    if(p.iets_anders&&p.wat==='Iets anders')p.wat='Iets anders: '+p.iets_anders;
    /* Sollicitaties: altijd naar Make (ook zonder telefoon), source=zondags-kandidaat: rij in de kandidatensheet + bevestigingsmail. Geen geboortedatum of andere gevoelige gegevens. */
    if(kand){
      const leeg=v=>/^(kies je statuut|maak een keuze|niets aangeduid)$/i.test(v)?'':v;
      const vn0=g(['voornaam']), an0=g(['achternaam']), nm=g(['Naam','naam']).replace(/\s+/g,' ');
      const vn=vn0||(nm?nm.split(' ')[0]:''), an=vn0?an0:(nm.indexOf(' ')>0?nm.slice(nm.indexOf(' ')+1):'');
      Object.assign(p,{source:'zondags-kandidaat',type:'Kandidaat via formulier',voornaam:vn,achternaam:an,naam:(vn+' '+an).trim(),
        statuut:leeg(g(['Statuut'])),uren:leeg(g(['Dagen per week','dagen'])),rijbewijs:leeg(g(['rijbewijs'])),vanaf:g(['vanaf']),
        doet_graag:leeg(g(['Doet graag'])),wat:leeg(g(['Doet graag'])),cv:(()=>{const c=fd.get('cv');return c&&c.name?'ja':'';})()});
    }
    if(LIVE&&(tel||kand)){try{const b=new URLSearchParams(p);if(!(navigator.sendBeacon&&navigator.sendBeacon(HOOK,b)))fetch(HOOK,{method:'POST',mode:'no-cors',keepalive:true,body:b});}catch(err){}}
  }));

  /* Chat-teaser (chat.js) nooit over een formulier: zolang een formulier in beeld is, krijgt <html> de klasse form-in-view en verbergt site.css de teaser */
  if('IntersectionObserver' in window){
    const forms=$$('form[action*="formsubmit"]'), vis=new Set();
    if(forms.length){
      const fio=new IntersectionObserver(es=>{es.forEach(x=>x.isIntersecting?vis.add(x.target):vis.delete(x.target));document.documentElement.classList.toggle('form-in-view',vis.size>0);},{rootMargin:'0px 0px 120px 0px'});
      forms.forEach(f=>fio.observe(f));
    }
  }

  /* Chat-teaser op desktop nooit over tekst: liggen er tekstregels, knoppen, velden of beelden onder de teaser (+16px marge),
     dan krijgt <html> de klasse teaser-over-tekst en verbergt site.css de teaser. Onder 560px is de teaser altijd weg (site.css). */
  (function(){
    const H=document.documentElement, PAD=16, BOX=/^(IMG|SVG|VIDEO|IFRAME|INPUT|TEXTAREA|SELECT|BUTTON|PICTURE|CANVAS)$/;
    const hit=(a,b)=>a.left<b.right&&a.right>b.left&&a.top<b.bottom&&a.bottom>b.top;
    function over(){
      const t=document.querySelector('.zc-teaser'); if(!t) return false;
      const r=t.getBoundingClientRect(); if(!r.width||!r.height) return false;
      const z={left:r.left-PAD,right:r.right+PAD,top:r.top-PAD,bottom:r.bottom+PAD}, seen=new Set();
      for(let i=0;i<=5;i++)for(let j=0;j<=4;j++){
        const x=Math.min(innerWidth-1,Math.max(0,z.left+(z.right-z.left)*i/5)), y=Math.min(innerHeight-1,Math.max(0,z.top+(z.bottom-z.top)*j/4));
        const e=(document.elementsFromPoint(x,y)||[]).find(n=>!n.closest('.zc')&&n!==H&&n!==document.body);
        if(!e||seen.has(e)) continue; seen.add(e);
        if(BOX.test(e.tagName.toUpperCase())){ if(hit(e.getBoundingClientRect(),z)) return true; continue; }
        const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT); let n,k=0;
        while((n=w.nextNode())&&k++<400){
          if(!n.nodeValue.trim()) continue;
          const p=n.parentElement; if(p&&p.closest('.zc')) continue;
          const g=document.createRange(); g.selectNodeContents(n);
          for(const q of g.getClientRects()) if(q.width&&hit(q,z)) return true;
        }
        const m=e.querySelectorAll('img,svg,input,textarea,select,button,video,iframe');
        for(let k2=0;k2<m.length&&k2<200;k2++) if(!m[k2].closest('.zc')&&hit(m[k2].getBoundingClientRect(),z)) return true;
      }
      return false;
    }
    let busy=false;
    const upd=()=>{ if(busy) return; busy=true; requestAnimationFrame(()=>{ busy=false; H.classList.toggle('teaser-over-tekst',over()); }); };
    addEventListener('scroll',upd,{passive:true}); addEventListener('resize',upd); addEventListener('load',upd);
    setInterval(upd,700); upd();
  })();

  /* Rustige beweging: secties schuiven 12px op en vagen in (600ms), niet bij "minder beweging" */
  if(reduce||!('IntersectionObserver' in window)) return;
  const els=$$('main section h2, main .lrow, main .aud__c, main .qa, main .next li, main .art__body > h2, main .pband, main .open, main .erv__item, main .card, main .steps .step');
  const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target);}}),{rootMargin:'0px 0px -8% 0px'});
  els.forEach(el=>{if(el.getBoundingClientRect().top>innerHeight){el.classList.add('fx');io.observe(el);}});
  /* Fallback: .fx wordt altijd zichtbaar, ook als de observer niet vuurt (afdrukken, schermopnames van de volledige pagina) */
  const showAll=()=>$$('.fx').forEach(el=>{el.classList.add('in');io.unobserve(el);});
  addEventListener('beforeprint',showAll);
  setTimeout(showAll,2500);
})();
