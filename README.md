# Alchimiste_Github

Usine **CSV-driven** pour le canal GitHub d’Alchimiste IA.
Compte public : [valnet91](https://github.com/valnet91). Pas de second user.

`contracts/` est la source de vérité. `output/` est dérivé : ne pas l’éditer à la main.

## Chaîne

```
contracts/site.csv + contracts/entries.csv
        ↓  python tools/render_github.py --write
output/README.md + output/llms.txt + output/controles/*.md
```

```powershell
$pythonProjet = 'D:\miniconda4\envs\Richou\python.exe'
Set-Location 'D:\miniconda5\Richou\Projets\_Archives\MiniProjet\Alchimiste_Github'
& $pythonProjet tools\render_github.py --check
& $pythonProjet tools\render_github.py --write
& $pythonProjet -m unittest discover -s tests -v
```

## Dates

`date_classement` sert à **ordonner** les fiches (idée Histoire et mémoire).
Ce n’est pas une date de création du compte GitHub, ni une date de commit.
Aucun script de ce dépôt ne pose `GIT_AUTHOR_DATE`. Le push reste manuel.

## Périmètre actuel

Les 10 contrôles indispensables + un encadré scanner AI-READY / AI-First,
avec uniquement des URL déjà publiées sur alchimiste-ia.com.
