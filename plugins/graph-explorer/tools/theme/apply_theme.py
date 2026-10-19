#!/usr/bin/env python
"""Post-procesa graph.html (generado por el motor graphify) para darle una
estetica "neuronal" (glow tipo sinapsis, resalte persistente de las aristas
conectadas y "corriente" animada viajando por ellas mientras el nodo siga
seleccionado) sin tocar el motor vendorizado. Idempotente: si el archivo ya
tiene el marcador de tema, no hace nada.

Uso: apply_theme.py <ruta a graph.html>
"""
from __future__ import annotations
import sys
from pathlib import Path

MARKER = "<!-- graph-explorer:neural-theme:v2 -->"

STYLE_BLOCK = f"""{MARKER}
<style>
  body {{
    background:
      repeating-linear-gradient(0deg, rgba(139,92,246,0.035) 0px, rgba(139,92,246,0.035) 1px, transparent 1px, transparent 42px),
      repeating-linear-gradient(90deg, rgba(139,92,246,0.035) 0px, rgba(139,92,246,0.035) 1px, transparent 1px, transparent 42px),
      radial-gradient(ellipse at 50% 0%, #1c1033 0%, #0a0714 55%, #050308 100%) !important;
  }}
  #graph {{
    background: radial-gradient(circle at 30% 20%, rgba(139,92,246,0.07) 0%, transparent 45%),
                radial-gradient(circle at 75% 70%, rgba(34,211,238,0.05) 0%, transparent 40%);
  }}

  #sidebar {{
    background: rgba(15,11,26,0.82) !important;
    backdrop-filter: blur(14px);
    border-left: 1px solid rgba(139,92,246,0.3) !important;
    box-shadow: -12px 0 32px rgba(0,0,0,0.45), inset 1px 0 0 rgba(255,255,255,0.03);
    font-family: ui-monospace, 'Cascadia Code', 'SF Mono', Consolas, monospace;
  }}
  #sidebar h3 {{
    display: flex; align-items: center; gap: 8px;
    color: #c4b5fd !important;
  }}
  #sidebar h3::before {{
    content: ''; width: 3px; height: 13px; border-radius: 2px;
    background: linear-gradient(180deg, #22d3ee, #a78bfa);
    box-shadow: 0 0 8px rgba(34,211,238,0.8);
  }}

  #search-wrap, #info-panel, #legend-wrap, #stats {{
    border-color: rgba(139,92,246,0.16) !important;
  }}
  #search {{
    background: rgba(8,6,16,0.85) !important;
    border: 1px solid rgba(139,92,246,0.3) !important;
    border-radius: 8px !important;
    color: #e4e4f7 !important;
    font-family: inherit;
  }}
  #search::placeholder {{ color: #6b6483; }}
  #search:focus {{
    border-color: #22d3ee !important;
    box-shadow: 0 0 0 3px rgba(34,211,238,0.15), 0 0 16px rgba(34,211,238,0.2) !important;
  }}

  #info-content {{ font-family: inherit; }}
  #info-content .field {{
    padding: 3px 0 3px 10px;
    border-left: 2px solid rgba(139,92,246,0.25);
  }}
  #info-content .field b {{ color: #c4b5fd; }}

  .legend-item {{
    border-radius: 6px;
    transition: background 0.15s ease, transform 0.15s ease, padding-left 0.15s ease;
  }}
  .legend-item:hover {{
    background: rgba(139,92,246,0.14) !important;
    transform: translateX(2px);
  }}
  .legend-dot {{ box-shadow: 0 0 7px currentColor, 0 0 2px currentColor; }}
  .neighbor-link {{ border-radius: 4px; transition: background 0.15s ease, transform 0.15s ease; }}
  .neighbor-link:hover {{ background: rgba(34,211,238,0.14) !important; transform: translateX(2px); }}

  #stats {{
    color: #7c7597 !important;
    letter-spacing: 0.04em;
  }}

  ::-webkit-scrollbar {{ width: 8px; }}
  ::-webkit-scrollbar-track {{ background: transparent; }}
  ::-webkit-scrollbar-thumb {{
    background: rgba(139,92,246,0.4); border-radius: 4px;
    transition: background 0.15s ease;
  }}
  ::-webkit-scrollbar-thumb:hover {{ background: rgba(34,211,238,0.55); }}
</style>
"""

