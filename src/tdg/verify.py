"""Verificación del límite de páginas exigido por el reglamento.

El reglamento del Programa de Ingeniería Física no cuenta portada, índices ni
sección de referencias dentro del límite de páginas. Esta verificación
descuenta esas páginas y compara el resto contra `max_content_pages`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

from .config import Document


@dataclass(frozen=True)
class PageReport:
    total: int
    content: int
    limit: int

    @property
    def ok(self) -> bool:
        return self.limit <= 0 or self.content <= self.limit

    def __str__(self) -> str:
        if self.limit <= 0:
            return f"{self.total} páginas totales ({self.content} de contenido, sin límite)"
        estado = "OK" if self.ok else "EXCEDE"
        return (
            f"{self.content}/{self.limit} páginas de contenido efectivo "
            f"[{estado}] — {self.total} páginas totales"
        )


def check_pages(pdf: Path, doc: Document) -> PageReport:
    total = len(PdfReader(pdf).pages)
    content = total - doc.front_pages - doc.back_pages
    return PageReport(total=total, content=content, limit=doc.max_content_pages)
