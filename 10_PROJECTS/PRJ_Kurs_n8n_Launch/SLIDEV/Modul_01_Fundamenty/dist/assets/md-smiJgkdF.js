import{o as n,b as d,w as s,g as e,v as a,x as l,T as i}from"./modules/vue-DTm6WjlB.js";import{I as p}from"./slidev/default-CxxHKT0_.js";import{u as g,f as m}from"./slidev/context-fk4oM2Ln.js";import"./index-B9XWOAx6.js";import"./modules/shiki-a8IyBTWe.js";const h={__name:"slides.md__slidev_7",setup(f){const{$clicksContext:o,$frontmatter:t}=g();return o.setup(),(x,r)=>(n(),d(p,a(l(i(m)(i(t),6))),{default:s(()=>[...r[0]||(r[0]=[e("h1",null,"Interfejs n8n — mapa",-1),e("div",{style:{background:"#0A1628","border-radius":"10px",overflow:"hidden",border:"1px solid rgba(255,255,255,0.08)","box-shadow":"0 8px 32px rgba(0,0,0,0.4)","font-family":"Inter,sans-serif",position:"relative"}},[e("div",{style:{position:"absolute",inset:"0","background-image":"radial-gradient(rgba(255,255,255,0.04) 1px,transparent 1px)","background-size":"20px 20px","pointer-events":"none"}}),e("div",{style:{position:"relative",background:"#0F2137","border-bottom":"2px solid #E63946",padding:"0.5rem 1rem",display:"flex","align-items":"center",gap:"1.5rem"}},[e("div",{style:{display:"flex","align-items":"center",gap:"0.4rem"}},[e("div",{style:{background:"#E63946",color:"#fff","font-weight":"900","font-size":"0.65rem",width:"18px",height:"18px","border-radius":"3px",display:"flex","align-items":"center","justify-content":"center"}},"n"),e("span",{style:{color:"#fff","font-size":"0.72rem","font-weight":"700"}},"n8n")]),e("div",{style:{display:"flex",gap:"1rem"}},[e("span",{style:{color:"#A8D8EA","font-size":"0.68rem","font-weight":"600","border-bottom":"2px solid #E63946","padding-bottom":"2px"}},"Workflows"),e("span",{style:{color:"#64748B","font-size":"0.68rem"}},"Credentials"),e("span",{style:{color:"#64748B","font-size":"0.68rem"}},"Executions"),e("span",{style:{color:"#64748B","font-size":"0.68rem"}},"Settings")]),e("div",{style:{"margin-left":"auto",display:"flex",gap:"0.5rem"}},[e("span",{style:{background:"#1E2D40",color:"#8096AA","font-size":"0.6rem",padding:"0.2rem 0.55rem","border-radius":"4px",border:"1px solid rgba(255,255,255,0.08)"}},"Save"),e("span",{style:{background:"#1E2D40",color:"#8096AA","font-size":"0.6rem",padding:"0.2rem 0.55rem","border-radius":"4px",border:"1px solid rgba(255,255,255,0.08)"}},"Test"),e("span",{style:{background:"#22C55E",color:"#fff","font-size":"0.6rem",padding:"0.2rem 0.55rem","border-radius":"4px","font-weight":"700"}},"Activate")])]),e("div",{style:{position:"relative",display:"flex",gap:"0","min-height":"160px"}},[e("pre",null,[e("code",null,`<!-- Left panel — node library -->
<div style="width:140px;flex-shrink:0;background:#0F2137;border-right:1px solid rgba(255,255,255,0.07);padding:0.6rem 0.7rem">
  <div style="color:#E63946;font-size:0.6rem;font-weight:700;letter-spacing:0.08em;margin-bottom:0.5rem">BIBLIOTEKA NODÓW</div>
  <div style="display:flex;flex-direction:column;gap:0.3rem">
    <div style="background:#1E2D40;border-radius:4px;padding:0.25rem 0.5rem;font-size:0.62rem;color:#A8D8EA;border-left:2px solid #F97316">⚡ Triggery</div>
    <div style="background:#1E2D40;border-radius:4px;padding:0.25rem 0.5rem;font-size:0.62rem;color:#A8D8EA;border-left:2px solid #3B82F6">⚙ Akcje</div>
    <div style="background:#1E2D40;border-radius:4px;padding:0.25rem 0.5rem;font-size:0.62rem;color:#A8D8EA;border-left:2px solid #8B5CF6">🔀 Logika</div>
    <div style="background:#1E2D40;border-radius:4px;padding:0.25rem 0.5rem;font-size:0.62rem;color:#A8D8EA;border-left:2px solid #64748B">🔗 HTTP / Code</div>
  </div>
</div>

<!-- Canvas -->
<div style="flex:1;padding:1rem 1.2rem;display:flex;align-items:center;gap:0.6rem">
  <div style="background:#1E2D40;border-radius:6px;border:1px solid rgba(255,255,255,0.08);border-top:2px solid #F97316;padding:0.4rem 0.7rem;text-align:center;min-width:72px">
    <div style="font-size:0.6rem;color:#F97316;font-weight:700">WEBHOOK</div>
    <div style="font-size:0.55rem;color:#64748B;margin-top:2px">Trigger</div>
  </div>
  <svg width="28" height="8" viewBox="0 0 28 8"><line x1="0" y1="4" x2="20" y2="4" stroke="#E63946" stroke-width="1.5" stroke-dasharray="3 2"/><polygon points="20,1 28,4 20,7" fill="#E63946"/></svg>
  <div style="background:#1E2D40;border-radius:6px;border:1px solid rgba(255,255,255,0.08);border-top:2px solid #3B82F6;padding:0.4rem 0.7rem;text-align:center;min-width:72px">
    <div style="font-size:0.6rem;color:#3B82F6;font-weight:700">IF NODE</div>
    <div style="font-size:0.55rem;color:#64748B;margin-top:2px">Logika</div>
  </div>
  <svg width="28" height="8" viewBox="0 0 28 8"><line x1="0" y1="4" x2="20" y2="4" stroke="#E63946" stroke-width="1.5" stroke-dasharray="3 2"/><polygon points="20,1 28,4 20,7" fill="#E63946"/></svg>
  <div style="background:#1E2D40;border-radius:6px;border:1px solid rgba(255,255,255,0.08);border-top:2px solid #22C55E;padding:0.4rem 0.7rem;text-align:center;min-width:72px">
    <div style="font-size:0.6rem;color:#22C55E;font-weight:700">GMAIL</div>
    <div style="font-size:0.55rem;color:#64748B;margin-top:2px">Wyślij</div>
  </div>
  <div style="margin-left:auto;background:#0F2137;border-radius:6px;padding:0.5rem 0.8rem;font-size:0.6rem;color:#64748B;border:1px dashed rgba(255,255,255,0.1);text-align:center">
    <div style="color:#A8D8EA;font-weight:600;margin-bottom:2px">CANVAS</div>
    <div>przeciągnij nody</div>
    <div>z biblioteki →</div>
  </div>
</div>
`)])]),e("div",{style:{position:"relative",background:"#0F2137","border-top":"1px solid rgba(255,255,255,0.07)",padding:"0.4rem 1rem",display:"flex","align-items":"center",gap:"1.5rem"}},[e("span",{style:{color:"#22C55E","font-size":"0.62rem","font-weight":"600"}},"✓ Executions: 14 total"),e("span",{style:{color:"#64748B","font-size":"0.6rem"}},"Last: 2 min ago"),e("div",{style:{"margin-left":"auto",display:"flex",gap:"1rem"}},[e("span",{style:{color:"#8096AA","font-size":"0.6rem"}},"← Execution log"),e("span",{style:{color:"#8096AA","font-size":"0.6rem"}},"Settings →")])])],-1)])]),_:1},16))}};export{h as default};
