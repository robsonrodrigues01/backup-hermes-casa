// qa-painel.js — sonda canônica de QA do painel-escritório (v3+)
// USO: colar TODO este arquivo como `expression` no browser_console (após browser_navigate).
// Erros de JS: o buffer do próprio browser_console já reporta; exigir zero ALÉM do verde.
// REGRA: verde é FINAL. Parar, publicar, encerrar. Nunca retunar estado que já passou.
(() => {
  // Ajustar EXPECT só se o elenco mudar (13 hoje) ou entrar novo tipo de placa
  const EXPECT = { agents: 13, maxLpOverlap: 0, maxTrunc: 0 };
  const out = {};
  // 1) agentes renderizados = array JS = esperado
  const dom = document.querySelectorAll('.agent').length;
  const js = window.AG ? AG.length : -1;
  out.agents = { dom, js, ok: dom > 0 && dom === js && dom === EXPECT.agents };
  // 2) sobreposição entre cartões fixos .lp da mesa longa (tolerância 2px)
  const r = [...document.querySelectorAll('.lp')].map(e => e.getBoundingClientRect());
  let ov = 0;
  for (let i = 0; i < r.length; i++)
    for (let j = i + 1; j < r.length; j++) {
      const a = r[i], b = r[j];
      if (a.left < b.right - 2 && b.left < a.right - 2 && a.top < b.bottom - 2 && b.top < a.bottom - 2) ov++;
    }
  out.lpOverlap = { n: ov, ok: ov <= EXPECT.maxLpOverlap };
  // 3) texto cortado em .st (status) e .lp (cartões) — DOM, nunca screenshot
  const trunc = [...document.querySelectorAll('.st,.lp')]
    .filter(e => e.scrollWidth > e.clientWidth + 1)
    .map(e => (e.id || e.className).toString().slice(0, 24));
  out.trunc = { n: trunc.length, which: trunc, ok: trunc.length <= EXPECT.maxTrunc };
  // 4) cena cabe na tela (bug v2 no celular: clip da coluna esquerda)
  const sb = document.querySelector('.fitwrap') || document.querySelector('.scenebox');
  const vw = document.documentElement.clientWidth;
  const sw = sb ? Math.round(sb.getBoundingClientRect().width) : null;
  out.fit = { scene: sw, viewport: vw, ok: !sb || sw <= vw + 2 };
  out.verdict = (out.agents.ok && out.lpOverlap.ok && out.trunc.ok && out.fit.ok)
    ? 'VERDE: parar, publicar e encerrar'
    : 'VERMELHO: ajustar UMA coisa e re-rodar a sonda';
  return JSON.stringify(out);
})()
