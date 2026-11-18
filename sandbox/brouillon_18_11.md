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
