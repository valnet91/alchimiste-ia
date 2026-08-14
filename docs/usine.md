# Usine Alchimiste_Github

Notice interne. Le README public du dépôt est généré à la **racine**
(`README.md`) depuis les CSV. Ne pas l’éditer à la main.

Compte public : [valnet91](https://github.com/valnet91). Pas de second user.

`contracts/` est la source de vérité. `README.md`, `output/llms.txt`,
`output/controles/` et `output/cards/` sont dérivés.

## Chaîne

```
contracts/site.csv + contracts/entries.csv
        ↓  python tools/render_github.py --write
README.md + output/llms.txt + output/controles/*.md
```

```powershell
$pythonProjet = 'D:\miniconda4\envs\Richou\python.exe'
Set-Location 'D:\miniconda5\Richou\Projets\_Archives\MiniProjet\Alchimiste_Github'
& $pythonProjet tools\render_github.py --check
& $pythonProjet tools\render_github.py --write
& $pythonProjet tools\render_cards.py --write
& $pythonProjet tools\render_cards.py --write --audio
& $pythonProjet -m unittest discover -s tests -v
```

Cartes : `contracts/cards.csv` → `output/cards/*.webp` (+ `.mp3` si `--audio`)
et `output/cards/index.html` (micro-page : image + bouton d’écoute).
Pour la démo en ligne : GitHub Pages, source `main`, dossier `/` ;
URL : `https://valnet91.github.io/alchimiste-ia/output/cards/`.
EXIF/XMP via `exiftool`. GPS seulement si `gps_lat` **et** `gps_lon` sont remplis.
Voix : `henri`, `denise`, ou `duo` (Henri puis Denise, une ligne chacun).

## Dates

`date_classement` sert à **ordonner** les fiches (idée Histoire et mémoire).
Ce n’est pas une date de création du compte GitHub, ni une date de commit.
Aucun script de ce dépôt ne pose `GIT_AUTHOR_DATE`. Le push reste manuel.

## Périmètre actuel

Les 10 contrôles indispensables + un encadré scanner AI-READY / AI-First,
avec uniquement des URL déjà publiées sur alchimiste-ia.com.
