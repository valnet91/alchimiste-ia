<!-- GENERE depuis contracts/*.csv par tools/render_github.py -- NE PAS EDITER A LA MAIN -->
---
canonical: https://alchimiste-ia.com
id: controle-02-dns
date_classement: 2026-08-14
categorie: controles-indispensables
---

# 🌐 DNS et propagation mondiale — P0

Je contrôle : A et éventuellement AAAA du domaine racine, CNAME des sous-domaines, cohérence entre www et domaine nu, serveurs NS redondants, TTL adaptés, CAA pour limiter les autorités de certification, DNSSEC si le registrar et l’hébergeur le permettent, absence de wildcard DNS inutile, résolution cohérente depuis plusieurs résolveurs (Google, Cloudflare, Quad9, serveurs autoritatifs).

**Definition of Done :** Tous les résolveurs retournent la même cible, sans SERVFAIL, boucle CNAME ou ancienne IP.