SCRIPT_BLOCK = f"""{MARKER}
<script>
// Look neuronal v2: glow nativo + resalte PERSISTENTE de las aristas conectadas
// mientras el nodo siga seleccionado, con "corriente" (particulas) viajando por
// esas aristas en loop. El loop de animacion solo corre mientras hay un nodo
// activo o un pulso de impacto en curso -- se apaga solo en reposo.
(function () {{
  network.setOptions({{
    nodes: {{ shadow: {{ enabled: true, color: 'rgba(139,92,246,0.55)', size: 16, x: 0, y: 0 }} }},
    edges: {{ shadow: {{ enabled: true, color: 'rgba(99,102,241,0.30)', size: 6, x: 0, y: 0 }} }},
  }});

  const PULSE_MS = 900;
  const CURRENT_PERIOD_MS = 900;
  const pulses = [];
  let activeNodeId = null;
  let activeEdgeIds = [];
  let prevEdgeStates = [];
  let rafRunning = false;

  function ensureLoop() {{
    if (!rafRunning) {{ rafRunning = true; requestAnimationFrame(loop); }}
  }}
  function loop() {{
    const now = performance.now();
    for (let i = pulses.length - 1; i >= 0; i--) {{
      if (now - pulses[i].start > PULSE_MS) pulses.splice(i, 1);
    }}
    network.redraw();
    if (pulses.length || activeNodeId !== null) requestAnimationFrame(loop);
    else rafRunning = false;
  }}

  network.on('afterDrawing', function (ctx) {{
    const now = performance.now();

    // Anillo de impacto (una vez, al seleccionar)
    pulses.forEach(function (p) {{
      const t = Math.min(1, (now - p.start) / PULSE_MS);
      const pos = network.getPositions([p.id])[p.id];
      if (!pos) return;
      const r = 14 + t * 46;
      ctx.save();
      ctx.globalAlpha = (1 - t) * 0.8;
      ctx.strokeStyle = '#22d3ee';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(pos.x, pos.y, r, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
    }});

    // Corriente viajando por las aristas conectadas al nodo activo
    if (activeNodeId !== null && activeEdgeIds.length) {{
      const phase = (now % CURRENT_PERIOD_MS) / CURRENT_PERIOD_MS;
      activeEdgeIds.forEach(function (eid) {{
        const edge = edgesDS.get(eid);
        if (!edge) return;
        const positions = network.getPositions([edge.from, edge.to]);
        const p0 = positions[edge.from], p1 = positions[edge.to];
        if (!p0 || !p1) return;
        [0, 0.34, 0.67].forEach(function (offset) {{
          const f = (phase + offset) % 1;
          const x = p0.x + (p1.x - p0.x) * f;
          const y = p0.y + (p1.y - p0.y) * f;
          ctx.save();
          ctx.globalAlpha = 0.95;
          ctx.fillStyle = '#8fe9fb';
          ctx.shadowColor = '#22d3ee';
          ctx.shadowBlur = 10;
          ctx.beginPath();
          ctx.arc(x, y, 3, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();
        }});
      }});
    }}
  }});

  function clearHighlight() {{
    if (prevEdgeStates.length) edgesDS.update(prevEdgeStates);
    prevEdgeStates = [];
    activeEdgeIds = [];
  }}

  network.on('selectNode', function (params) {{
    const id = params.nodes[0];
    if (id === undefined) return;
    if (activeNodeId !== null && activeNodeId !== id) clearHighlight();
    activeNodeId = id;
    pulses.push({{ id: id, start: performance.now() }});

    const connectedEdges = network.getConnectedEdges(id);
    prevEdgeStates = edgesDS.get(connectedEdges).map(function (e) {{
      return {{ id: e.id, color: e.color, width: e.width }};
    }});
    edgesDS.update(connectedEdges.map(function (eid) {{
      return {{ id: eid, color: {{ color: '#22d3ee', highlight: '#22d3ee' }}, width: 2.5 }};
    }}));
    activeEdgeIds = connectedEdges;
    ensureLoop();
  }});

  network.on('deselectNode', function () {{
    clearHighlight();
    activeNodeId = null;
  }});
}})();
</script>
"""


def apply_theme(html_path: Path) -> dict:
    text = html_path.read_text(encoding="utf-8")
    if MARKER in text:
        return {"ok": True, "applied": False, "reason": "ya tenia el tema (marcador presente)"}
    if "</head>" not in text or "</body>" not in text:
        return {"ok": False, "applied": False, "reason": "no parece un graph.html de graphify (faltan </head> o </body>)"}

    text = text.replace("</head>", STYLE_BLOCK + "</head>", 1)
    text = text.replace("</body>", SCRIPT_BLOCK + "</body>", 1)
    html_path.write_text(text, encoding="utf-8")
    return {"ok": True, "applied": True}


def main() -> int:
    if len(sys.argv) != 2:
        print('{"ok": false, "error": "uso: apply_theme.py <ruta a graph.html>"}')
        return 2
    html_path = Path(sys.argv[1])
    if not html_path.is_file():
        print(f'{{"ok": false, "error": "no existe: {html_path}"}}')
        return 1
    result = apply_theme(html_path)
    import json
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
