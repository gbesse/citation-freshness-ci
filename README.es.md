# citation-freshness-ci

Detecta fragmentos de código citados que se han movido o cambiado.

[Français](README.md) · [English](README.en.md) · [Español](README.es.md)

## Proyectos relacionados

- [jevgrep — búsqueda de código con fragmentos y líneas](https://github.com/dzhng/jevgrep)
- [Agent Retrieval Bench — evaluación de localización de código](https://agent-retrieval-bench.github.io/)

Estos proyectos documentan la necesidad o cubren parte del problema. No se afirma ninguna afiliación ni integración con ellos.

## Inicio rápido

```bash
python3 tool.py demo
python3 tool.py capture examples/source.py 1 2
```

Python 3.11+; no external package required. / Python 3.11+ ; aucune dépendance externe. / Python 3.11+; sin dependencias externas.

## Alcance actual

`capture` genera un recibo JSON con ruta, líneas, fragmento y SHA-256. `verify ROOT RECEIPT.json` distingue `exact`, `moved`, `stale`, `missing` y `ambiguous`. Esta versión comprueba archivos locales; todavía no verifica un commit de Git.

## Pruebas

```bash
python3 -m unittest discover -s tests -v
```

## Licencia

MIT.
