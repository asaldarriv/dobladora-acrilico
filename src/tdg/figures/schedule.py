"""Cronograma del trabajo de grado como diagrama de Gantt vectorial.

Genera `assets/figuras/cronograma.pdf`, que el anteproyecto incluye con
\\includegraphics. El calendario (semana 1, semana de receso) y los datos
—ACTIVITIES y MILESTONES— están declarados arriba: para replanear, edítalos
ahí y vuelve a ejecutar el script.

El eje x son las 18 semanas del período 2026-2: la semana `n` ocupa el
intervalo [n-1, n], de modo que una actividad de la semana 3 a la 8 se dibuja
de x=2 a x=8.

Uso:
    uv run --extra analisis python -m tdg.figures.schedule
    uv run --extra analisis python -m tdg.figures.schedule --png   # vista rápida
"""

from __future__ import annotations

import argparse
import datetime as dt
from dataclasses import dataclass
from pathlib import Path

from ..config import load

# --------------------------------------------------------------------------
#  Calendario del período académico 2026-2
# --------------------------------------------------------------------------
WEEK_1_MONDAY = dt.date(2026, 7, 13)
BREAK_AFTER_WEEK = 8              # la semana de receso va después de esta
WEEKS = 18

MONTHS = ["ene", "feb", "mar", "abr", "may", "jun",
          "jul", "ago", "sep", "oct", "nov", "dic"]


# --------------------------------------------------------------------------
#  Datos del cronograma
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class Activity:
    name: str
    start: int           # primera semana, inclusive
    end: int             # última semana, inclusive
    group: str           # clave de COLORS / LABELS


@dataclass(frozen=True)
class Milestone:
    name: str
    week: int
    date: str            # etiqueta corta que se imprime al margen derecho


ACTIVITIES = [
    Activity("Revisión bibliográfica", 1, 4, "documentation"),
    Activity("F1. Caracterización térmica", 3, 8, "development"),
    Activity("F2. Subsistema térmico", 5, 8, "development"),
    Activity("F3. Diseño mecánico y CAD", 7, 10, "development"),
    Activity("F4. Control PID e interfaz", 9, 12, "development"),
    Activity("F5. Fabricación e integración", 9, 12, "development"),
    Activity("F6. Validación experimental", 11, 14, "development"),
    Activity("F7. Documentación del proyecto", 3, 15, "documentation"),
    Activity("Entrega del prototipo", 15, 16, "documentation"),
    Activity("Preparación de la defensa", 15, 18, "documentation"),
]

MILESTONES = [
    Milestone("Anteproyecto y sustentación", 3, "27 jul."),
    Milestone("Informe 1 de avance", 8, "31 ago."),
    Milestone("Informe 2 de avance", 14, "19 oct."),
    Milestone("Informe final y carta de aval", 15, "30 oct."),
    Milestone("Defensa pública", 18, "20 nov."),
]

# --------------------------------------------------------------------------
#  Estilo (paleta validada; azul y naranja se distinguen también en escala de
#  grises y bajo daltonismo, y los hitos usan tinta neutra, no un tercer color)
# --------------------------------------------------------------------------
COLORS = {
    "development": "#2a78d6",
    "documentation": "#eb6834",
    "milestone": "#0b0b0b",
    "grid": "#e6e5de",
    "secondary": "#52514e",
    "muted": "#898781",
    "surface": "#ffffff",
}

LABELS = {
    "development": "Desarrollo técnico",
    "documentation": "Documentación y cierre",
}

WIDTH_IN = 6.14      # = 15,6 cm de \linewidth: la figura se inserta sin escalar
HEIGHT_IN = 3.1
BAR_WIDTH_PT = 5.0
BLOCK_GAP = 0.8      # filas en blanco entre actividades e hitos
TOP_MARGIN = 1.1     # filas libres arriba, para la marca del receso


def monday_of(week: int) -> dt.date:
    """Lunes de la semana académica `week`, contando el receso."""
    recess = 7 if week > BREAK_AFTER_WEEK else 0
    return WEEK_1_MONDAY + dt.timedelta(days=7 * (week - 1) + recess)


def month_spans() -> list[tuple[str, float]]:
    """Nombre del mes y centro (en coordenadas de semana) de cada tramo."""
    spans: list[list] = []
    for week in range(1, WEEKS + 1):
        month = monday_of(week).month
        if spans and spans[-1][0] == month:
            spans[-1][2] = week
        else:
            spans.append([month, week - 1, week])
    return [(MONTHS[month - 1], (start + end) / 2) for month, start, end in spans]


def _bar(ax, y: float, activity: Activity) -> None:
    """Barra de extremos redondeados; el margen compensa el ancho del cap."""
    inset = 0.10
    ax.plot([activity.start - 1 + inset, activity.end - inset], [y, y],
            color=COLORS[activity.group], lw=BAR_WIDTH_PT,
            solid_capstyle="round", zorder=3)


