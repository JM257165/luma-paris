# PRD : Luma Event Scraper (Tech / IA)

**Auteur :** —
**Date :** 11 juillet 2026
**Statut :** Brouillon
**Version :** 1.0

---

## 1. Résumé

Un scraper automatisé qui découvre chaque jour les nouveaux événements publiés
sur Luma (lu.ma) dans les catégories **tech** et **ai**, et récupère le nom
et le lien de chaque événement pour un usage ultérieur (dashboard, newsletter,
notification vers un canal, etc.).

## 2. Problème / Motivation

Luma n'offre pas d'API publique officielle pour les tiers, ni de mécanisme
natif d'alertes par catégorie/thème en dehors de sa newsletter hebdomadaire
par ville. Pour quelqu'un qui veut suivre activement l'écosystème des
événements tech/IA (pour y assister, promouvoir, faire de la recherche
communautaire, générer des leads, etc.), la seule solution aujourd'hui est de
consulter manuellement la page Discover tous les jours : c'est lent et on
risque fortement de manquer des événements.

## 3. Objectif

Automatiser la détection des nouveaux événements tech/IA sur Luma, avec une
exécution une fois par jour, sans dépendre d'une API officielle ni d'une
intervention manuelle.

## 4. Périmètre

### 4.1 Dans le périmètre (v1)
- Consulter les événements des catégories `tech` et `ai`.
- Couverture multi-villes (liste de coordonnées configurable) pour atténuer le
  biais géographique de l'endpoint de découverte.
- Déduplication entre les exécutions (ne signaler que les événements réellement nouveaux).
- Persistance de :
  - L'état des événements déjà vus.
  - L'historique cumulé de tous les événements (CSV maître).
  - Un fichier quotidien ne contenant que les nouveaux événements détectés.
- Exécution planifiée une fois par jour (cron ou GitHub Actions).
- Gestion des erreurs avec relances et backoff en cas de panne réseau.

### 4.2 Hors périmètre (v1)
- Authentification / scraping des listes de participants (nécessite un cookie
  de session — complexité juridique et technique plus élevée).
- Notifications push automatiques (Slack/Telegram/e-mail) — proposées pour la v2.
- Enrichissement des données des hôtes (réseaux sociaux, biographies).
- Filtrage sémantique par mots-clés ou pertinence (au-delà de la catégorie
  native de Luma).
- Interface / dashboard de visualisation.
- Déduplication sémantique entre événements aux noms similaires, même
  organisateur (la déduplication se fait uniquement par `api_id`).

## 5. Utilisateurs / Cas d'usage

| Utilisateur | Cas d'usage |
|---|---|
| Personne intéressée par les événements tech/IA | Recevoir un flux quotidien des nouveaux événements sans consulter Luma manuellement |
| Community manager / organisateur | Détecter les événements de la concurrence ou de l'écosystème pour un benchmark |
| Équipe growth / partenariats | Identifier les événements où il vaut la peine d'être présent ou de sponsoriser |

## 6. Exigences fonctionnelles

| ID | Exigence | Priorité |
|---|---|---|
| RF-1 | Le système doit interroger l'endpoint de découverte de Luma pour chaque combinaison de catégorie configurée (`tech`, `ai`) et de ville configurée. | Haute |
| RF-2 | Le système doit paginer automatiquement les résultats jusqu'à épuisement de la liste ou jusqu'à une limite de sécurité de pages. | Haute |
| RF-3 | Le système doit identifier chaque événement de manière unique (`api_id`) pour éviter les doublons entre exécutions. | Haute |
| RF-4 | Le système doit persister sur disque l'ensemble des événements déjà vus entre les exécutions. | Haute |
| RF-5 | Le système doit générer un fichier ne contenant que les nouveaux événements détectés lors de l'exécution en cours, avec au minimum : nom, lien, date de début, ville, catégorie. | Haute |
| RF-6 | Le système doit tenir un historique cumulé (append-only) de tous les événements détectés depuis le début. | Moyenne |
| RF-7 | Le système doit pouvoir s'exécuter de façon non surveillée et planifiée (sans intervention manuelle) au moins une fois par jour. | Haute |
| RF-8 | Le système doit relancer automatiquement en cas de panne réseau passagère, avec un backoff progressif. | Moyenne |
| RF-9 | Le système doit journaliser (logging) chaque exécution : nombre d'événements consultés, nombre de nouveaux, et erreurs rencontrées. | Moyenne |
| RF-10 | La liste des villes et catégories à interroger doit être configurable sans modifier la logique centrale du script. | Moyenne |

