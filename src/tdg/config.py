"""Lectura de la configuración de documentos desde pyproject.toml."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


def repo_root(start: Path | None = None) -> Path:
    """Sube por el árbol de directorios hasta encontrar pyproject.toml."""
    here = (start or Path.cwd()).resolve()
    for candidate in (here, *here.parents):
        if (candidate / "pyproject.toml").is_file():
            return candidate
    raise FileNotFoundError("No se encontró pyproject.toml; ¿estás dentro del repositorio?")


@dataclass(frozen=True)
class Document:
    name: str
    tex: Path
    titulo: str
    front_pages: int
    back_pages: int
    max_content_pages: int

    @property
    def has_page_limit(self) -> bool:
        return self.max_content_pages > 0


@dataclass(frozen=True)
class Config:
    root: Path
    build_dir: Path
    deliverables_dir: Path
    autor_slug: str
    documents: dict[str, Document]


def load(start: Path | None = None) -> Config:
    root = repo_root(start)
    data = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    tdg = data.get("tool", {}).get("tdg", {})

    documents: dict[str, Document] = {}
    for name, spec in tdg.get("documents", {}).items():
        documents[name] = Document(
            name=name,
            tex=root / spec["tex"],
            titulo=spec.get("titulo", name),
            front_pages=int(spec.get("front_pages", 0)),
            back_pages=int(spec.get("back_pages", 0)),
            max_content_pages=int(spec.get("max_content_pages", 0)),
        )

    return Config(
        root=root,
        build_dir=root / tdg.get("build_dir", "build"),
        deliverables_dir=root / tdg.get("deliverables_dir", "entregables"),
        autor_slug=tdg.get("autor_slug", "autor"),
        documents=documents,
    )
