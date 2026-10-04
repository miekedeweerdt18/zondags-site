/* Zondags chat: aanmelden voor bedrijven en kandidaten, meldingen naar WhatsApp en mail. */
(function () {
  'use strict';
  if (window.ZondagsChat) return;

  var WA = '32470565358';
  var HOOK = 'https://hook.eu2.make.com/kxqukx7dzzc666hvuefito1g4uytlvad';
  var MAIL = 'https://formsubmit.co/ajax/mieke@hummingbirds.be';
  var path = location.pathname;
  var isJobPage = /\/(jobs|zondag-worden|studentenjob|flexi|werken)/.test(path);
  var quiet = /\/(bedankt|aanvraag)/.test(path);

  function store(k, v) { try { if (v === undefined) return sessionStorage.getItem(k); sessionStorage.setItem(k, v); } catch (e) { return null; } }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function el(tag, cls, html) { var n = document.createElement(tag); if (cls) n.className = cls; if (html != null) n.innerHTML = html; return n; }

  var css = '' +
  '.zc,.zc *{box-sizing:border-box}' +
  '.zc{--zi:#17221E;--zp:#F6F2EB;--zg:#E9BE55;--zs:#EAE2D5;--zm:#6A6A5E;font-family:"Geist","Helvetica Neue",Arial,sans-serif;color:var(--zi);-webkit-font-smoothing:antialiased}' +
  '.zc-launch{position:fixed;right:20px;bottom:calc(20px + env(safe-area-inset-bottom,0px));z-index:60;width:60px;height:60px;border-radius:50%;border:0;background:var(--zi);color:var(--zp);display:grid;place-items:center;cursor:pointer;box-shadow:0 12px 30px rgba(23,34,30,.28);transition:transform .35s cubic-bezier(.22,1,.36,1)}' +
  '.zc-launch:hover{transform:scale(1.06)}.zc-launch:focus-visible{outline:3px solid var(--zg);outline-offset:3px}' +
  '.zc-launch svg{width:28px;height:28px}.zc-launch .zc-dot{position:absolute;top:9px;right:9px;width:12px;height:12px;border-radius:50%;background:var(--zg);box-shadow:0 0 0 3px var(--zi)}' +
  '.zc-launch::after{content:"";position:absolute;inset:0;border-radius:50%;box-shadow:0 0 0 0 rgba(233,190,85,.6);animation:zcPulse 2.4s 1.2s 3}' +
  '@keyframes zcPulse{0%{box-shadow:0 0 0 0 rgba(233,190,85,.55)}100%{box-shadow:0 0 0 18px rgba(233,190,85,0)}}' +
  '.zc-teaser{position:fixed;right:20px;bottom:calc(92px + env(safe-area-inset-bottom,0px));z-index:59;display:flex;flex-direction:column;align-items:flex-end;gap:10px;max-width:min(340px,calc(100vw - 40px));opacity:0;transform:translateY(12px);pointer-events:none;transition:opacity .5s cubic-bezier(.22,1,.36,1),transform .5s cubic-bezier(.22,1,.36,1)}' +
  '.zc-teaser.is-on{opacity:1;transform:none;pointer-events:auto}' +
  '.zc-pill{display:flex;align-items:center;gap:12px;width:100%;text-align:left;border:0;cursor:pointer;border-radius:18px;padding:13px 14px 13px 18px;font:inherit;font-size:14.5px;line-height:1.3;box-shadow:0 10px 28px rgba(23,34,30,.18);transition:transform .3s cubic-bezier(.22,1,.36,1)}' +
  '.zc-pill:hover{transform:translateX(-4px)}.zc-pill:focus-visible{outline:3px solid var(--zg);outline-offset:2px}' +
  '.zc-pill b{display:block;font-family:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif;font-weight:700;font-size:16px;letter-spacing:-.01em;margin-top:2px}' +
  '.zc-pill span.zc-t{flex:1}.zc-pill i{flex:none;width:34px;height:34px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-size:18px}' +
  '.zc-pill--b{background:var(--zi);color:var(--zp)}.zc-pill--b i{background:var(--zg);color:var(--zi)}' +
  '.zc-pill--w{background:var(--zg);color:var(--zi)}.zc-pill--w i{background:var(--zi);color:var(--zg)}' +
  '.zc-arrow{width:64px;height:40px;margin-right:6px;color:var(--zi);opacity:.85}' +
  '.zc-x{position:absolute;top:-12px;left:-12px;width:28px;height:28px;border-radius:50%;border:0;background:var(--zp);color:var(--zi);box-shadow:0 4px 12px rgba(23,34,30,.2);cursor:pointer;font-size:16px;line-height:28px}' +
  '.zc-panel{position:fixed;right:20px;bottom:calc(92px + env(safe-area-inset-bottom,0px));z-index:61;width:min(390px,calc(100vw - 40px));height:min(620px,calc(100vh - 120px));background:var(--zp);border-radius:22px;box-shadow:0 24px 60px rgba(23,34,30,.32);display:flex;flex-direction:column;overflow:hidden;opacity:0;transform:translateY(16px) scale(.98);transform-origin:bottom right;pointer-events:none;transition:opacity .35s cubic-bezier(.22,1,.36,1),transform .35s cubic-bezier(.22,1,.36,1)}' +
  '.zc-panel.is-open{opacity:1;transform:none;pointer-events:auto}' +
  '.zc-head{background:var(--zi);color:var(--zp);padding:18px 18px 16px 20px;display:flex;align-items:center;gap:12px}' +
  '.zc-sun{width:38px;height:38px;border-radius:50%;background:var(--zg);flex:none;display:grid;place-items:center;color:var(--zi);font-family:"Bricolage Grotesque",Arial,sans-serif;font-weight:800;font-size:18px}' +
  '.zc-head h2{margin:0;font-family:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif;font-size:19px;font-weight:700;letter-spacing:-.01em;color:var(--zp)}' +
  '.zc-head p{margin:2px 0 0;font-size:12.5px;opacity:.75}' +
  '.zc-close{margin-left:auto;width:36px;height:36px;border-radius:50%;border:0;background:rgba(246,242,235,.12);color:var(--zp);cursor:pointer;font-size:20px;line-height:36px}' +
  '.zc-close:focus-visible{outline:2px solid var(--zg)}' +
  '.zc-body{flex:1;overflow-y:auto;padding:18px 16px 8px;display:flex;flex-direction:column;gap:8px;overscroll-behavior:contain}' +
  '.zc-msg{max-width:86%;padding:11px 14px;border-radius:16px;font-size:14.5px;line-height:1.45;white-space:pre-line;animation:zcIn .35s cubic-bezier(.22,1,.36,1)}' +
  '@keyframes zcIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}' +
  '.zc-bot{background:#fff;border:1px solid rgba(23,34,30,.08);border-bottom-left-radius:5px;align-self:flex-start}' +
  '.zc-me{background:var(--zi);color:var(--zp);border-bottom-right-radius:5px;align-self:flex-end}' +
  '.zc-msg a{color:inherit;font-weight:600}' +
  '.zc-typing{align-self:flex-start;background:#fff;border:1px solid rgba(23,34,30,.08);border-radius:16px;padding:12px 14px;display:flex;gap:4px}' +
  '.zc-typing span{width:6px;height:6px;border-radius:50%;background:var(--zm);animation:zcDot 1s infinite}.zc-typing span:nth-child(2){animation-delay:.15s}.zc-typing span:nth-child(3){animation-delay:.3s}' +
  '@keyframes zcDot{0%,60%,100%{opacity:.25}30%{opacity:1}}' +
  '.zc-chips{display:flex;flex-wrap:wrap;gap:7px;padding:4px 0 6px;align-self:stretch}' +
  '.zc-chip{border:1.5px solid var(--zi);background:transparent;color:var(--zi);border-radius:999px;padding:8px 13px;font:inherit;font-size:13.5px;cursor:pointer;transition:background .2s,color .2s}' +
  '.zc-chip:hover{background:var(--zs)}.zc-chip[aria-pressed="true"]{background:var(--zi);color:var(--zp)}' +
  '.zc-chip--go{background:var(--zg);border-color:var(--zg);font-weight:600}.zc-chip--go:hover{background:#dfb043}' +
  '.zc-chip--wa{background:#1f7a4c;border-color:#1f7a4c;color:#fff;font-weight:600}.zc-chip--wa:hover{background:#18653e}' +
  '.zc-chip:focus-visible{outline:3px solid var(--zg);outline-offset:2px}' +
  '.zc-foot{border-top:1px solid rgba(23,34,30,.1);padding:10px 12px 12px;background:var(--zp)}' +
  '.zc-form{display:flex;gap:8px}' +
  '.zc-in{flex:1;min-width:0;border:1.5px solid rgba(23,34,30,.18);background:#fff;border-radius:999px;padding:11px 16px;font:inherit;font-size:16px;color:var(--zi)}' +
  '.zc-in:focus{outline:none;border-color:var(--zi)}' +
  '.zc-send{flex:none;width:44px;height:44px;border-radius:50%;border:0;background:var(--zi);color:var(--zg);cursor:pointer;font-size:18px}' +
  '.zc-send:focus-visible{outline:3px solid var(--zg);outline-offset:2px}' +
  '.zc-note{margin:8px 4px 0;font-size:11.5px;color:var(--zm)}.zc-note a{color:var(--zm)}' +
  '.zc-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}' +
  '@media (max-width:560px){' +
  '.zc-launch{right:16px;width:56px;height:56px}' +
  '.zc-teaser{right:16px;bottom:calc(84px + env(safe-area-inset-bottom,0px));max-width:calc(100vw - 32px);gap:8px}' +
  '.zc-pill{font-size:13.5px;padding:10px 10px 10px 14px;border-radius:16px}.zc-pill b{font-size:15px}.zc-pill i{width:30px;height:30px}' +
  '.zc-arrow{display:none}' +
  '.zc-panel{right:0;left:0;bottom:0;width:100%;height:calc(100% - 40px);height:calc(100dvh - 40px);border-radius:22px 22px 0 0}' +
  '}' +
  '@media (prefers-reduced-motion:reduce){.zc *,.zc-launch::after{animation:none!important;transition:none!important}}';

  var st = el('style'); st.textContent = css; document.head.appendChild(st);

  var root = el('div', 'zc');
  root.setAttribute('data-lenis-prevent', '');
  document.body.appendChild(root);

  /* ---------- teaser met twee pijlen ---------- */
  var teaser = el('div', 'zc-teaser');
  teaser.setAttribute('role', 'complementary');
  teaser.setAttribute('aria-label', 'Aanmelden bij Zondags');
  var pB = '<button type="button" class="zc-pill zc-pill--b" data-flow="hulp"><span class="zc-t">Bedrijf en hulp nodig?<b>Meld je aan</b></span><i aria-hidden="true">&rarr;</i></button>';
  var pW = '<button type="button" class="zc-pill zc-pill--w" data-flow="werk"><span class="zc-t">Student, flexi of vast en op zoek naar werk?<b>Meld je aan</b></span><i aria-hidden="true">&rarr;</i></button>';
  teaser.innerHTML = '<button type="button" class="zc-x" aria-label="Verberg">&times;</button>' + (isJobPage ? pW + pB : pB + pW) +
    '<svg class="zc-arrow" viewBox="0 0 64 40" fill="none" aria-hidden="true"><path d="M4 6c18 2 34 10 44 26" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><path d="M38 30l10 3 2-10" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  root.appendChild(teaser);

  /* ---------- launcher ---------- */
  var launch = el('button', 'zc-launch');
  launch.type = 'button';
  launch.setAttribute('aria-label', 'Open de chat van Zondags');
  launch.setAttribute('aria-expanded', 'false');
  launch.innerHTML = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v8a2.5 2.5 0 0 1-2.5 2.5H10l-4.2 3.6c-.5.4-1.3 0-1.3-.6V16A2.5 2.5 0 0 1 4 13.5v-8z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M8.5 9.5h7M8.5 12.5h4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg><span class="zc-dot" aria-hidden="true"></span>';
  root.appendChild(launch);

  /* ---------- paneel ---------- */
  var panel = el('div', 'zc-panel');
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-modal', 'false');
  panel.setAttribute('aria-label', 'Chat met Zondags');
  panel.innerHTML =
    '<div class="zc-head"><div class="zc-sun" aria-hidden="true">z</div><div><h2>Zondags</h2><p>Elke dag een beetje zondag</p></div><button type="button" class="zc-close" aria-label="Sluit de chat">&times;</button></div>' +
    '<div class="zc-body" aria-live="polite"></div>' +
    '<div class="zc-foot"><form class="zc-form" novalidate><label class="zc-sr" for="zcIn">Typ je bericht</label><input id="zcIn" class="zc-in" autocomplete="off" placeholder="Typ je bericht"><button class="zc-send" type="submit" aria-label="Verstuur">&rarr;</button></form>' +
    '<p class="zc-note">Liever bellen of WhatsApp? <a href="https://wa.me/' + WA + '">0470 56 53 58</a>, elke dag van 6 tot 22 uur.</p></div>';
  root.appendChild(panel);

  var body = panel.querySelector('.zc-body');
  var form = panel.querySelector('.zc-form');
  var input = panel.querySelector('.zc-in');
  var data = {}, step = null, flow = null, started = false, busy = false;

  function scroll() { body.scrollTop = body.scrollHeight; }
  function me(t) { var m = el('div', 'zc-msg zc-me'); m.textContent = t; body.appendChild(m); scroll(); }
  function clearChips() { var c = body.querySelectorAll('.zc-chips'); for (var i = 0; i < c.length; i++) c[i].remove(); }
  function say(lines, then) {
    lines = [].concat(lines); busy = true;
    var t = el('div', 'zc-typing', '<span></span><span></span><span></span>');
    body.appendChild(t); scroll();
    var i = 0;
    (function next() {
      setTimeout(function () {
        var m = el('div', 'zc-msg zc-bot', lines[i]); body.insertBefore(m, t); scroll();
        i++;
        if (i < lines.length) next(); else { t.remove(); busy = false; if (then) then(); scroll(); }
      }, Math.min(900, 350 + lines[i].length * 6));
    })();
  }
  function chips(list, opts) {
    opts = opts || {};
    var box = el('div', 'zc-chips'); var picked = [];
    list.forEach(function (c) {
      var label = typeof c === 'string' ? c : c.label;
      var b = el('button', 'zc-chip' + (c.cls ? ' ' + c.cls : ''), esc(label)); b.type = 'button';
      if (opts.multi && !c.action) b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', function () {
        if (c.href) { window.open(c.href, '_blank', 'noopener'); return; }
        if (opts.multi && !c.action) {
          var on = b.getAttribute('aria-pressed') !== 'true'; b.setAttribute('aria-pressed', on ? 'true' : 'false');
          if (on) picked.push(label); else picked = picked.filter(function (x) { return x !== label; });
          return;
        }
        if (c.action === 'done') {
          if (!picked.length) { b.textContent = 'Kies eerst iets'; setTimeout(function () { b.textContent = label; }, 1200); return; }
          box.remove(); me(picked.join(', ')); opts.onPick(picked.slice()); return;
        }
        box.remove(); me(label); (c.go || opts.onPick)(label);
      });
      box.appendChild(b);
    });
    body.appendChild(box); scroll();
  }
  function ask(key, q, opts) {
    opts = opts || {}; step = { key: key, opts: opts };
    input.type = opts.type || 'text';
    input.setAttribute('inputmode', opts.inputmode || 'text');
    input.setAttribute('autocomplete', opts.ac || 'off');
    input.placeholder = opts.ph || 'Typ je antwoord';
    say(q, function () {
      if (opts.skip) chips([{ label: 'Sla over', go: function () { resetInput(); opts.next(''); } }]);
      if (window.matchMedia('(min-width:561px)').matches) input.focus();
    });
  }
  function resetInput() { step = null; input.type = 'text'; input.placeholder = 'Typ je bericht'; input.setAttribute('inputmode', 'text'); }

  function validPhone(v) { return v.replace(/[^0-9]/g, '').length >= 9; }
  function validMail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v); }
  function waNum(v) { var d = v.replace(/[^0-9+]/g, ''); if (d.indexOf('+') === 0) return d.slice(1); if (d.indexOf('00') === 0) return d.slice(2); if (d.indexOf('0') === 0) return '32' + d.slice(1); return d; }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = input.value.trim(); if (!v || busy) return;
    input.value = '';
    if (step) {
      var s = step;
      if (s.opts.validate && !s.opts.validate(v)) { me(v); say(s.opts.err); return; }
      clearChips(); me(v); resetInput(); data[s.key] = v; s.opts.next(v); return;
    }
    clearChips(); me(v); answer(v);
  });

  /* ---------- kennisbank ---------- */
  var KB = [
    { k: /prijs|kost|tarief|euro|duur|betalen per uur|uurprijs|offerte/i, a: 'Dat hangt af van het aantal uren en wat je nodig hebt. Na een kort gesprek krijg je een voorstel op maat. De eerste 2 uur zijn gratis, om kennis te maken.', cta: 'hulp' },
    { k: /vennootschap|factuur|aftrek|fiscaal|btw|boekhoud|accountant|voordeel van alle aard|vaa/i, a: 'Zondags werkt met een gewone dienstenfactuur op naam van je vennootschap, voor je kantoor of praktijk en voor je woning. Een vennootschap kan geen dienstencheques kopen. Voor het privégedeelte geldt een voordeel van alle aard. Laat je accountant dit bevestigen voor je eigen situatie.', cta: 'hulp' },
    { k: /dienstencheque|particulier|prive persoon|privé persoon/i, a: 'Zondags werkt niet met dienstencheques. We werken voor ondernemers, zaakvoerders, vrije beroepen en bedrijven, met een factuur op naam van de vennootschap. Je woning kan daar ook bij.', cta: 'hulp' },
    { k: /regio|gemeente|waar|stad|kortrijk|roeselare|waregem|gent|brugge|ieper|oost-vlaanderen|west-vlaanderen/i, a: 'We werken in West- en Oost-Vlaanderen, vanuit Marke bij Kortrijk. Onder meer in Kortrijk, Waregem, Harelbeke, Roeselare, Izegem, Menen, Wevelgem, Ieper, Tielt en Oudenaarde. Twijfel je over jouw gemeente? Laat ze achter, dan kijken we het na.' },
    { k: /dezelfde|vaste persoon|wisselend|vervang|ziek|verlof/i, a: 'Ja, steeds dezelfde Zondag, op dezelfde dag, op hetzelfde uur. Bij verlof of ziekte zoeken wij een oplossing. Jij hoeft niets te regelen.' },
    { k: /loon|verdien|uurloon|barema|betaald|salaris|vergoed/i, a: 'Beter dan het barema, met vergoede verplaatsingen en alles in orde op papier. Het precieze loon hangt af van je statuut en je uren. Dat bespreken we in het eerste gesprek.', cta: 'werk' },
    { k: /student|flexi|bijverdien|bijjob|statuut|weekend|avond|uren|flexibel/i, a: 'Studenten vanaf 18 jaar zijn welkom, net als wie wil bijverdienen naast een job of een vast contract zoekt. Je kiest mee je dagen, overdag en zonder weekends. Je statuut bekijken we samen.', cta: 'werk' },
    { k: /poets|kook|koken|boodschap|strijk|was|tuin|kinder|school|kantoor|praktijk|hond|maaltijd|eten/i, a: 'Een Zondag poetst, doet de was en de strijk, kookt en doet boodschappen, haalt de kinderen op, houdt de tuin bij en onderhoudt je kantoor of praktijk. Alles in één vast plan, met één vaste persoon.', cta: 'hulp' },
    { k: /start|wanneer|hoe snel|beginnen|intake/i, a: 'Na je aanmelding bellen we je binnen één werkdag. Daarna komen we langs voor de intake en leggen we samen je zondagsplan vast. Vanaf dan komt elke week dezelfde Zondag.', cta: 'hulp' },
    { k: /opzeg|contract|abonnement|extra uren/i, a: 'Je abonnement is maandelijks opzegbaar. Extra uren bijboeken kan altijd en ze vervallen niet.', cta: 'hulp' }
  ];
  function answer(v) {
    var hit = null; for (var i = 0; i < KB.length; i++) if (KB[i].k.test(v)) { hit = KB[i]; break; }
    if (hit) {
      say(hit.a, function () {
        var list = [];
        if (hit.cta === 'hulp') list.push({ label: 'Meld je aan als bedrijf', go: function () { start('hulp', true); } });
        if (hit.cta === 'werk') list.push({ label: 'Meld je aan voor werk', go: function () { start('werk', true); } });
        list.push({ label: 'Nog een vraag', go: function () { say('Zeg het maar.'); } });
        chips(list);
      });
    } else {
      data.vraag = v;
      say(['Goede vraag. Die beantwoorden we liefst persoonlijk.', 'Mogen we je even terugbellen?'], function () {
        chips([{ label: 'Ja, bel me terug', go: function () { start('vraag', true); } }, { label: 'Stuur een WhatsApp', cls: 'zc-chip--wa', href: 'https://wa.me/' + WA + '?text=' + encodeURIComponent('Hallo Zondags, ik heb een vraag: ' + v) }]);
      });
    }
  }

  /* ---------- flows ---------- */
  function greet() {
    say(['Hallo, welkom bij Zondags.', 'Waarmee kunnen we je helpen?'], function () {
      chips([
        { label: 'Ik zoek hulp voor mijn bedrijf', go: function () { start('hulp', true); } },
        { label: 'Ik zoek werk', go: function () { start('werk', true); } },
        { label: 'Ik heb een vraag', go: function () { say('Stel gerust je vraag. Of kies er een:', function () { chips(['Wat kost een Zondag?', 'Kan mijn vennootschap dit betalen?', 'In welke regio werken jullie?', 'Wat verdien ik als Zondag?', 'Kan ik werken als student of flexi?'], { onPick: answer }); }); } }
      ]);
    });
  }

  function start(f, silent) {
    flow = f; var keep = data.vraag; data = { type: f === 'hulp' ? 'Bedrijf zoekt hulp' : f === 'werk' ? 'Kandidaat zoekt werk' : 'Vraag, terugbellen' };
    if (keep) data.vraag = keep;
    if (f === 'hulp') return hulp1();
    if (f === 'werk') return werk1();
    return naam(function () { return tel(function () { return summary(); }); });
  }

  function hulp1() {
    say(['Fijn. Wat mag je Zondag voor je doen?', 'Kies wat past, meerdere mag.'], function () {
      chips(['Poetsen', 'Was en strijk', 'Koken', 'Boodschappen', 'Kinderen ophalen', 'Tuin', 'Kantoor of praktijk', 'Alles in huis', { label: 'Verder', action: 'done', cls: 'zc-chip--go' }], { multi: true, onPick: function (p) { data.wat = p.join(', '); hulp2(); } });
    });
  }
  function hulp2() { ask('gemeente', 'In welke gemeente mag je Zondag langskomen?', { ph: 'Bijvoorbeeld Kortrijk', ac: 'address-level2', next: hulp3 }); }
  function hulp3() {
    say('Hoeveel hulp heb je ongeveer nodig?', function () {
      chips(['Een paar uur per week', 'Een halve dag per week', 'Meerdere dagen per week', 'Weet ik nog niet'], { onPick: function (v) { data.uren = v; naam(function () { ask('bedrijf', 'En de naam van je bedrijf of praktijk?', { ph: 'Naam van je zaak', ac: 'organization', skip: true, next: function () { tel(mail); } }); }); } });
    });
  }

  function werk1() {
    say(['Leuk dat je Zondag wilt worden.', 'Wat past het best bij jou?'], function () {
      chips(['Student', 'Flexi-job of bijverdienen', 'Vast contract', 'Werkzoekend', 'Iets anders'], { onPick: function (v) { data.statuut = v; werk2(); } });
    });
  }
  function werk2() {
    say('We werken met mensen vanaf 18 jaar. Ben jij 18 of ouder?', function () {
      chips([{ label: 'Ja', go: werk3 }, { label: 'Nog niet', go: function () { say('Dan houden we je graag in gedachten voor later. Kom zeker terug zodra je 18 bent.', function () { chips([{ label: 'Opnieuw beginnen', go: greet }]); }); } }]);
    });
  }
  function werk3() {
    var note = /Student/.test(data.statuut) ? 'Als student werk je met een studentencontract. Dat regelen wij.' :
               /Flexi/.test(data.statuut) ? 'Of een flexi-job voor jou kan, hangt af van je hoofdjob. Dat bekijken we samen in het eerste gesprek.' : '';
    var q = (note ? [note] : []).concat('Waar woon je?');
    ask('gemeente', q, { ph: 'Bijvoorbeeld Waregem', ac: 'address-level2', next: werk4 });
  }
  function werk4() {
    say(['Wanneer kun je werken?', 'Kies wat past, meerdere mag.'], function () {
      chips(['Voormiddagen', 'Namiddagen', 'Hele dagen', 'Tijdens de schooluren', 'In de schoolvakanties', 'Flexibel', { label: 'Verder', action: 'done', cls: 'zc-chip--go' }], { multi: true, onPick: function (p) { data.uren = p.join(', '); werk5(); } });
    });
  }
  function werk5() {
    say('Wat doe je graag?', function () {
      chips(['Huishouden', 'Koken', 'Boodschappen', 'Kinderen', 'Tuin', 'Kantoren en praktijken', { label: 'Verder', action: 'done', cls: 'zc-chip--go' }], { multi: true, onPick: function (p) { data.wat = p.join(', '); naam(function () { tel(mail); }); } });
    });
  }

  function naam(next) { ask('naam', 'Hoe heet je?', { ph: 'Voor- en achternaam', ac: 'name', next: next }); }
  function tel(next) {
    ask('telefoon', 'Op welk nummer mogen we je bellen?', { type: 'tel', inputmode: 'tel', ac: 'tel', ph: '0470 12 34 56', validate: validPhone, err: 'Dat nummer lijkt niet volledig. Probeer je het nog eens?', next: function () { next(); } });
  }
  function mail() {
    ask('email', 'En je e-mailadres? Dat mag je ook overslaan.', { type: 'email', inputmode: 'email', ac: 'email', ph: 'naam@bedrijf.be', skip: true, validate: function (v) { return validMail(v); }, err: 'Dat e-mailadres klopt niet helemaal. Probeer je het nog eens?', next: summary });
  }

  function lines() {
    var L = [];
    L.push('Type: ' + data.type);
    if (data.naam) L.push('Naam: ' + data.naam);
    if (data.bedrijf) L.push('Bedrijf: ' + data.bedrijf);
    if (data.statuut) L.push('Statuut: ' + data.statuut);
    if (data.gemeente) L.push('Gemeente: ' + data.gemeente);
    if (data.wat) L.push((flow === 'werk' ? 'Doet graag: ' : 'Hulp bij: ') + data.wat);
    if (data.uren) L.push((flow === 'werk' ? 'Beschikbaar: ' : 'Hoeveel: ') + data.uren);
    if (data.telefoon) L.push('Telefoon: ' + data.telefoon);
    if (data.email) L.push('E-mail: ' + data.email);
    if (data.vraag) L.push('Vraag: ' + data.vraag);
    return L;
  }
  function summary() {
    say(['Top. Dit sturen we door:', esc(lines().slice(1).join('\n')), 'We gebruiken je gegevens enkel om je te contacteren.'], function () {
      chips([{ label: 'Verstuur', cls: 'zc-chip--go', go: send }, { label: 'Opnieuw beginnen', go: function () { start(flow, true); } }]);
    });
  }

  function utm() {
    var q = new URLSearchParams(location.search), out = [];
    ['utm_source', 'utm_medium', 'utm_campaign'].forEach(function (k) { if (q.get(k)) out.push(q.get(k)); });
    var ref = document.referrer && document.referrer.indexOf(location.host) < 0 ? document.referrer.replace(/^https?:\/\//, '').split('/')[0] : '';
    var first = store('zc_first') || ''; if (!first) { first = location.pathname; store('zc_first', first); }
    return { bron: out.join(' / ') || ref || 'direct', eerste: first };
  }

  function send() {
    var u = utm();
    var txt = 'Hallo Zondags,\n' + lines().join('\n');
    var leadWa = data.telefoon ? 'https://wa.me/' + waNum(data.telefoon) + '?text=' + encodeURIComponent('Hallo ' + (data.naam || '').split(' ')[0] + ', met Mieke van Zondags. Bedankt voor je bericht via onze website.') : '';
    var p = {
      source: 'zondags-chat', type: data.type, naam: data.naam || '', bedrijf: data.bedrijf || '', statuut: data.statuut || '',
      telefoon: data.telefoon || '', e_mail: data.email || '', gemeente: data.gemeente || '', wat: data.wat || '', uren: data.uren || '',
      vraag: data.vraag || '', pagina: location.href.split('#')[0], bron: u.bron, eerste_pagina: u.eerste,
      tijdstip: new Date().toLocaleString('nl-BE', { timeZone: 'Europe/Brussels' }), wa_link: leadWa
    };
    try { fetch(HOOK, { method: 'POST', mode: 'no-cors', body: new URLSearchParams(p) }); } catch (e) {}
    var m = { _subject: 'Zondags chat: ' + data.type + ' · ' + (data.naam || '') + (data.gemeente ? ' · ' + data.gemeente : ''), _template: 'table', _captcha: 'false' };
    if (data.email) m._replyto = data.email;
    lines().forEach(function (l) { var i = l.indexOf(': '); m[l.slice(0, i)] = l.slice(i + 2); });
    m['Pagina'] = p.pagina; m['Bron'] = u.bron; m['Antwoord via WhatsApp'] = leadWa || '-';
    try { fetch(MAIL, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(m) }); } catch (e) {}
    try { if (window.gtag) window.gtag('event', 'generate_lead', { lead_type: flow }); if (window.dataLayer) window.dataLayer.push({ event: 'zondags_chat_lead', lead_type: flow }); } catch (e) {}
    store('zc_done', '1');
    var first = (data.naam || '').split(' ')[0];
    var msg = flow === 'werk' ? 'Dank je, ' + esc(first) + '. We bellen je binnen de twee werkdagen voor een kort gesprek.' :
              'Dank je, ' + esc(first) + '. Binnen één werkdag belt een van ons je persoonlijk terug.';
    say([msg, 'Wil je meteen iets kwijt? Stuur ons gerust ook een WhatsApp.'], function () {
      chips([{ label: 'Stuur een WhatsApp', cls: 'zc-chip--wa', href: 'https://wa.me/' + WA + '?text=' + encodeURIComponent(txt) }, { label: 'Nog een vraag', go: function () { resetInput(); flow = null; data = {}; say('Zeg het maar.'); } }]);
    });
  }

  /* ---------- open en dicht ---------- */
  function open(f) {
    hideTeaser(true);
    panel.classList.add('is-open'); launch.setAttribute('aria-expanded', 'true');
    launch.setAttribute('aria-label', 'Sluit de chat');
    if (!started) { started = true; if (f) { say('Hallo, welkom bij Zondags.', function () { start(f, true); }); } else greet(); }
    else if (f && f !== flow) { clearChips(); start(f, true); }
    setTimeout(function () { if (window.matchMedia('(min-width:561px)').matches) input.focus(); }, 380);
  }
  function close() {
    panel.classList.remove('is-open'); launch.setAttribute('aria-expanded', 'false');
    launch.setAttribute('aria-label', 'Open de chat van Zondags'); launch.focus();
  }
  function hideTeaser(remember) { teaser.classList.remove('is-on'); if (remember) store('zc_teaser', 'off'); }

  launch.addEventListener('click', function () { panel.classList.contains('is-open') ? close() : open(); });
  panel.querySelector('.zc-close').addEventListener('click', close);
  teaser.querySelector('.zc-x').addEventListener('click', function () { hideTeaser(true); });
  Array.prototype.forEach.call(teaser.querySelectorAll('[data-flow]'), function (b) { b.addEventListener('click', function () { open(b.getAttribute('data-flow')); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && panel.classList.contains('is-open')) close(); });
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-chat]');
    if (a) { e.preventDefault(); open(a.getAttribute('data-chat') || undefined); }
  });

  if (!quiet && store('zc_teaser') !== 'off' && store('zc_done') !== '1') {
    setTimeout(function () { if (!panel.classList.contains('is-open')) teaser.classList.add('is-on'); }, 2500);
  }

  window.ZondagsChat = { open: open, close: close };
})();