def build(output: Path | None = None, png: bool = False) -> Path:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
        "font.size": 6.5,
        "pdf.fonttype": 42,      # TrueType embebido: texto seleccionable en el PDF
        "svg.fonttype": "none",
    })

    conf = load()
    name = "cronograma.png" if png else "cronograma.pdf"
    output = output or conf.root / "assets" / "figuras" / name
    output.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(WIDTH_IN, HEIGHT_IN))
    fig.patch.set_facecolor(COLORS["surface"])
    ax.set_facecolor(COLORS["surface"])
    fig.subplots_adjust(left=0.265, right=0.925, top=0.905, bottom=0.185)

    activity_rows = list(range(len(ACTIVITIES)))
    divider = len(ACTIVITIES) - 1 + BLOCK_GAP
    milestone_rows = [divider + 1 + i for i in range(len(MILESTONES))]
    last_row = milestone_rows[-1]

    for y, activity in zip(activity_rows, ACTIVITIES):
        _bar(ax, y, activity)

    # Separador entre el bloque de actividades y el de hitos
    ax.axhline(divider, color=COLORS["grid"], lw=0.6, zorder=1)

    for y, milestone in zip(milestone_rows, MILESTONES):
        ax.plot(milestone.week - 0.5, y, marker="D", ms=4.0,
                color=COLORS["milestone"], markeredgecolor=COLORS["surface"],
                markeredgewidth=1.2, zorder=4, clip_on=False)
        ax.text(1.015, y, milestone.date, transform=ax.get_yaxis_transform(),
                va="center", ha="left", fontsize=6.2, color=COLORS["secondary"])

    # ---- Ejes -------------------------------------------------------------
    ax.set_xlim(0, WEEKS)
    ax.set_ylim(last_row + 0.8, -TOP_MARGIN)   # y crece hacia abajo

    ax.set_yticks(activity_rows + milestone_rows)
    ax.set_yticklabels([a.name for a in ACTIVITIES] + [m.name for m in MILESTONES])

    ax.set_xticks([n - 0.5 for n in range(1, WEEKS + 1)])
    ax.set_xticklabels([str(n) for n in range(1, WEEKS + 1)])
    ax.set_xticks(range(WEEKS + 1), minor=True)
    ax.xaxis.set_ticks_position("top")
    ax.tick_params(axis="x", which="both", length=0, pad=3,
                   labelsize=6.5, colors=COLORS["secondary"])
    ax.tick_params(axis="y", length=0, pad=4, labelsize=6.5, colors=COLORS["secondary"])
    ax.grid(axis="x", which="minor", color=COLORS["grid"], lw=0.4)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.text(-0.012, 1.0, "Semana", transform=ax.transAxes, ha="right", va="center",
            fontsize=6.5, color=COLORS["muted"])

    # Franja de meses bajo el eje
    for month, center in month_spans():
        ax.text(center, -0.045, month, transform=ax.get_xaxis_transform(),
                ha="center", va="top", fontsize=6.5, color=COLORS["muted"])

    # Semana de receso: no ocupa columna, se marca en la frontera
    ax.plot([BREAK_AFTER_WEEK] * 2, [-0.55, last_row + 0.8],
            color=COLORS["muted"], lw=0.7, ls=(0, (2, 2)), zorder=1)
    ax.text(BREAK_AFTER_WEEK, -0.95, "receso", ha="center", va="center",
            fontsize=6, color=COLORS["muted"])

    # ---- Leyenda ----------------------------------------------------------
    keys = [
        Line2D([], [], color=COLORS["development"], lw=5,
               solid_capstyle="round", label=LABELS["development"]),
        Line2D([], [], color=COLORS["documentation"], lw=5,
               solid_capstyle="round", label=LABELS["documentation"]),
        Line2D([], [], color=COLORS["milestone"], marker="D", ms=4.0, lw=0,
               label="Hito evaluativo"),
    ]
    ax.legend(handles=keys, loc="upper center", bbox_to_anchor=(0.5, -0.11),
              ncol=3, frameon=False, fontsize=6.5, handlelength=1.6,
              columnspacing=1.8, handletextpad=0.6, labelcolor=COLORS["secondary"])

    fig.savefig(output, dpi=300 if png else None, facecolor=COLORS["surface"])
    plt.close(fig)
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--png", action="store_true",
                        help="genera PNG en vez de PDF (vista rápida)")
    parser.add_argument("-o", "--output", type=Path, help="ruta de salida explícita")
    args = parser.parse_args(argv)

    print(f"Figura generada: {build(args.output, png=args.png)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
