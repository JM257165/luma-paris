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

## Bilan recherche web et méthode suivante

Sur les 61 calendriers de calendar_master.csv, la recherche « Luma <nom> Paris » en retrouve 4, soit 6,6 %. Les autres ne sont pas trouvés, ou sont noyés par des homonymes (LUMA Arles, LUMAS, Luma AI). Méthode suivante : 1) dresser la liste des entreprises qui nous intéressent ; 2) chercher leur calendrier Luma avec la recherche web ; 3) pour chaque calendrier trouvé, faire deux appels (passé et futur) et récupérer tous les événements. Aucune requête vers Luma avant ton feu vert.

## Recherche web v2 : résultat

Requête « <nom court> calendar Paris events », restreinte à lu.ma et luma.com, avec sélection des pages dont le titre contient « Events Calendar ». Résultat : 17 calendriers retrouvés sur 61, soit **27,9 %**, contre 6,6 % avec la v1. Gains : 14 calendriers, dont Dust, Hexa, Startup Valley, swanbase et Vercel Community. Pertes : LeClub IA, retrouvé par la v1 mais pas par la v2. Limites : DR Network est rejeté à cause de son titre en français « Calendrier d'événements », et les calendriers non indexés (Alan, Modal, Tandem) restent introuvables. Prochain pas : accepter ce titre français et relancer LeClub IA.

## Analyse d'un ami : contourner le blocage de recherche

- Constat : Google bloque l'IP (pas le compte) lors d'un scraping rapide. Pour un seul domaine : utiliser le sitemap.xml du site cible, ou cumuler les quotas gratuits d'une dizaine d'API de résultats de recherche (Bright Data, Serper, Brave, Tavily, Exa, DataForSEO, Keirolabs, SerpApi…) en optimisant les requêtes avec site:domaine.com et OR.
- Volume gratuit annoncé (non vérifié) : ~8 000 à 12 000 requêtes récurrentes par mois, ~6 000 en crédits à l'inscription, ~300 à 400 par jour en moyenne.
- Avis : le constat sur l'IP est plausible, mais les chiffres sont des estimations non sourcées, à vérifier sur les pages tarifaires de chaque fournisseur. Trois points bloquants :
  1. Cumuler les quotas gratuits en ouvrant plusieurs comptes revient à contourner les limites des services. C'est la voie que tu as exclue (pas de compte jetable, pas de contournement).
  2. Le sitemap de lu.ma reste une requête vers Luma : elle ne se lance qu'après ton feu vert, avec les pauses de 3 à 5 s.
  3. Les conditions d'utilisation de ces APIs et de la recherche elle-même doivent être lues avant tout usage ; « Keirolabs » n'est pas un service que je peux vérifier.
- Piste plus propre : une seule API de recherche officielle, sur un compte à ton nom, avec son quota payant ou gratuit documenté. Pour une centaine de requêtes, le coût devrait rester faible. Rien n'est lancé.
