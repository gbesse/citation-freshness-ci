# citation-freshness-ci

Detects cited code snippets that have moved or changed.

[Français](README.md) · [English](README.en.md) · [Español](README.es.md)

## Related projects

- [jevgrep — code search with snippets and line numbers](https://github.com/dzhng/jevgrep)
- [Agent Retrieval Bench — code location benchmark](https://agent-retrieval-bench.github.io/)

These projects document the need or cover part of the problem. No affiliation or integration with them is claimed.

## Quick start

```bash
python3 tool.py demo
python3 tool.py capture examples/source.py 1 2
```

Python 3.11+; no external package required. / Python 3.11+ ; aucune dépendance externe. / Python 3.11+; sin dependencias externas.

## Current scope

`capture` emits a JSON receipt with path, lines, excerpt and SHA-256. `verify ROOT RECEIPT.json` distinguishes `exact`, `moved`, `stale`, `missing` and `ambiguous`. This version checks local files; it does not yet verify a Git commit.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT.
