#!/usr/bin/env python
"""Resuelve el binario de tgrep (microsoft/tgrep, MIT) y lo ejecuta con los
argumentos recibidos, pasando antes por verificacion de integridad.

Prioridad de resolucion:
  1) `tgrep` ya en PATH (instalacion propia del usuario -- se respeta tal cual).
  2) Cache persistente en ~/.cache/tgrep/<version>/ (sobrevive updates
     del plugin y sirve para cualquier proyecto futuro, mismo espiritu que
     el "uv tool persistente" de graph-explorer).
  3) Descarga del release oficial de GitHub, VERIFICADA por sha256 antes de
     ejecutar nada -- si el hash no coincide, aborta sin extraer ni correr
     el binario.

Version pineada a proposito (no se auto-actualiza sola), misma razon que
graph-explorer pinea graphifyy: reproducibilidad y auditoria, no "siempre
lo ultimo".
"""
from __future__ import annotations
import hashlib
import os
import platform
import shutil
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path

VERSION = "1.0.10"
BASE_URL = f"https://github.com/microsoft/tgrep/releases/download/v{VERSION}"

# sha256 por plataforma para el release v1.0.10. Los 4 *nix salen del
# checksums.txt oficial publicado en ese release; los 2 de Windows NO estan
# en ese archivo (microsoft no publica checksum para esos assets), asi que
# los calculamos nosotros mismos una vez (descargamos el asset real y
# corrimos sha256) y quedan pineados aca.
ASSETS = {
    ("Windows", "x86_64"): ("tgrep-v{v}-x86_64-pc-windows-msvc.zip", "35829894320b74c6ff9bcbfcb99523c9f7a0acdc1a58e9bcacfa0f3c8ff372f8", "tgrep.exe"),
    ("Windows", "aarch64"): ("tgrep-v{v}-aarch64-pc-windows-msvc.zip", "eb1a8f69d1679569b7bb51441f656a34b9e92142792987f7fea29ece9f4db8a9", "tgrep.exe"),
    ("Linux", "x86_64"): ("tgrep-v{v}-x86_64-unknown-linux-musl.tar.gz", "de259323635a1d6e9ed26f2833eaa0961f964c234fa127ea8d69bafe16ebd89e", "tgrep"),
    ("Linux", "aarch64"): ("tgrep-v{v}-aarch64-unknown-linux-musl.tar.gz", "913a028e3dc2a9264298fe7f634a3eb84ee208d97afc6d33143adb5aac1e288f", "tgrep"),
    ("Darwin", "x86_64"): ("tgrep-v{v}-x86_64-apple-darwin.tar.gz", "f1472df9a42f40523e80c58a13a35b2514b2211a2074d8e3b7686c20f2beedb5", "tgrep"),
    ("Darwin", "aarch64"): ("tgrep-v{v}-aarch64-apple-darwin.tar.gz", "4240e9e4a6365a55efc4382cb9ccae3eb16ec42df847e38b5d12d935e88188b7", "tgrep"),
}

ARCH_ALIASES = {"amd64": "x86_64", "x86_64": "x86_64", "arm64": "aarch64", "aarch64": "aarch64"}


def cache_dir() -> Path:
    d = Path.home() / ".cache" / "tgrep" / VERSION
    d.mkdir(parents=True, exist_ok=True)
    return d


def resolve_binary() -> Path:
    existing = shutil.which("tgrep")
    if existing:
        return Path(existing)

    system = platform.system()
    machine = ARCH_ALIASES.get(platform.machine().lower(), platform.machine().lower())
    exe_name = "tgrep.exe" if system == "Windows" else "tgrep"
    cached = cache_dir() / exe_name
    if cached.is_file():
        return cached

    key = (system, machine)
    if key not in ASSETS:
        raise SystemExit(f"fast-grep: plataforma no soportada ({system}/{machine})")
    asset_tpl, expected_sha, inner_name = ASSETS[key]
    asset_name = asset_tpl.format(v=VERSION)
    url = f"{BASE_URL}/{asset_name}"

    tmp_archive = cache_dir() / asset_name
    urllib.request.urlretrieve(url, tmp_archive)

    digest = hashlib.sha256(tmp_archive.read_bytes()).hexdigest()
    if digest != expected_sha:
        tmp_archive.unlink(missing_ok=True)
        raise SystemExit(
            f"fast-grep: SHA256 no coincide para {asset_name} "
            f"(esperado {expected_sha}, obtenido {digest}) -- descarga abortada, "
            f"no se extrae ni se ejecuta nada sin verificar."
        )

    extract_dir = cache_dir() / "_extract"
    extract_dir.mkdir(exist_ok=True)
    try:
        if asset_name.endswith(".zip"):
            with zipfile.ZipFile(tmp_archive) as zf:
                zf.extractall(extract_dir)
        else:
            with tarfile.open(tmp_archive) as tf:
                try:
                    tf.extractall(extract_dir, filter="data")
                except TypeError:
                    tf.extractall(extract_dir)  # Python <3.12 sin soporte de filter

        shutil.move(str(extract_dir / inner_name), str(cached))
        if system != "Windows":
            cached.chmod(0o755)
    finally:
        tmp_archive.unlink(missing_ok=True)
        shutil.rmtree(extract_dir, ignore_errors=True)
    return cached


def main() -> int:
    binary = resolve_binary()
    os.execv(str(binary), [str(binary)] + sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
