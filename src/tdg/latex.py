"""Compilación de documentos LaTeX.

Motor preferido: Tectonic (binario único, descarga los paquetes que haga falta).
Alternativas automáticas si Tectonic no está: latexmk, xelatex o pdflatex.

Todas las compilaciones se ejecutan desde la RAÍZ del repositorio, con
TEXINPUTS apuntando a ella (latexmk / xelatex / pdflatex) o con
`-Z search-path` (Tectonic, que no lee TEXINPUTS), de modo que rutas como
`\\input{docs/comun/preambulo}` funcionen sin importar desde dónde se invoque.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


class CompilationError(RuntimeError):
    pass


@dataclass(frozen=True)
class Engine:
    name: str
    executable: str

    def command(self, tex: Path, outdir: Path, root: Path) -> list[str]:
        rel = tex.relative_to(root).as_posix()
        out = outdir.as_posix()
        match self.name:
            case "tectonic":
                # Tectonic ignora TEXINPUTS y resuelve las rutas relativas al
                # directorio del .tex principal; -Z search-path añade la raíz.
                return [
                    self.executable, "-X", "compile", rel,
                    "--outdir", out, "--keep-logs", "--synctex",
                    "-Z", f"search-path={root}",
                ]
            case "latexmk":
                return [
                    self.executable, "-pdf", "-halt-on-error",
                    "-interaction=nonstopmode", f"-outdir={out}", rel,
                ]
            case _:  # xelatex / pdflatex "a mano"
                return [
                    self.executable, "-interaction=nonstopmode",
                    "-halt-on-error", f"-output-directory={out}", rel,
                ]

    @property
    def passes(self) -> int:
        """Tectonic y latexmk gestionan solos las pasadas; los motores crudos no."""
        return 1 if self.name in {"tectonic", "latexmk"} else 3


PREFERENCE = ("tectonic", "latexmk", "xelatex", "pdflatex")


def detect_engine(preferred: str | None = None) -> Engine:
    candidates = (preferred,) if preferred else PREFERENCE
    for name in candidates:
        if name and (exe := shutil.which(name)):
            return Engine(name=name, executable=exe)
    raise CompilationError(
        "No se encontró ningún motor LaTeX en el PATH.\n"
        "Instala Tectonic:  winget install TectonicProject.Tectonic\n"
        "o revisa https://tectonic-typesetting.github.io/book/latest/installation/"
    )


def _environment(root: Path) -> dict[str, str]:
    env = os.environ.copy()
    # El '' final le dice a kpathsea que además use sus rutas por defecto.
    previous = env.get("TEXINPUTS", "")
    env["TEXINPUTS"] = os.pathsep.join([str(root), previous, ""])
    return env


def compile_document(tex: Path, outdir: Path, root: Path, engine: Engine) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    cmd = engine.command(tex, outdir, root)
    env = _environment(root)

    for attempt in range(1, engine.passes + 1):
        result = subprocess.run(
            cmd, cwd=root, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        if result.returncode != 0:
            log = outdir / f"{tex.stem}.log"
            detail = _tail_errors(log) or result.stdout[-3000:] or result.stderr[-3000:]
            raise CompilationError(
                f"{engine.name} falló en la pasada {attempt}/{engine.passes}.\n\n{detail}"
            )

    pdf = outdir / f"{tex.stem}.pdf"
    if not pdf.is_file():
        raise CompilationError(f"La compilación terminó sin errores pero no se generó {pdf}.")
    return pdf


def _tail_errors(log: Path, context: int = 4) -> str:
    """Extrae las líneas de error (`! ...`) del log de LaTeX."""
    if not log.is_file():
        return ""
    lines = log.read_text(encoding="utf-8", errors="replace").splitlines()
    chunks: list[str] = []
    for i, line in enumerate(lines):
        if line.startswith("!"):
            chunks.append("\n".join(lines[i : i + context]))
    return "\n\n".join(chunks[:5])
