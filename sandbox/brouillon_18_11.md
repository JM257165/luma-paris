Réussi : 2 requêtes Hexa (passé et futur) suffisent pour les speakers du semestre, sans requête par événement. 20 événements, 5 avec speakers. Organisateur (nom du calendrier) déjà ajouté. Question : garde-t-on aussi les hôtes (personnes) ? Si oui, colonnes hôte_1, hôte_2… dans l'Excel.

---

Ce qu'on a appris :
- IMPORTDATA lit le CSV brut : l'URL GitHub « blob » renvoie du HTML, il faut raw.githubusercontent.com. Dépôt privé : IMPORTDATA ne marche plus.
- Les intervenants viennent de featured_guests : nom, bio courte, LinkedIn, site, réseaux. Pas de champ entreprise.
- Sur Hexa, 5 événements sur 20 ont des intervenants, 10 chacun : d'où MAX_SPEAKERS = 10. À vérifier : limite de l'API ou vrai nombre ?
- Les speakers sont masqués dans l'interface pour les visiteurs non connectés. Dépôt repassé en privé.

Fait et poussé :
- config.py, scraper.py, backfill_calendar.py : organisateur, speakers, backfill d'un calendrier.
- events_master.csv : 172 lignes, 37 colonnes, 20 lignes Hexa.

Reste :
- Décider : hôtes en plus de l'organisateur ? Si oui, colonnes à ajouter.
- Vérifier si la réponse discover contient featured_guests (une requête).
- Remplir les 152 anciennes lignes via d'autres calendriers, après accord (pauses 3 à 5 s).

## Invités mis en avant : ce qu'on a appris

Les colonnes speaker_i du CSV remote ne sont pas des intervenants mais des invités mis en avant par Luma (10 sur 102 pour 8q8fwz0z), sans rôle ni critère de sélection connus. La description dit « no program ». L'organisateur réel est la colonne organisateur (nom du calendrier, ex. Hexa House). L'affichage peut différer de la donnée : l'hôte « Hexa » est Faustine Rohr-Lacoste dans le JSON, et le code source affiche aussi (Hexa) après son nom. Décision : on abandonne les invités mis en avant et on garde les organisateurs.

## Prochaine étape : tous les calendriers tech/IA de Paris

1. Lister les calendriers Luma associés à la tech ou à l'IA à Paris.
2. Pour chaque calendrier, appliquer la méthode Hexa : 2 requêtes (passé et futur), pauses de 3 à 5 s, arrêt immédiat sur 403 ou 429, pages bornées.
3. Garder les organisateurs et les événements, sans les invités mis en avant.
4. Proxy : à éviter. Si un blocage survient, on s'arrête et on en reparle, sans en choisir un au hasard.

Aucune requête avant ton feu vert.

## Événements déjà listés avec champs vides

Décision : retirer les colonnes speaker du schéma. Si un événement déjà listé (même api_id) a un champ vide (ex. organisateur), on complète la ligne existante, sans écraser les champs remplis ni first_seen.
- Deux endpoints : discover trouve les calendriers (futurs seulement), calendar/get-items donne passé et futur d'un calendrier connu. Exhaustivité non garantie, on accumule au fil des discover.
