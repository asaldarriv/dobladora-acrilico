# Dobladora automática de acrílico

Trabajo de grado — Ingeniería Física, Universidad EAFIT (2026-2)
Alexander Saldarriaga Vélez · Asesor: Hugo Alberto Murillo Hoyos

Repositorio único para los documentos LaTeX, el firmware de Arduino, el
análisis de datos y los archivos de hardware del proyecto.

---

## 1. Requisitos

| Herramienta | Para qué | Instalación (Windows / bash) |
|---|---|---|
| [uv](https://docs.astral.sh/uv/) | Python y dependencias | `winget install astral-sh.uv` |
| [Tectonic](https://tectonic-typesetting.github.io/) | compilar LaTeX | `curl -L -o ~/Downloads/tectonic.zip https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.16.9/tectonic-0.16.9-x86_64-pc-windows-msvc.zip`<br>`mkdir -p ~/bin/tectonic`<br>`unzip ~/Downloads/tectonic.zip -d ~/bin/tectonic`<br>`echo 'export PATH="$HOME/bin/tectonic:$PATH"' >> ~/.bashrc`<br>`source ~/.bashrc` |
| Git | versionado | `winget install Git.Git` |
| [arduino-cli](https://arduino.github.io/arduino-cli/) | firmware (opcional) | `winget install ArduinoSA.CLI` |

Tectonic es un binario único: descarga por su cuenta solo los paquetes LaTeX que
el documento necesita y hace las pasadas de compilación automáticamente. La
primera compilación tarda un poco más porque llena su caché.

Si ya descargaste `tectonic.exe`, también puedes usarlo sin instalar nada más:

```bash
"/c/Users/Usuario/Downloads/tectonic.exe" --version
```

Si prefieres dejarlo fijo en tu `PATH` de bash, cópialo a una carpeta como `~/bin`
y añade esa ruta a `~/.bashrc`:

```bash
mkdir -p ~/bin
cp "/c/Users/Usuario/Downloads/tectonic.exe" ~/bin/
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
tectonic --version
```

Cierra y vuelve a abrir la terminal después de instalar, para que el `PATH` se refresque.

## 2. Puesta en marcha

```powershell
git clone <url-de-tu-repo>
cd dobladora-acrilico
uv sync                 # crea .venv e instala dependencias
uv run tdg list         # lista los documentos configurados
uv run tdg build anteproyecto
```

El PDF queda en `build/anteproyecto/main.pdf`.

## 3. Uso diario

```powershell
uv run tdg build anteproyecto              # compila y verifica el límite de páginas
uv run tdg build --all                     # compila todos los documentos
uv run tdg build anteproyecto --release    # además copia el PDF a entregables/
uv run tdg build anteproyecto --engine latexmk   # forzar otro motor
uv run tdg clean                           # borra build/
uv run pytest                              # pruebas
uv run ruff check .                        # linter
```

`tdg build` **verifica automáticamente el límite del reglamento**: descuenta la
portada, el índice y la bibliografía, y avisa si el contenido efectivo pasa de
5 páginas en el anteproyecto. Si excede, el comando devuelve código de salida 1.

Los límites se declaran en `pyproject.toml`, en `[tool.tdg.documents.*]`.

## 4. Estructura

```
.
├── docs/                      # documentos LaTeX
│   ├── comun/                 #   preámbulo, portada y bibliografía compartidos
│   ├── anteproyecto/          #   main.tex + secciones/
│   ├── avance/
│   └── informe-final/
├── src/tdg/                   # herramientas Python
│   ├── cli.py                 #   comando `tdg`
│   ├── latex.py               #   compilación (Tectonic / latexmk / xelatex)
│   ├── verify.py              #   verificación del límite de páginas
│   └── analysis/              #   análisis de datos experimentales
├── firmware/dobladora/        # código Arduino
├── hardware/                  # CAD, electrónica, BOM
├── data/{raw,processed}/      # datos de los ensayos
├── assets/{figuras,fotos}/    # imágenes para los documentos
├── entregables/               # PDF enviados a Interactiva (versionados)
└── build/                     # salidas de compilación (ignorado por git)
```

### Cómo agregar una imagen

Guárdala en `assets/figuras/` y en el `.tex` escribe solo el nombre:

```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.8\linewidth]{curva-calentamiento-3mm}
  \caption{Curva de calentamiento para \SI{3}{\milli\meter}.}
  \label{fig:curva-3mm}
\end{figure}
```

El preámbulo ya declara `\graphicspath` con `assets/figuras/`, `assets/fotos/` y
`assets/logos/`, así que no hace falta escribir la ruta completa. Prefiere PDF o
SVG para gráficas (vectorial) y JPG para fotos.

### Cómo agregar un documento nuevo

1. Crea `docs/<nombre>/main.tex` (copia el de `avance` como plantilla).
2. Añade su bloque en `pyproject.toml`:

```toml
[tool.tdg.documents.presentacion]
tex = "docs/presentacion/main.tex"
titulo = "Sustentación"
front_pages = 0
back_pages = 0
max_content_pages = 0
```

## 5. Análisis de datos

```powershell
uv sync --extra analisis
uv run python -m tdg.analysis.termico data/raw/ensayo_3mm_155C_01.csv
```

Genera una figura en `assets/figuras/` lista para incluir en el informe.

## 6. Relación con Overleaf

El preámbulo funciona igual en **pdfLaTeX** (Overleaf) y en **XeLaTeX**
(Tectonic local), así que el PDF sale idéntico en ambos.

Para trabajar también en Overleaf, usa su integración con GitHub
(*Menu → GitHub → Import/Sync*) y en Overleaf marca `docs/anteproyecto/main.tex`
como documento principal. Git sigue siendo la fuente de verdad.

## 7. Flujo de trabajo con git

```powershell
git switch -c avance/caracterizacion-termica
# ... editar ...
git add docs/ assets/
git commit -m "docs(anteproyecto): precisar tolerancia angular objetivo"
git push -u origin avance/caracterizacion-termica
```

Etiqueta cada entrega para poder volver a ella:

```powershell
git tag -a entrega/anteproyecto -m "Anteproyecto entregado 2026-07-27"
git push --tags
```
