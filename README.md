# citation-freshness-ci

Détecte les extraits de code cités qui ont bougé ou changé.

[Français](README.md) · [English](README.en.md) · [Español](README.es.md)

## Projets voisins

- [jevgrep — recherche de code avec extraits et lignes](https://github.com/dzhng/jevgrep)
- [Agent Retrieval Bench — localisation de code](https://agent-retrieval-bench.github.io/)

Ces projets documentent le besoin ou couvrent une partie du problème. Aucun lien d’affiliation ni intégration avec eux n’est revendiqué.

## Démarrer

```bash
python3 tool.py demo
python3 tool.py capture examples/source.py 1 2
```

Python 3.11+; no external package required. / Python 3.11+ ; aucune dépendance externe. / Python 3.11+; sin dependencias externas.

## Portée actuelle

`capture` produit un reçu JSON contenant chemin, lignes, extrait et SHA-256. `verify ROOT RECEIPT.json` distingue `exact`, `moved`, `stale`, `missing` et `ambiguous`. Cette version contrôle les fichiers locaux ; elle ne vérifie pas encore un commit Git.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Licence

MIT.
