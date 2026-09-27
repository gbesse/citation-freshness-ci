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

## Demo relacionada con jevgrep

El analizador lee bloques `Source block` numerados en la [salida documentada de jevgrep](https://github.com/dzhng/jevgrep/blob/main/specs/done/jevgrep/assets/stdout-example.txt). Crea recibos a partir de los fragmentos observados y los compara con archivos locales:

```bash
python3 tool.py capture-jevgrep . examples/jevgrep-output.txt > receipts.json
python3 tool.py verify-batch . receipts.json
```

El ejemplo es sintético y no llama a jevgrep ni a Jev. `capture-jevgrep` puede leer una salida real guardada; una fuente modificada produce `stale` al verificar.

## Pruebas

```bash
python3 -m unittest discover -s tests -v
```

## Licencia

MIT.
