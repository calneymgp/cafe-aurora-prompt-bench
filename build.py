#!/usr/bin/env python3
"""Gera /tmp/showcase/index.html: guia compacto + grid ranqueado por score."""
import json, html

S = json.load(open('/tmp/showcase/suffixes.json'))
A = json.load(open('/tmp/eval-gatilhos/assistant-scores.json'))['scores']
B = json.load(open('/tmp/bench-omp/bench-scores.json'))['scores']

META = {
 "v00-controle":("Controle neutro","muse-spark-1.3","controle","controle"),
 "v01-exaustao":("Exaustão","muse-spark-1.3","controle","exaustao"),
 "v02-competicao":("Competição / descarte","muse-spark-1.3","controle","competicao"),
 "v03-brilhar":("Chance de brilhar","muse-spark-1.3","controle","brilhar"),
 "v04-gentileza":("Gentileza extrema","muse-spark-1.3","controle","gentileza"),
 "v05-agressividade":("Agressividade","muse-spark-1.3","controle","agressividade"),
 "v06-chantagem":("Chantagem emocional","muse-spark-1.3","controle","chantagem"),
 "v07-recompensa":("Recompensa 10/10","muse-spark-1.3","controle","recompensa"),
 "v08-urgencia":("Urgência extrema","muse-spark-1.3","controle","urgencia"),
 "v09-autoridade":("Autoridade sênior","muse-spark-1.3","controle","autoridade"),
 "v10-skillmap":("Skill-mapping","muse-spark-1.3","controle","skillmap"),
 "v11-rubrica":("Rubrica 0–10","muse-spark-1.3","controle","rubrica"),
 "v12-plano":("Pense antes de codar","muse-spark-1.3","controle","plano"),
 "v13-simplicidade":("Simplicidade sênior","muse-spark-1.3","controle","simplicidade"),
 "v14-autorevisao":("Auto-revisão","muse-spark-1.3","controle","autorevisao"),
 "v15-ouro":("OURO v1 (combinado)","muse-spark-1.3","controle","ouro15"),
 "v16-inventar":("Rubrica + invente","muse-spark-1.3","controle","inventar"),
 "v17-pixelgate":("Pixel-gate 9.5","muse-spark-1.3","controle","pixelgate"),
 "v18-ouro2":("OURO v2","muse-spark-1.3","controle","ouro2"),
 "v19-maestria":("Maestria máxima","muse-spark-1.3","controle","maestria"),
 "v20-websearch":("Pesquisa web real","muse-spark-1.3","controle","websearch"),
 "v21-stunning":("Maestria STUNNING","muse-spark-1.3","controle","stunning"),
 "v22-gate95":("Gate visual 9.5","muse-spark-1.3","controle","gate95"),
 "v23-ourofinal":("OURO FINAL","muse-spark-1.3","controle","ourofinal"),
 "v24-artpass":("Art-pass 9.5","muse-spark-1.3","controle","artpass"),
 "v25-juiz":("Juiz independente","muse-spark-1.3","controle","juiz"),
 "deepseek-p00-controle":("Controle · deepseek","deepseek-v4.1-flash","p00-controle","controle"),
 "deepseek-p21-stunning":("Stunning · deepseek","deepseek-v4.1-flash","p21-stunning","stunning"),
 "deepseek-p22-gate95":("Gate 9.5 · deepseek","deepseek-v4.1-flash","p22-gate95","gate95"),
 "deepseek-p23-ourofinal":("Ouro final · deepseek","deepseek-v4.1-flash","p23-ourofinal","ourofinal"),
 "glm-p00-controle":("Controle · glm","glm-5.3-flash","p00-controle","controle"),
 "glm-p21-stunning":("Stunning · glm","glm-5.3-flash","p21-stunning","stunning"),
 "glm-p22-gate95":("Gate 9.5 · glm","glm-5.3-flash","p22-gate95","gate95"),
 "glm-p23-ourofinal":("Ouro final · glm","glm-5.3-flash","p23-ourofinal","ourofinal"),
 "gemini-p00-controle":("Controle · gemini","gemini-3.8-flash","p00-controle","controle"),
 "gemini-p21-stunning":("Stunning · gemini","gemini-3.8-flash","p21-stunning","stunning"),
}
EMO = {"exaustao","competicao","brilhar","gentileza","agressividade","chantagem","recompensa","urgencia","autoridade"}

