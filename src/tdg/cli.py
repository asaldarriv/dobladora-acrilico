"""CLI del proyecto:  uv run tdg <comando>"""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
import sys
from pathlib import Path

from . import config as cfg
from . import latex, verify

OK, WARN, ERR = "[ok]", "[!]", "[x]"


def _resolve(conf: cfg.Config, names: list[str], todos: bool) -> list[cfg.Document]:
    if todos or not names:
        return list(conf.documents.values())
    faltantes = [n for n in names if n not in conf.documents]
    if faltantes:
        disponibles = ", ".join(conf.documents)
        sys.exit(f"{ERR} Documento desconocido: {', '.join(faltantes)}. Disponibles: {disponibles}")
    return [conf.documents[n] for n in names]


def cmd_build(args: argparse.Namespace) -> int:
    conf = cfg.load()
    engine = latex.detect_engine(args.engine)
    print(f"Motor: {engine.name} ({engine.executable})")

    fallo = False
    for doc in _resolve(conf, args.documento, args.all):
        if not doc.tex.is_file():
            print(f"{WARN} {doc.name}: no existe {doc.tex.relative_to(conf.root)}; se omite.")
            continue
        outdir = conf.build_dir / doc.name
        print(f"\n-> {doc.titulo} ({doc.tex.relative_to(conf.root)})")
        try:
            pdf = latex.compile_document(doc.tex, outdir, conf.root, engine)
        except latex.CompilationError as exc:
            print(f"{ERR} {exc}")
            fallo = True
            continue

        reporte = verify.check_pages(pdf, doc)
        marca = OK if reporte.ok else ERR
        print(f"{marca} {pdf.relative_to(conf.root)} — {reporte}")
        if not reporte.ok:
            fallo = True

        if args.release:
            destino = _release(conf, doc, pdf)
            print(f"{OK} Entregable: {destino.relative_to(conf.root)}")

    return 1 if fallo else 0


def _release(conf: cfg.Config, doc: cfg.Document, pdf: Path) -> Path:
    conf.deliverables_dir.mkdir(parents=True, exist_ok=True)
    fecha = dt.date.today().isoformat()
    destino = conf.deliverables_dir / f"{fecha}_{doc.name}_{conf.autor_slug}.pdf"
    shutil.copy2(pdf, destino)
    return destino


def cmd_clean(_: argparse.Namespace) -> int:
    conf = cfg.load()
    if conf.build_dir.exists():
        shutil.rmtree(conf.build_dir)
        print(f"{OK} Eliminado {conf.build_dir.relative_to(conf.root)}/")
    else:
        print(f"{OK} Nada que limpiar.")
    return 0


def cmd_list(_: argparse.Namespace) -> int:
    conf = cfg.load()
    print(f"Repositorio: {conf.root}\n")
    for doc in conf.documents.values():
        limite = f"máx. {doc.max_content_pages} pág." if doc.has_page_limit else "sin límite"
        existe = "" if doc.tex.is_file() else "  (falta el .tex)"
        print(f"  {doc.name:<15} {doc.titulo:<22} {limite}{existe}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="tdg", description="Herramientas del trabajo de grado")
    sub = parser.add_subparsers(dest="comando", required=True)

    p_build = sub.add_parser("build", help="compila uno o varios documentos a PDF")
    p_build.add_argument("documento", nargs="*", help="nombre(s); vacío = todos")
    p_build.add_argument("--all", action="store_true", help="compila todos los documentos")
    p_build.add_argument("--engine", choices=latex.PREFERENCE, help="forzar un motor LaTeX")
    p_build.add_argument(
        "--release", action="store_true",
        help="copia el PDF a entregables/ con fecha y nombre del autor",
    )
    p_build.set_defaults(func=cmd_build)

    sub.add_parser("clean", help="borra el directorio build/").set_defaults(func=cmd_clean)
    sub.add_parser("list", help="lista los documentos configurados").set_defaults(func=cmd_list)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
