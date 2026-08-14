<!-- GENERE depuis contracts/*.csv par tools/render_github.py -- NE PAS EDITER A LA MAIN -->
---
canonical: https://alchimiste-ia.com
id: controle-03-https
date_classement: 2026-08-14
categorie: controles-indispensables
---

# 🔒 HTTPS, certificats et en-têtes de sécurité — P0

Je vérifie pour chaque hôte : certificat valide pour le domaine, www et les sous-domaines, redirection HTTP vers HTTPS en une seule étape, absence de contenu mixte, TLS moderne, en-têtes Strict-Transport-Security (après validation de tous les sous-domaines), Content-Security-Policy, X-Content-Type-Options nosniff, Referrer-Policy, Permissions-Policy, protection contre l’affichage en iframe via CSP frame-ancestors.

**Definition of Done :** Aucun avertissement navigateur, certificat supervisé et politique CSP testée sans casser Mollie, les formulaires ou le cockpit.

OWASP recommande ces en-têtes comme couche de défense contre le XSS, le clickjacking et les fuites d’information.
