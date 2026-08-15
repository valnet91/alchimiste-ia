<!-- GENERE depuis contracts/*.csv par tools/render_github.py -- NE PAS EDITER A LA MAIN -->
---
canonical: https://alchimiste-ia.com
author: Jean-Jacques Valognes
publisher: Alchimiste IA
rna: W912007379
---

# Alchimiste IA

> Architecture GEO, SEO technique et visibilité IA fondées sur des preuves vérifiables.
> https://alchimiste-ia.com/ · https://github.com/valnet91/alchimiste-ia · RNA W912007379

**[Voir et entendre les 10 contrôles](https://valnet91.github.io/alchimiste-ia/output/cards/)** — cartes + voix Henri / Denise.

## Scanner

- Site : [https://alchimiste-ia.com/](https://alchimiste-ia.com/)
- Audit AI-READY : [https://aiready.alchimiste-ia.com/index.html](https://aiready.alchimiste-ia.com/index.html)
- Consultant : [https://alchimiste-ia.com/consultant-ia/](https://alchimiste-ia.com/consultant-ia/)
- Cartes parlantes : [https://valnet91.github.io/alchimiste-ia/output/cards/](https://valnet91.github.io/alchimiste-ia/output/cards/)
- Dépôt : [https://github.com/valnet91/alchimiste-ia](https://github.com/valnet91/alchimiste-ia)
- Licence : [CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/) — citation obligatoire, pas d'œuvre dérivée. Voir [LICENSE](LICENSE) et [CITATION.cff](CITATION.cff).

## Sommaire

- [🧭 Scanner AI-READY, architecture AI-First](#scanner-ai-ready-architecture-ai-first)
- [🔐 Propriété, marque et souveraineté du domaine — P0](#propriete-marque-et-souverainete-du-domaine-p0)
- [🌐 DNS et propagation mondiale — P0](#dns-et-propagation-mondiale-p0)
- [🔒 HTTPS, certificats et en-têtes de sécurité — P0](#https-certificats-et-en-tetes-de-securite-p0)
- [📧 Emails, identité d’expéditeur et magic links — P0](#emails-identite-d-expediteur-et-magic-links-p0)
- [🔍 SEO technique et maîtrise de l’indexation — P0/P1](#seo-technique-et-maitrise-de-l-indexation-p0-p1)
- [🌍 SEO international des 19 langues — P1](#seo-international-des-19-langues-p1)
- [🤖 GEO, agents IA et données structurées — P1](#geo-agents-ia-et-donnees-structurees-p1)
- [⚡ Performance, accessibilité et HCI — P1](#performance-accessibilite-et-hci-p1)
- [💳 Intégrité du SaaS, paiement et conformité commerciale — P0](#integrite-du-saas-paiement-et-conformite-commerciale-p0)
- [📊 Observabilité, non-régression et continuité — P0/P1](#observabilite-non-regression-et-continuite-p0-p1)

<a id="scanner-ai-ready-architecture-ai-first"></a>
### 🧭 Scanner AI-READY, architecture AI-First

Alchimiste IA publie un référentiel de contrôles pour qu’un site soit lisible, vérifiable et citable par les moteurs et les agents. L’audit AI-READY inspecte le DOM, la sémantique, les données structurées, l’accès et les points de découverte. Le produit se lance depuis aiready.alchimiste-ia.com ; la méthode et le cabinet restent sur alchimiste-ia.com.

**Definition of Done :** Un visiteur peut ouvrir le site, comprendre l’offre, lancer l’audit et joindre le consultant sans JavaScript opaque ni URL inventée.

<a id="propriete-marque-et-souverainete-du-domaine-p0"></a>
### 🔐 Propriété, marque et souveraineté du domaine — P0

Je vérifie : compte registrar protégé par 2FA, verrouillage du transfert, renouvellement automatique et moyen de paiement de secours, adresse de récupération indépendante du domaine, accès partagé et documenté (pas uniquement détenu par le fondateur), disponibilité ou protection de la marque auprès de l’INPI/EUIPO, réservation des variantes (sans tiret, fautes fréquentes, .fr, comptes sociaux).

**Definition of Done :** La perte d’un téléphone, d’un collaborateur ou d’une carte bancaire ne peut pas provoquer la perte du domaine.

<a id="dns-et-propagation-mondiale-p0"></a>
### 🌐 DNS et propagation mondiale — P0

Je contrôle : A et éventuellement AAAA du domaine racine, CNAME des sous-domaines, cohérence entre www et domaine nu, serveurs NS redondants, TTL adaptés, CAA pour limiter les autorités de certification, DNSSEC si le registrar et l’hébergeur le permettent, absence de wildcard DNS inutile, résolution cohérente depuis plusieurs résolveurs (Google, Cloudflare, Quad9, serveurs autoritatifs).

**Definition of Done :** Tous les résolveurs retournent la même cible, sans SERVFAIL, boucle CNAME ou ancienne IP.

<a id="https-certificats-et-en-tetes-de-securite-p0"></a>
### 🔒 HTTPS, certificats et en-têtes de sécurité — P0

Je vérifie pour chaque hôte : certificat valide pour le domaine, www et les sous-domaines, redirection HTTP vers HTTPS en une seule étape, absence de contenu mixte, TLS moderne, en-têtes Strict-Transport-Security (après validation de tous les sous-domaines), Content-Security-Policy, X-Content-Type-Options nosniff, Referrer-Policy, Permissions-Policy, protection contre l’affichage en iframe via CSP frame-ancestors.

**Definition of Done :** Aucun avertissement navigateur, certificat supervisé et politique CSP testée sans casser Mollie, les formulaires ou le cockpit.

OWASP recommande ces en-têtes comme couche de défense contre le XSS, le clickjacking et les fuites d’information.

<a id="emails-identite-d-expediteur-et-magic-links-p0"></a>
### 📧 Emails, identité d’expéditeur et magic links — P0

Je contrôle : enregistrements MX, SPF unique et valide, DKIM actif, DMARC (d’abord en observation puis renforcé), sous-domaine dédié aux emails transactionnels, cohérence entre From, domaine DKIM et domaine des liens, traitement des rebonds et plaintes, expiration / usage unique / révocation des magic links, limitation des tentatives et anti-énumération des comptes.

**Definition of Done :** Les emails arrivent chez Gmail, Outlook et Proton sans spam, et un lien déjà utilisé ne peut plus ouvrir de session.

Pour un SaaS à liens magiques, l’email est une composante d’authentification, pas seulement un canal marketing.

<a id="seo-technique-et-maitrise-de-l-indexation-p0-p1"></a>
### 🔍 SEO technique et maîtrise de l’indexation — P0/P1

Je vérifie : codes HTTP réels (200, 301, 404, 410), un seul domaine canonique, balises title / description / canonical, un seul h1 pertinent par page, robots.txt, sitemap.xml ne contenant que les URL canoniques, inscription Google Search Console et Bing Webmaster Tools, pages privées / cockpit / paiements en noindex, pages d’erreur réellement servies en 404, liens internes sans dépendance exclusive au JavaScript.

**Definition of Done :** Les pages commerciales sont indexables ; les écrans d’authentification, de paiement et de cockpit ne le sont pas.

<a id="seo-international-des-19-langues-p1"></a>
### 🌍 SEO international des 19 langues — P1

Je vérifie : URL distincte par langue, attribut lang HTML correct, hreflang réciproques, x-default sur le sélecteur de langue, canonical vers la page de la même langue, titres / descriptions / JSON-LD localisés, sélecteur de langue accessible sur chaque page, aucune redirection forcée selon l’adresse IP, absence de mélange linguistique.

**Definition of Done :** Chaque page dispose de sa propre URL localisée, avec hreflang et canonical cohérents, sans redirection géographique forcée.

<a id="geo-agents-ia-et-donnees-structurees-p1"></a>
### 🤖 GEO, agents IA et données structurées — P1

Je distingue quatre niveaux : HTML réellement lisible sans exécution complexe, entités et données structurées cohérentes, documents citables / dates / sources, fichiers expérimentaux destinés aux agents. Je contrôle notamment : JSON-LD Organization / WebSite / SoftwareApplication / Product / Offer, cohérence entre prix visible / JSON-LD / CGV, pages méthode / documentation / sécurité / auteur, robots.txt par type d’agent si besoin, flux RSS / Atom ou changelog, /llms.txt lisible et structuré, sources primaires derrière chaque affirmation technique, date et version du référentiel de scoring.

llms.txt reste une proposition, pas une norme IETF ni une garantie de visibilité ou de citation. Il doit rester un bonus, jamais un critère bloquant devant l’HTML, le SEO, les données structurées et l’autorité éditoriale.

<a id="performance-accessibilite-et-hci-p1"></a>
### ⚡ Performance, accessibilité et HCI — P1

Je mesure : Core Web Vitals réels (LCP, INP, CLS), TTFB par région, poids HTML / CSS / JS / images, comportement mobile, parcours clavier, contraste et focus visible, textes alternatifs, labels des formulaires, annonces accessibles des erreurs, expérience quand JavaScript échoue, lisibilité des prix / CTA / confirmations.

**Definition of Done :** Une personne peut comprendre l’offre, renseigner son email, payer et consulter son rapport sur mobile, au clavier et avec une connexion médiocre.

Les Core Web Vitals doivent être mesurés sur l’expérience réelle des visiteurs, Lighthouse restant essentiellement un outil de diagnostic en laboratoire.

<a id="integrite-du-saas-paiement-et-conformite-commerciale-p0"></a>
### 💳 Intégrité du SaaS, paiement et conformité commerciale — P0

Je vérifie le parcours de bout en bout : création de compte, magic link, ajout de domaine, lancement du scan, limitation selon l’abonnement, paiement Mollie, signature et idempotence des webhooks, activation après paiement réellement confirmé, facture, renouvellement, résiliation, remboursement, suppression ou export des données, consentement newsletter distinct du service, identité juridique exacte sur toutes les pages.

**Definition of Done :** Aucun prix ni droit d’accès n’est codé manuellement dans plusieurs fichiers différents. Le prix affiché, le prix envoyé à Mollie, le montant facturé, le JSON-LD et les CGV viennent de la même source de vérité applicative.

<a id="observabilite-non-regression-et-continuite-p0-p1"></a>
### 📊 Observabilité, non-régression et continuité — P0/P1

Je mets en place : surveillance du domaine / DNS / certificat, tests synthétiques du site / login / paiement, suivi des erreurs front et back, journaux d’audit, alertes sur les échecs d’email et de webhook, mesure du tunnel visite-scan-email-compte-paiement, sauvegardes automatiques, test de restauration réel, contrôle SEO / GEO à chaque déploiement, politique de rollback, page de statut séparée, SLO mesurable et rapport mensuel.
