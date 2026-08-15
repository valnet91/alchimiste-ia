# About et social preview (UI GitHub)

Le README généré porte déjà le lien Pages. About et l’image d’aperçu se règlent sur le dépôt.

1. Ouvrir [github.com/valnet91/alchimiste-ia](https://github.com/valnet91/alchimiste-ia)
2. À droite, **About** → roue dentée
3. Description : `Référentiel public AI-READY / AI-First : 10 contrôles, cartes parlantes, GEO.`
4. Website : `https://alchimiste-ia.com`
5. Topics : `geo` `seo` `ai` `llms-txt` `france`
6. **Social preview** : envoyer `.github/social-preview.png` (1280×640)

Ou en CLI, si `gh` est connecté en valnet91 :

```powershell
gh repo edit valnet91/alchimiste-ia --description "Référentiel public AI-READY / AI-First : 10 contrôles, cartes parlantes, GEO." --homepage "https://alchimiste-ia.com" --add-topic geo --add-topic seo --add-topic ai --add-topic llms-txt --add-topic france
```

Profil GitHub : remplacer `README.md` du dépôt [valnet91/valnet91](https://github.com/valnet91/valnet91) par `docs/profile-readme.md`.
