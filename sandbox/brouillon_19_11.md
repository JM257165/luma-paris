# Brouillon 19/11

Où on en est (18/11) :
- Discover : 61 calendriers tech/IA Paris trouvés. Pauses de quelques secondes via GitHub (requêtes hors de ton IP, protection limitée).
- Calendrier : 2 requêtes (passé, futur) suffisent, avec les organisateurs.
- Enjeu : trouver les calendriers, seul accès au passé.
- Recherche web : v1 4/61 (6,6 %), v2 17/61 (27,9 %). Quota de 200 = outil Claude Code, pas Google. Service payant (~10 000 requêtes, ~5 €) à vérifier.
- Partage de recherches entre amis : non retenu (contourne les limites du moteur).

Suite : API officielle à comparer (Brave, Google PSE, Exa, Tavily), séquentielle, sur ton compte.

## Feature intéressante (non codée)

Chaque jour, ajouter à calendar_master.csv les calendriers vus dans discover, sans doublon. Pour chaque nouveau calendrier, backfill passé et futur (2 requêtes, pauses de 3 à 5 s), puis complément d'events_master.csv sans écraser les champs remplis. Aucune requête sans ton accord.

## À faire

(à compléter)
