#!/usr/bin/env python3
"""Instala un plugin de este market en una config de OpenCode. Solo stdlib.

  python install.py <plugin|all> --project DIR   # DIR/.opencode/
  python install.py <plugin|all> --global        # $OPENCODE_CONFIG_DIR o ~/.config/opencode
  agregar --dry-run para ver que copiaria sin tocar nada

Skills y comandos van a skills/ y commands/ (lo que OpenCode descubre solo); el
resto del plugin (wrappers bin/, tools/) va a market/<plugin>/. Es solo copia de
archivos: no ejecuta nada del plugin.

Las entradas de catalog.json con kind "app" no se instalan con este script: tienen una
receta en apps/<nombre>/recipe.json que se sigue paso a paso con tu herramienta bash.
"""
import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKEN = "${CLAUDE_PLUGIN_ROOT}"
SKILL_TOKEN = "${SKILL_ROOT}"
NOT_PAYLOAD = {"commands", "skills"}


def target_dir(args):
    if args.project:
        return Path(args.project).resolve() / ".opencode"
    env = os.environ.get("OPENCODE_CONFIG_DIR")
    return Path(env) if env else Path.home() / ".config" / "opencode"


def plan(entry, target):
    src = ROOT / entry["path"]
    payload = target / "market" / entry["name"]
    for f in sorted(src.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(src)
        top = rel.parts[0]
        # skill_root: carpeta propia de ESTA skill una vez instalada (skills/<nombre>/...),
        # para que una skill con scripts/referencias internas pueda citar su propia ruta
        # con ${SKILL_ROOT} sin importar si se instalo con --project o --global.
        skill_root = target / "skills" / rel.parts[1] if top == "skills" and len(rel.parts) > 1 else None
        if top in ("skills", "commands"):
            yield f, target / rel, f.suffix == ".md", payload, skill_root
        elif top not in NOT_PAYLOAD:
            yield f, payload / rel, False, payload, skill_root


def install(entry, target, dry):
    for f, dest, substitute, payload, skill_root in plan(entry, target):
        print(f"{'[dry] ' if dry else ''}{f.relative_to(ROOT).as_posix()} -> {dest}")
        if dry:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if substitute:
            text = f.read_text(encoding="utf-8").replace(TOKEN, payload.as_posix())
            if skill_root is not None:
                text = text.replace(SKILL_TOKEN, skill_root.as_posix())
            # OpenCode descarta en silencio un comando cuyo frontmatter no es YAML valido;
            # argument-hint (clave de Claude Code) suele traer "[...]" sin comillas.
            text = re.sub(r"(?m)^argument-hint:\s*(.*)$",
                          lambda m: "argument-hint: " + json.dumps(m.group(1), ensure_ascii=False), text)
            dest.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(f, dest)
            if dest.parent.name == "bin" and dest.suffix == "":
                dest.chmod(dest.stat().st_mode | 0o111)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plugin", help="nombre del plugin (ver catalog.json) o 'all'")
    scope = ap.add_mutually_exclusive_group(required=True)
    scope.add_argument("--project", metavar="DIR")
    scope.add_argument("--global", dest="glob", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))["entries"]
    plugins = [p for p in catalog if p["kind"] == "plugin"]
    chosen = plugins if args.plugin == "all" else [p for p in catalog if p["name"] == args.plugin]
    if not chosen:
        sys.exit(f"desconocido: {args.plugin}. Plugins instalables: {', '.join(p['name'] for p in plugins)}")
    if chosen[0]["kind"] == "app":
        sys.exit(f"'{args.plugin}' es una app, no se instala con este script. Seguí su receta: {chosen[0]['path']}/recipe.json")

    target = target_dir(args)
    for entry in chosen:
        install(entry, target, args.dry_run)
    if not args.dry_run:
        print(f"\nListo en {target}. Reinicia OpenCode y verifica con: opencode debug skill")


if __name__ == "__main__":
    main()