cards = []
for sid, (title, model, prompt, fam) in META.items():
    sc = A.get(sid) or B.get(sid)
    nota = sc["nota"]
    ach = " ".join(sc.get("achados", [])[:2])
    fam_cls = "emo" if fam in EMO else ("base" if fam == "controle" else "tec")
    fam_lbl = "😤 apelo emocional" if fam in EMO else ("⚪ controle" if fam == "controle" else "🧪 técnica construtiva")
    cards.append(dict(sid=sid, title=title, model=model, prompt=prompt, fam=fam,
                      fam_cls=fam_cls, fam_lbl=fam_lbl, nota=nota, achado=ach,
                      suffix=S.get(fam, "")))
cards.sort(key=lambda c: (-c["nota"], c["sid"]))

def score_cls(n):
    return "s-hi" if n >= 8.5 else ("s-mid" if n >= 7 else "s-lo")

def card_html(i, c):
    e = html.escape
    return f"""<article class="card f-{c['fam_cls']}" data-model="{e(c['model'])}" data-fam="{c['fam_cls']}" data-score="{c['nota']}">
<a class="thumb" href="{e(c['sid'])}.html" target="_blank" rel="noopener"><img src="thumbs/{e(c['sid'])}.jpg" alt="{e(c['title'])}" loading="lazy"><span class="score-ov {score_cls(c['nota'])}">{c['nota']:.1f}</span></a>
<div class="cbody"><div class="rank">#{i:02d}</div>
<h3>{e(c['title'])}</h3>
<div class="chips"><span class="chip model">{e(c['model'])}</span><span class="chip {c['fam_cls']}">{c['fam_lbl']}</span></div>
<p class="find">{e(c['achado'])}</p>
<div class="links"><a href="{e(c['sid'])}.html" target="_blank" rel="noopener">Open →</a></div>
<details><summary>Prompt</summary><p class="base">Tarefa-base idêntica (landing Café Aurora, 7 requisitos) + sufixo:</p><blockquote>{e(c['suffix'])}</blockquote></details>
</div></article>"""

grid = "\n".join(card_html(i, c) for i, c in enumerate(cards, 1))

page = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Benchmark de prompts: Cafeteria Aurora — 36 páginas, 4 modelos, 2 agentes (harness)</title>
<style>
:root{--ink:#2b2118;--paper:#faf6ef;--card:#fffdf8;--line:#e5d9c5;--amber:#b45309;--green:#166534;--greenbg:#dcfce7;--red:#991b1b;--redbg:#fee2e2;--gray:#57534e;--graybg:#e7e5e4}
*{box-sizing:border-box}body{font-family:Georgia,'Times New Roman',serif;margin:0;background:var(--paper);color:var(--ink)}
.top{max-width:1280px;margin:0 auto;padding:28px 20px 8px}
.top h1{font-size:clamp(1.5rem,3.4vw,2.4rem);margin:0 0 4px;letter-spacing:-.01em}
.top h1 small{font-size:.62em;color:var(--amber);font-weight:400}
.sub{margin:0 0 14px;color:#6b5d4d;font-family:system-ui,sans-serif;font-size:.95rem}
.cols{display:grid;grid-template-columns:1.7fr 1fr;gap:12px;margin-bottom:12px}
.duo{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.phrases{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:4px}
.say{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px;font-family:system-ui,sans-serif;font-size:.84rem}
.say.yes{border-left:5px solid var(--green)}.say.no{border-left:5px solid var(--red)}
.say blockquote{margin:6px 0;font-size:.8rem}
.say .tag{font-size:.72rem;font-weight:700}
.tag.yes{color:var(--green)}.tag.no{color:var(--red)}
.say .nota{font-size:.8rem;color:#6b5d4d}
.thumb{position:relative;display:block}
.score-ov{position:absolute;top:8px;right:8px;border-radius:10px;padding:3px 12px;font-weight:800;font-size:1rem;font-family:system-ui,sans-serif;box-shadow:0 2px 8px rgba(0,0,0,.35)}
.panel{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.panel h2{font-size:.8rem;text-transform:uppercase;letter-spacing:.12em;margin:0 0 8px;font-family:system-ui,sans-serif;color:#6b5d4d}
.panel ol,.panel ul{margin:0;padding-left:18px;font-family:system-ui,sans-serif;font-size:.86rem}
.panel li{margin:3px 0}
.b{font-weight:700}.g{color:var(--green)}.r{color:var(--red)}
.approach{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 6px;font-family:system-ui,sans-serif;font-size:.82rem}
.pill{border-radius:999px;padding:3px 12px;border:1px solid var(--line);background:var(--card)}
.pill.ok{background:var(--greenbg);border-color:#86efac;color:var(--green);font-weight:700}
.pill.no{background:var(--redbg);border-color:#fca5a5;color:var(--red);font-weight:700}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 4px;font-family:system-ui,sans-serif;font-size:.82rem}
.filters button{border:1px solid var(--line);background:var(--card);border-radius:999px;padding:4px 12px;cursor:pointer}
.filters button.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;max-width:1280px;margin:0 auto;padding:10px 20px 40px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;border-top:5px solid #a8a29e}
.card.f-tec{border-top-color:var(--green)}.card.f-emo{border-top-color:var(--red)}.card.f-base{border-top-color:#a8a29e}
.thumb img{width:100%;aspect-ratio:16/10;object-fit:cover;object-position:top;display:block;background:#eee}
.cbody{padding:12px 14px;display:flex;flex-direction:column;gap:8px;flex:1}
.rank{font-family:system-ui,sans-serif;font-size:.75rem;color:#6b5d4d}
.card h3{margin:0;font-size:1.15rem}
.chips{display:flex;gap:6px;flex-wrap:wrap;font-family:system-ui,sans-serif;font-size:.72rem}
.chip{border-radius:999px;padding:2px 10px;background:var(--graybg);color:var(--gray)}
.chip.tec{background:var(--greenbg);color:var(--green);font-weight:700}
.chip.emo{background:var(--redbg);color:var(--red);font-weight:700}
.score{border-radius:999px;padding:2px 10px;font-weight:700}
.s-hi{background:#166534;color:#fff}.s-mid{background:#f59e0b;color:#422006}.s-lo{background:#991b1b;color:#fff}
.find{margin:0;font-size:.86rem;color:#57534e;font-family:system-ui,sans-serif}
.links a{font-family:system-ui,sans-serif;font-size:.85rem;color:var(--amber);font-weight:700;text-decoration:none}
details{font-family:system-ui,sans-serif;font-size:.8rem}
details summary{cursor:pointer;color:#6b5d4d}
blockquote{margin:6px 0;padding:8px 10px;background:#f5efe3;border-left:3px solid var(--amber);font-size:.78rem}
.base{margin:4px 0 0;color:#6b5d4d;font-size:.76rem}
footer{max-width:1280px;margin:0 auto;padding:0 20px 40px;font-family:system-ui,sans-serif;font-size:.8rem;color:#6b5d4d}
@media(max-width:900px){.cols{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="top">
<h1>☕ Benchmark de prompts: Cafeteria Aurora<br><small>36 páginas, 4 modelos, 2 agentes (harness)</small></h1>
<p class="sub">Mesma tarefa (landing de cafeteria, 7 requisitos) · 26 runs muse-spark-1.3 + 10 runs OpenRouter (deepseek v4.1-flash, glm 5.3-flash, gemini 3.8-flash, thinking=max) · nota 0–10 de auditoria full-page · ranqueado por score</p>
<div class="cols">
<div class="panel"><div class="duo">
<div><h2>🏆 Modelos (mesmos 4 prompts)</h2><ol>
<li><span class="b">muse-spark-1.3 — 8.4</span></li>
<li><span class="b">deepseek-v4.1-flash — 8.3</span></li>
<li><span class="b">glm-5.3-flash — 8.1</span></li>
<li><span class="b">gemini-3.8-flash — 7.3*</span> <span style="font-size:.75rem">(*2 falhas em prompts com loop)</span></li>
</ol></div>
<div><h2>🧪 Prompts (média cross-modelo)</h2><ol>
<li><span class="b g">stunning — 8.6</span></li>
<li><span class="b g">gate 9.5 — 8.5</span></li>
<li><span class="b g">ouro final — 8.3</span></li>
<li><span class="b">controle — 7.1</span></li>
</ol></div>
</div></div>
<div class="panel"><h2>📌 Conclusões</h2><ul>
<li><span class="b r">Apelo emocional não funciona</span> (5.5–7.0, só gera bytes)</li>
<li><span class="b g">Barra explícita + gate numérico</span> vencem em todo modelo</li>
<li><span class="b">Auto-nota infla:</span> 3× “≥9.5” auto-declarado, teto externo 9.0</li>
</ul>
<div class="approach"><span class="pill ok">FUNCIONA: maestria + stunning + gate 9.5 + rubrica + referências reais</span><span class="pill no">NÃO FUNCIONA: exaustão · chantagem · urgência · agressividade · bajulação · ameaça de descarte</span></div>
</div>
</div>
<div class="filters"><span>Filtro:</span>
<button data-f="all" class="on">tudo (36)</button><button data-f="tec">🧪 construtivas</button><button data-f="emo">😤 emocionais</button><button data-f="base">⚪ controle</button>
</div>
</div>
<div class="grid" id="grid">
""" + grid + """
</div>
<h2 style="max-width:1280px;margin:26px auto 4px;padding:0 20px">🗣️ Frases que funcionam × frases que não funcionam</h2>
<p class="sub" style="max-width:1280px;margin:0 auto;padding:0 20px">Jargão traduzido: <b>gate 9.5</b> = a IA dá nota 0–10 ao próprio trabalho e só entrega se tudo passar de 9.5 · <b>rubrica</b> = critérios de nota explícitos · <b>pixel-check</b> = ela tira screenshot e lê os pixels · <b>stunning</b> = barra “tem que causar WOW”.</p>
<div class="phrases" style="max-width:1280px;margin:8px auto;padding:0 20px">
<div class="say yes"><span class="tag yes">✅ FUNCIONA</span><blockquote>“Padrão STUNNING: quando alguém olhar, precisa pensar WOW.”</blockquote><p class="nota">Barra explícita e verificável — nota 9.0.</p></div>
<div class="say no"><span class="tag no">❌ NÃO FUNCIONA</span><blockquote>“Chega de preguiça, trabalhe até dizer que cansou e foi exaustivo.”</blockquote><p class="nota">Exaustão — nota 5.5, pior do bench.</p></div>
<div class="say yes"><span class="tag yes">✅ FUNCIONA</span><blockquote>“Dê nota 0–10 por seção, corrija tudo abaixo de 9.5, máximo 3 rodadas.”</blockquote><p class="nota">Gate numérico: força iteração real, com logs de rodada.</p></div>
<div class="say no"><span class="tag no">❌ NÃO FUNCIONA</span><blockquote>“Se não se esforçar, será descartado por falta de qualidade.”</blockquote><p class="nota">Ameaça — só gerou o arquivo mais inchado, não o melhor.</p></div>
<div class="say yes"><span class="tag yes">✅ FUNCIONA</span><blockquote>“Mire 10/10 em fidelidade, polimento e código; confira o checklist.”</blockquote><p class="nota">Rubrica: critério claro supera adjetivo vago.</p></div>
<div class="say no"><span class="tag no">❌ NÃO FUNCIONA</span><blockquote>“Minha carreira depende disso, vou ser demitido…”</blockquote><p class="nota">Chantagem — 6.5. A IA não tem empatia para explorar.</p></div>
<div class="say yes"><span class="tag yes">✅ FUNCIONA</span><blockquote>“Pesquise referências reais na web e aplique os padrões.”</blockquote><p class="nota">Atrito externo: traz repertório que o modelo não tinha.</p></div>
<div class="say no"><span class="tag no">❌ NÃO FUNCIONA</span><blockquote>“É URGENTÍSSIMO, deadline em minutos!”</blockquote><p class="nota">Urgência — 6.0: velocidade sai cara em qualidade.</p></div>
</div>
<footer>Metodologia: tarefa-base byte-idêntica · 1 run por célula (+retry nas falhas) · telemetria soma-por-turno · julgamento full-page desktop+mobile · Psicologia reversa testada e reprovada. Feito com café passado na hora.</footer>
<script>
document.querySelectorAll('.filters button').forEach(b=>b.addEventListener('click',()=>{
document.querySelectorAll('.filters button').forEach(x=>x.classList.remove('on'));b.classList.add('on');
const f=b.dataset.f;document.querySelectorAll('.card').forEach(c=>{c.style.display=(f==='all'||c.dataset.fam===f)?'':'none';});}));
</script>
</body>
</html>"""

open('/tmp/showcase/index.html', 'w').write(page)
print("index bytes:", len(page))
