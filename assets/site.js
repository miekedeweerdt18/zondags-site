(function(){
  const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
  const LIVE=/(^|\.)zondags\.be$/.test(location.hostname);

  /* Paginaovergang */
  const cur=$('.curtain');
  if(cur){
    requestAnimationFrame(()=>cur.classList.add('out'));
    addEventListener('pageshow',e=>{if(e.persisted){cur.className='curtain out';}});
    $$('a[href]').forEach(a=>{
      const h=a.getAttribute('href');
      if(!h||h.startsWith('#')||h.startsWith('http')||h.startsWith('mailto')||h.startsWith('tel')||a.target==='_blank') return;
      a.addEventListener('click',e=>{
        if(e.metaKey||e.ctrlKey||e.shiftKey||reduce) return;
        e.preventDefault(); cur.className='curtain in'; cur.offsetHeight; cur.classList.add('go');
        setTimeout(()=>{location.href=h;},520);
      });
    });
  }

  /* Mobiel menu */
  const burger=$('.burger');
  if(burger) burger.addEventListener('click',()=>{const o=document.body.classList.toggle('menu-open');burger.setAttribute('aria-expanded',o);});

  /* Nav */
  const nav=$('#nav'); let lastY=0;
  addEventListener('scroll',()=>{const y=scrollY;nav.classList.toggle('is-scrolled',y>40);nav.classList.toggle('is-hidden',y>lastY&&y>400&&!document.body.classList.contains('menu-open'));lastY=y;},{passive:true});

  /* Draaiend woord */
  const inner=$('.rot__inner'), rot=$('#rot');
  if(inner){
    let idx=0; const n=inner.children.length-1;
    const size=()=>{rot.style.width=inner.children[idx%n].offsetWidth+'px';};
    addEventListener('load',size); setTimeout(size,300);
    if(!reduce) setInterval(()=>{
      idx++; inner.style.transform='translateY(-'+idx+'em)'; size();
      if(idx===n) setTimeout(()=>{inner.style.transition='none';idx=0;inner.style.transform='none';inner.offsetHeight;inner.style.transition='';size();},950);
    },2600);
  }

  /* Zon: foto's wisselen */
  const imgs=$$('#sunDisc img'), taskEl=$('#sunTask');
  const tasks=['Poetsen','Koken','De kinderen','Strijken','Tuin en buiten','Huiswerk begeleiden'];
  if(imgs.length&&!reduce){let s=0;setInterval(()=>{imgs[s].classList.remove('on');s=(s+1)%imgs.length;imgs[s].classList.add('on');if(taskEl)taskEl.textContent=tasks[s];},3200);}

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

  /* Aangevinkte keuzes samenvoegen tot één veld (leesbaar in de mail) */
  $$('form[action*="formsubmit"]').forEach(f=>f.addEventListener('submit',e=>{
    if(e.defaultPrevented) return;
    const groups={};
    f.querySelectorAll('input[type=checkbox][data-group]').forEach(c=>{(groups[c.dataset.group]=groups[c.dataset.group]||[]);if(c.checked)groups[c.dataset.group].push(c.value);});
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
  window.ZD_CONV=CONV;
  window.dataLayer=window.dataLayer||[];
  if(!window.gtag) window.gtag=function(){window.dataLayer.push(arguments);};
  if(LIVE){
    const grant={ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted',analytics_storage:'granted'};
    let ok=null; try{ok=localStorage.getItem('zd_consent');}catch(e){}
    gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',wait_for_update:400});
    if(ok==='ja') gtag('consent','update',grant);
    gtag('js',new Date()); gtag('config',AW);
    const gs=document.createElement('script'); gs.async=true; gs.src='https://www.googletagmanager.com/gtag/js?id='+AW; document.head.appendChild(gs);
    if(/^\/bedankt(\.html)?\/?$/.test(location.pathname)){
      let done=null; try{done=sessionStorage.getItem('zd_conv');}catch(e){}
      if(!done){gtag('event','conversion',{send_to:CONV});try{sessionStorage.setItem('zd_conv','1');}catch(e){}}
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
    const subj=g(['_subject']), kand=/kandidaat/i.test(subj)||!!f.querySelector('[name="Statuut"]');
    const tel=g(['GSM','gsm','Telefoon','telefoon']), naam=g(['Naam','naam'])||(g(['voornaam'])+' '+g(['achternaam'])).trim();
    const p={source:'zondags-chat',type:kand?'Kandidaat via formulier':'Bedrijf via formulier',naam:naam,bedrijf:g(['Bedrijf','bedrijf']),statuut:g(['Statuut']),
      telefoon:tel,e_mail:g(['E-mail','email']),gemeente:g(['Gemeente','gemeente','Woonplaats','woonplaats']),wat:g(['Taken','waarvoor']),uren:g(['uren','Dagen per week','dagen']),
      vraag:g(['Bericht','bericht','motivatie']),pagina:location.href.split('#')[0],bron:SRC?SRC.bron:'Direct',kanaal:SRC?SRC.kanaal:'Direct',campagne:SRC?SRC.campagne:'',verwijzer:SRC?SRC.verwijzer:'',eerste_bezoek:SRC?SRC.datum:'',eerste_pagina:SRC?SRC.landing:'',
      tijdstip:new Date().toLocaleString('nl-BE',{timeZone:'Europe/Brussels'}),
      wa_link:tel?'https://wa.me/'+waNum(tel)+'?text='+encodeURIComponent('Hallo '+naam.split(' ')[0]+', met Mieke van Zondags. Bedankt voor je aanvraag via onze website.'):''};
    if(LIVE&&tel){try{const b=new URLSearchParams(p);if(!(navigator.sendBeacon&&navigator.sendBeacon(HOOK,b)))fetch(HOOK,{method:'POST',mode:'no-cors',keepalive:true,body:b});}catch(err){}}
  }));

  if(reduce||!window.gsap) return;
  gsap.registerPlugin(ScrollTrigger);

  /* Vloeiend scrollen */
  if(window.Lenis){
    const lenis=new Lenis({lerp:.1,smoothWheel:true});
    lenis.on('scroll',()=>ScrollTrigger.update());
    gsap.ticker.add(t=>lenis.raf(t*1000)); gsap.ticker.lagSmoothing(0);
    $$('a[href^="#"]').forEach(a=>a.addEventListener('click',e=>{const t=document.querySelector(a.getAttribute('href'));if(t){e.preventDefault();lenis.scrollTo(t,{offset:-70});}}));
  }

  /* Titels: letters rijzen op */
  $$('[data-split] .line').forEach(line=>{
    if(line.querySelector('.rot')) return;
    if(line.querySelector('em')){line.innerHTML='<span class="ch">'+line.innerHTML+'</span>';return;}
    line.innerHTML=line.textContent.trim().split(/\s+/).map(w=>'<span class="wd">'+w.split('').map(c=>'<span class="ch">'+c+'</span>').join('')+'</span>').join(' ');
  });
  if($('[data-split]')){
    gsap.from('[data-split] .ch',{yPercent:115,rotate:6,duration:1.1,ease:'expo.out',stagger:.022,delay:.35});
    if($('.hero .rot')) gsap.from('.hero .rot',{yPercent:115,duration:1.1,ease:'expo.out',delay:.8});
    gsap.from('.hero__lead,.hero__ctas,.hero__note,.phero p',{y:24,opacity:0,duration:1,ease:'expo.out',stagger:.08,delay:.9});
  }
  if($('.bento')) gsap.from('.bento .bt',{y:50,scale:.94,opacity:0,duration:1.2,ease:'expo.out',stagger:.08,delay:.3});
  if($('.sun')) gsap.from('.sun',{scale:.9,opacity:.2,duration:1.6,ease:'expo.out',delay:.4});

  /* Opening: cirkel wordt volledig beeld */
  if($('#open')) gsap.timeline({scrollTrigger:{trigger:'#open',start:'top top',end:'+=130%',pin:true,scrub:1}})
    .fromTo('#openImg',{clipPath:'circle(16% at 50% 50%)'},{clipPath:'circle(75% at 50% 50%)',ease:'none'},0)
    .fromTo('#openImg img',{scale:1.35},{scale:1,ease:'none'},0)
    .from('.open__txt',{y:60,opacity:0,ease:'none',duration:.35},.55);

  /* Statement: woorden lichten op */
  const st=$('#statement');
  if(st){
    const out=[];
    st.childNodes.forEach(n=>{
      if(n.nodeType===3) n.textContent.split(/(\s+)/).forEach(t=>out.push(/^\s+$/.test(t)||!t?t:'<span class="w">'+t+'</span>'));
      else out.push('<span class="w" data-hl>'+n.textContent+'</span>');
    });
    st.innerHTML=out.join('');
    const ws=$$('#statement .w');
    ScrollTrigger.create({trigger:st,start:'top 80%',end:'bottom 45%',scrub:true,onUpdate:self=>{
      const k=Math.round(self.progress*ws.length);
      ws.forEach((w,i)=>{w.style.opacity=i<k?1:.16;w.classList.toggle('hl',i<k&&w.hasAttribute('data-hl'));});
    }});
  }

  /* Knoppen: licht magnetisch */
  if(fine) $$('.btn').forEach(b=>{
    b.addEventListener('mousemove',e=>{const r=b.getBoundingClientRect();gsap.to(b,{x:(e.clientX-r.left-r.width/2)*.25,y:(e.clientY-r.top-r.height/2)*.35,duration:.4,ease:'power3.out'});});
    b.addEventListener('mouseleave',()=>gsap.to(b,{x:0,y:0,duration:.7,ease:'elastic.out(1,.4)'}));
  });

  /* Koppen schuiven in */
  $$('main section:not(.open):not(.hero):not(.phero) h2').forEach(h=>gsap.from(h,{y:70,opacity:.2,duration:1.1,ease:'expo.out',scrollTrigger:{trigger:h,start:'top 88%'}}));
  $$('.lrow').forEach((r,i)=>gsap.from(r,{y:40,opacity:.2,duration:1,ease:'expo.out',scrollTrigger:{trigger:r,start:'top 92%'}}));

  /* Diensten horizontaal (desktop) */
  const track=$('#track');
  if(track) gsap.matchMedia().add('(min-width: 901px)',()=>{
    const dist=()=>track.scrollWidth-innerWidth, total=track.children.length-1;
    gsap.to(track,{x:()=>-dist(),ease:'none',scrollTrigger:{trigger:'.svc__pin',start:'center center',end:()=>'+='+dist(),pin:'.svc__pin',scrub:1,invalidateOnRefresh:true,
      onUpdate:self=>{const bar=$('#svcBar'),n=$('#svcN');if(bar)bar.style.setProperty('--p',self.progress);if(n)n.textContent=String(Math.min(total,1+Math.floor(self.progress*total))).padStart(2,'0');}}});
  });

  /* Parallax */
  $$('.collage img').forEach((im,i)=>gsap.to(im,{yPercent:-12*(i+1),ease:'none',scrollTrigger:{trigger:'.collage',scrub:true}}));
  if($('#jobImg')) gsap.to('#jobImg',{yPercent:-10,ease:'none',scrollTrigger:{trigger:'.job',scrub:true}});

  /* Stappen */
  $$('.step').forEach(s=>gsap.fromTo(s.querySelector('.step__bar'),{scaleX:0},{scaleX:1,ease:'none',scrollTrigger:{trigger:s,start:'top 85%',end:'top 45%',scrub:true}}));

  /* Footer: zonsopgang */
  gsap.from('.foot__logo',{yPercent:40,ease:'none',scrollTrigger:{trigger:'.foot',start:'top bottom',end:'bottom bottom',scrub:true}});
  gsap.fromTo('.foot__sun',{yPercent:40,opacity:.15},{yPercent:-8,opacity:.6,ease:'none',scrollTrigger:{trigger:'.foot',start:'top bottom',end:'bottom bottom',scrub:true}});

  /* Marquee helt mee */
  if($('.marquee__track')){const sk=gsap.quickTo('.marquee__track','skewX',{duration:.5,ease:'power3'});ScrollTrigger.create({onUpdate:self=>sk(gsap.utils.clamp(-8,8,self.getVelocity()/-250))});}

  addEventListener('load',()=>ScrollTrigger.refresh());
})();
