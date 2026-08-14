<!-- GENERE depuis contracts/*.csv par tools/render_github.py -- NE PAS EDITER A LA MAIN -->
---
canonical: https://alchimiste-ia.com
id: controle-09-saas-paiement
date_classement: 2026-08-14
categorie: controles-indispensables
---

# 💳 Intégrité du SaaS, paiement et conformité commerciale — P0

Je vérifie le parcours de bout en bout : création de compte, magic link, ajout de domaine, lancement du scan, limitation selon l’abonnement, paiement Mollie, signature et idempotence des webhooks, activation après paiement réellement confirmé, facture, renouvellement, résiliation, remboursement, suppression ou export des données, consentement newsletter distinct du service, identité juridique exacte sur toutes les pages.

**Definition of Done :** Aucun prix ni droit d’accès n’est codé manuellement dans plusieurs fichiers différents. Le prix affiché, le prix envoyé à Mollie, le montant facturé, le JSON-LD et les CGV viennent de la même source de vérité applicative.
