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

## Démo liée à jevgrep

Le parseur lit les blocs `Source block` numérotés dans la [sortie documentée de jevgrep](https://github.com/dzhng/jevgrep/blob/main/specs/done/jevgrep/assets/stdout-example.txt). Il crée des reçus à partir des extraits observés, puis les compare aux fichiers locaux :

```bash
python3 tool.py capture-jevgrep . examples/jevgrep-output.txt > receipts.json
python3 tool.py verify-batch . receipts.json
```

La fixture est synthétique et aucun appel à jevgrep ou à Jev n’est lancé. `capture-jevgrep` peut lire une vraie sortie enregistrée ; une source modifiée donne `stale` au contrôle.

## Exemple : extrait dupliqué

`python3 -m examples.ambiguous_span` crée deux copies identiques d’un extrait dans un fichier temporaire. Le reçu est encore valide, mais le contrôle renvoie `ambiguous` car une citation ne peut plus désigner une ligne unique. Aucune source réelle n’est modifiée.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Licence

MIT.