## 7. Exigences non fonctionnelles

| ID | Exigence |
|---|---|
| RNF-1 | **Pas de dépendance à une API officielle** : le système ne doit requérir ni clé d'API ni accès autorisé de Luma. |
| RNF-2 | **Respectueux du serveur cible** : pauses aléatoires entre les requêtes, sans concurrence agressive. |
| RNF-3 | **Résilience aux changements de schéma** : un échec de parsing d'un champ ne doit pas interrompre l'exécution complète ; il doit être journalisé et le traitement doit continuer. |
| RNF-4 | **Portabilité** : doit fonctionner avec Python standard (sans dépendances externes obligatoires) pour simplifier le déploiement en cron/CI. |
| RNF-5 | **Coût** : doit pouvoir fonctionner sur un runner gratuit (ex. offre gratuite de GitHub Actions) sans infrastructure payante. |
| RNF-6 | **Traçabilité** : tout nouvel événement doit être tracé avec la date à laquelle il a été détecté pour la première fois (`first_seen`). |

## 8. Conception de la solution (haut niveau)

1. **Source de données** : endpoint JSON non documenté utilisé par le frontend
   de Luma lui-même (`api.luma.com/discover/get-paginated-events`), interrogé
   par `slug` de catégorie + coordonnées.
2. **Orchestration** : script Python exécuté par un planificateur externe
   (cron / GitHub Actions / timer systemd) — le script ne conserve aucun état
   en mémoire entre les exécutions ; tout l'état vit dans des fichiers locaux.
3. **Stockage** (dossier `data/`) :
   - `data/seen_events.json` — index de déduplication.
   - `data/events_master.csv` — historique complet.
   - `data/new_events/new_events_<date>.csv` — sortie du jour.
4. **Planification** : 1 exécution par jour (horaire configurable).

## 9. Métriques de succès

| Métrique | Objectif v1 |
|---|---|
| Nouveaux événements détectés par semaine | > 0 de façon régulière (vérifier que le pipeline fonctionne) |
| Taux d'erreur des exécutions (échecs non récupérés) | < 5 % des exécutions planifiées |
| Faux doublons (événement signalé comme nouveau plus d'une fois) | 0 |
| Couverture géographique | Au moins 5 villes/régions distinctes interrogées par exécution |

## 10. Risques et points d'attention

| Risque | Impact | Atténuation |
|---|---|---|
| L'endpoint non documenté change de forme ou cesse de répondre | Élevé — le scraper ne fonctionne plus | Journalisation détaillée + revue manuelle périodique du payload brut |
| Luma met en place des mesures anti-bot (limitation de débit, blocage d'IP) | Moyen | Pauses entre les requêtes, pas de concurrence, respect du backoff |
| Modifications des Conditions d'utilisation de Luma qui restreignent cet usage | Moyen à élevé | Revue juridique avant tout usage commercial ou à grande échelle ; ne pas conserver de données de participants / DCP |
| Biais géographique de l'endpoint (résultats centrés sur la coordonnée interrogée) | Faible à moyen | Interroger plusieurs villes ; surveiller la couverture |

## 11. Feuille de route future (hors v1)

- **v1.1** : notifications automatiques (Slack/Telegram/e-mail) lorsque de nouveaux événements sont détectés.
- **v1.2** : filtrage par mots-clés dans le nom / la description de l'événement.
- **v2** : enrichissement avec les données des hôtes (réseaux sociaux) pour la génération de leads.
- **v2** : dashboard web simple pour visualiser l'historique des événements.

## 12. Questions ouvertes

- L'usage prévu est-il personnel / de la recherche, ou a-t-il une finalité commerciale (génération de leads, revente de données) ? Cela détermine le niveau de rigueur de la vérification des Conditions d'utilisation de Luma.
- Faut-il une couverture mondiale, ou suffit-il de villes précises (ex. Lima + principaux hubs tech) ?
- Faut-il une alerte en temps réel, ou suffit-il du rapport quotidien cumulé ?
