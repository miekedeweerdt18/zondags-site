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
