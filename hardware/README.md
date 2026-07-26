# Hardware

- `cad/` — modelos y planos (SolidWorks/Fusion + export a STEP y PDF).
- `electronica/` — esquemáticos y PCB (KiCad).
- `bom/` — lista de materiales con proveedor, referencia y precio.

Los archivos binarios pesados (STEP, STL) se versionan tal cual; si el
repositorio crece demasiado, migrar a Git LFS:

```bash
git lfs install
git lfs track "*.step" "*.stl" "*.f3d"
```
