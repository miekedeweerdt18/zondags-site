/* Boekingsbuilder zondags.be: 1 pakket, 60 euro per uur excl. btw, per blok van 3 uur + extra uren. Betaling via Stripe Payment Links. */
(function(){
  const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
  const form=$('#bookForm'); if(!form) return;
  const LIVE=/(^|\.)zondags\.be$/.test(location.hostname);
  const PRICE_H=60, BLOCK_H=3, VAT=0.21, MAX_H=24;
  /* Stripe Payment Links per totaal aantal uren (3 tot 24). Wordt ingevuld door _tools/stripe_links.json bij de bouw. */
  const PAY={};
  const HOOK='https://hook.eu2.make.com/kxqukx7dzzc666hvuefito1g4uytlvad';
  const st={blokken:1,extra:0};
  const eur=n=>n.toLocaleString('nl-BE',{minimumFractionDigits:2,maximumFractionDigits:2})+' euro';
  const hours=()=>st.blokken*BLOCK_H+st.extra;

  function render(){
    const h=hours(), ex=h*PRICE_H, btw=ex*VAT;
    $('#o-blokken').textContent=st.blokken; $('#o-extra').textContent=st.extra;
    $('#t-uren').textContent=h+' uur ('+st.blokken+(st.blokken===1?' blok':' blokken')+(st.extra?' + '+st.extra+' extra':'')+')';
    $('#t-ex').textContent=eur(ex); $('#t-btw').textContent=eur(btw); $('#t-tot').textContent=eur(ex+btw);
    $$('[data-step]').forEach(b=>{
      const k=b.dataset.step, d=+b.dataset.d, v=st[k]+d;
      const min=k==='blokken'?1:0, over=(k==='blokken'?(v*BLOCK_H+st.extra):(st.blokken*BLOCK_H+v))>MAX_H;
      b.disabled=v<min||over;
    });
  }
  $$('[data-step]').forEach(b=>b.addEventListener('click',()=>{
    const k=b.dataset.step, v=st[k]+(+b.dataset.d), min=k==='blokken'?1:0;
    const next=Object.assign({},st,{[k]:v});
    if(v<min||next.blokken*BLOCK_H+next.extra>MAX_H) return;
    st[k]=v; render();
  }));
  render();

  /* Datum: enkel weekdagen, minstens 2 werkdagen vooruit */
  const dEl=$('#b-datum');
  function addWork(d,n){const x=new Date(d);while(n>0){x.setDate(x.getDate()+1);const w=x.getDay();if(w!==0&&w!==6)n--;}return x;}
  const iso=d=>d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
  const minD=addWork(new Date(),2); dEl.min=iso(minD);
  const dateOk=v=>{if(!v) return false;const d=new Date(v+'T12:00:00');return d>=new Date(iso(minD)+'T00:00:00')&&d.getDay()!==0&&d.getDay()!==6;};

  const checks=[
    ['b-datum','e-datum',dateOk],
    ['b-adres','e-adres',v=>v.trim().length>5],
    ['b-bedrijf','e-bedrijf',v=>v.trim().length>1],
    ['b-btw','e-btw',v=>v.replace(/[^0-9]/g,'').length>=9],
    ['b-naam','e-bnaam',v=>v.trim().length>1],
    ['b-gsm','e-bgsm',v=>v.replace(/\D/g,'').length>=9],
    ['b-mail','e-bmail',v=>/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)]
  ];
  const waNum=v=>{let d=String(v).replace(/[^0-9+]/g,'');if(d.indexOf('+')===0)return d.slice(1);if(d.indexOf('00')===0)return d.slice(2);if(d.indexOf('0')===0)return '32'+d.slice(1);return d;};

  form.addEventListener('submit',function(e){
    e.preventDefault(); e.stopImmediatePropagation();
    let first=null;
    checks.forEach(([i,er,ok])=>{const el=document.getElementById(i), bad=!ok(el.value);el.setAttribute('aria-invalid',bad);document.getElementById(er).hidden=!bad;if(bad&&!first)first=el;});
    const okBox=$('#b-ok'); $('#e-ok').hidden=okBox.checked; if(!okBox.checked&&!first) first=okBox;
    if(first){first.focus();return;}

    const g=id=>document.getElementById(id).value.trim();
    const taken=$$('input[data-group="Taken"]:checked').map(c=>c.value).join(', ')||'niets aangeduid';
    const h=hours(), ex=h*PRICE_H, btw=ex*VAT, tot=ex+btw;
    const val=n=>{const r=form.querySelector('input[name="'+n+'"]:checked');return r?r.value:'';};
    const SRC=window.ZD_SRC||null;
    const ref='ZD-'+Date.now().toString(36).toUpperCase();
    const data={
      Referentie:ref, Uren:h+' uur ('+st.blokken+' x 3 uur + '+st.extra+' extra)', 'Bedrag excl. btw':eur(ex), 'Bedrag incl. btw':eur(tot),
      Datum:g('b-datum'), Moment:g('b-moment'), Frequentie:val('frequentie'), Waar:val('waar'), Taken:taken, Adres:g('b-adres'),
      Bedrijf:g('b-bedrijf'), 'Btw-nummer':g('b-btw'), Naam:g('b-naam'), GSM:g('b-gsm'), 'E-mail':g('b-mail'), Bericht:g('b-msg'),
      Bron:SRC?SRC.bron:'Direct', Kanaal:SRC?SRC.kanaal:'Direct', 'Eerste pagina':SRC?SRC.landing:'',
      Betaling:PAY[h]?'Doorgestuurd naar Stripe, bevestiging volgt van Stripe':'Nog geen betaallink: betaallink manueel sturen',
      _subject:'Nieuwe boeking via zondags.be ('+h+' uur)', _template:'table', _captcha:'false'
    };
    const go=$('#b-go'); go.disabled=true; go.firstChild.textContent='Even geduld ';

    const tasks=[];
    if(LIVE){
      tasks.push(fetch('https://formsubmit.co/ajax/mieke@hummingbirds.be',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(data),keepalive:true}).catch(()=>{}));
      try{
        const p={source:'zondags-chat',type:'Boeking via site ('+h+' uur)',naam:data.Naam,bedrijf:data.Bedrijf,statuut:'',telefoon:data.GSM,e_mail:data['E-mail'],gemeente:data.Adres,wat:taken,uren:data.Uren+', '+data['Bedrag excl. btw']+' excl. btw',
          vraag:'Datum '+data.Datum+' ('+data.Moment+'), '+data.Frequentie+', '+data.Waar+'. '+data.Bericht,pagina:location.href.split('#')[0],bron:data.Bron,kanaal:data.Kanaal,campagne:SRC?SRC.campagne:'',verwijzer:SRC?SRC.verwijzer:'',eerste_bezoek:SRC?SRC.datum:'',eerste_pagina:data['Eerste pagina'],
          tijdstip:new Date().toLocaleString('nl-BE',{timeZone:'Europe/Brussels'}),wa_link:'https://wa.me/'+waNum(data.GSM)+'?text='+encodeURIComponent('Hallo '+data.Naam.split(' ')[0]+', met Mieke van Zondags. Bedankt voor je boeking van '+h+' uur.')};
        const b=new URLSearchParams(p);
        if(!(navigator.sendBeacon&&navigator.sendBeacon(HOOK,b))) fetch(HOOK,{method:'POST',mode:'no-cors',keepalive:true,body:b});
      }catch(err){}
    }
    try{sessionStorage.setItem('zd_boeking',JSON.stringify({ref:ref,uren:h,excl:ex,incl:tot}));}catch(err){}

    const finish=()=>{
      const url=PAY[h];
      if(LIVE&&url){
        const u=new URL(url); u.searchParams.set('prefilled_email',data['E-mail']); u.searchParams.set('client_reference_id',ref.replace(/[^A-Za-z0-9_-]/g,''));
        location.href=u.toString();
      }else{
        $('#bookFields').hidden=true; const t=$('#bookThanks'); t.hidden=false; t.focus();
      }
    };
    Promise.race([Promise.all(tasks),new Promise(r=>setTimeout(r,2500))]).then(finish,finish);
  },true);
})();
