<!-- GENERE depuis contracts/*.csv par tools/render_github.py -- NE PAS EDITER A LA MAIN -->
---
canonical: https://alchimiste-ia.com
id: controle-04-emails
date_classement: 2026-08-14
categorie: controles-indispensables
---

# 📧 Emails, identité d’expéditeur et magic links — P0

Je contrôle : enregistrements MX, SPF unique et valide, DKIM actif, DMARC (d’abord en observation puis renforcé), sous-domaine dédié aux emails transactionnels, cohérence entre From, domaine DKIM et domaine des liens, traitement des rebonds et plaintes, expiration / usage unique / révocation des magic links, limitation des tentatives et anti-énumération des comptes.

**Definition of Done :** Les emails arrivent chez Gmail, Outlook et Proton sans spam, et un lien déjà utilisé ne peut plus ouvrir de session.

Pour un SaaS à liens magiques, l’email est une composante d’authentification, pas seulement un canal marketing.
