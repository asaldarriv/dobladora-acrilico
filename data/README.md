# Datos experimentales

- `raw/` — datos tal como salen del equipo. **Nunca se editan a mano.**
- `processed/` — datos limpios generados por scripts de `src/tdg/analysis/`.

Formato esperado de los ensayos térmicos (Fase 1):

```csv
t_s,T_superior_C,T_inferior_C,T_lateral_C
0.0,24.8,24.7,24.6
1.0,31.2,26.0,25.1
```

Convención de nombres: `ensayo_<espesor>mm_<consigna>C_<n>.csv`
(por ejemplo `ensayo_3mm_155C_01.csv`).
