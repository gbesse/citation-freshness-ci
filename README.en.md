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

## Jevgrep-related demo

The parser reads numbered `Source block` sections in [jevgrep's documented output](https://github.com/dzhng/jevgrep/blob/main/specs/done/jevgrep/assets/stdout-example.txt). It creates receipts from observed excerpts and compares them with local files:

```bash
python3 tool.py capture-jevgrep . examples/jevgrep-output.txt > receipts.json
python3 tool.py verify-batch . receipts.json
```

The fixture is synthetic; neither jevgrep nor Jev is called. `capture-jevgrep` can read a saved real output; changed source returns `stale` on verification.

## Example: duplicated excerpt

`python3 -m examples.ambiguous_span` creates two identical copies of an excerpt in a temporary file. The receipt is still valid, but verification returns `ambiguous` because the citation no longer identifies a unique line. No real source file is changed.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT.

## Adoption check

[Try a concrete case and check its limits](examples/adoption-check.md).
