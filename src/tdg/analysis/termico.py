"""Curvas de calentamiento del PMMA (Fase 1 de la metodología).

Lee un CSV de `data/raw/` con columnas:
    t_s, T_superior_C, T_inferior_C, T_lateral_C
y genera una figura vectorial en `assets/figuras/`, lista para \\includegraphics.

Uso:
    uv run --extra analisis python -m tdg.analysis.termico data/raw/ensayo_3mm.csv
"""

from __future__ import annotations

import sys
from pathlib import Path

from ..config import load

TG_PMMA_C = 105.0        # temperatura de transición vítrea
T_CONFORMADO_C = (150.0, 160.0)   # ventana de conformado por línea térmica


def graficar(csv: Path, salida: Path | None = None) -> Path:
    import matplotlib.pyplot as plt
    import pandas as pd

    conf = load()
    salida = salida or conf.root / "assets" / "figuras" / f"{csv.stem}.pdf"
    salida.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    for col in (c for c in df.columns if c != "t_s"):
        ax.plot(df["t_s"], df[col], label=col.replace("_", " "))

    ax.axhline(TG_PMMA_C, ls="--", lw=0.9, color="gray")
    ax.annotate(r"$T_g \approx 105\,^\circ$C", (0.02, TG_PMMA_C + 3), xycoords=("axes fraction", "data"),
                fontsize=8, color="gray")
    ax.axhspan(*T_CONFORMADO_C, alpha=0.12, color="tab:red", label="ventana de conformado")

    ax.set_xlabel("Tiempo [s]")
    ax.set_ylabel(r"Temperatura [$^\circ$C]")
    ax.legend(fontsize=8, frameon=False)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(salida)
    return salida


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    print(f"Figura generada: {graficar(Path(sys.argv[1]))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
