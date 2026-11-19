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

## Perspective (non codée, non retenue en l'état)

Je comprends l'idée : une liste de 120 entreprises (Next 40 et French Tech 120), un onglet de recherche « Luma + entreprise » par nom, puis un tri manuel par toi. Ce tri à la main est acceptable. Un script qui lance les requêtes Google pour trouver des calendriers est possible : à faible volume, une seule passe à la fois. Règle d'interdiction retirée le 19/11 (elle était erronée).

Risque : blocage possible (CAPTCHA, « trafic inhabituel »). En cas de signal, on s'arrête et on n'insiste pas.

Ce qui est juste et faux : lire le code source des pages n'est pas la brique interdite, les conditions d'usage de Google restent à relire avant tout volume. Trouver une URL Luma ne suffit pas : il faut vérifier que c'est bien le calendrier de l'entreprise. Aucune brique de ce type n'est codée.

Idée (non codée) : classer les URLs Luma (calendrier ou événement) par leur signature, en règles ou avec un petit modèle. Possible hors ligne sur des URLs déjà obtenues, sans requête vers Luma.
## À faire

- Passe de rattrapage (plus tard, pas aujourd'hui) : repasser sur les calendriers déjà connus et sur tous les événements. Certains n'ont pas été renseignés (organisateur, speakers) alors que Luma les fournit. Compléter sans écraser les champs remplis.

## Graphique (non codé)

- Courbe du nombre de calendriers par jour, dans le README, pour repérer la stagnation. Plateau ≠ exhaustivité : discover ne montre que les événements à venir, donc les calendriers sans événement futur n'apparaissent pas.
- Discover mondial (toutes les villes) : non retenu en l'état. Il faudrait un volume de requêtes vers Luma bien plus élevé, sur un endpoint non documenté. Toute extension demande ton accord et une vérification des conditions d'usage.

## Après le code

- Faire tourner le run (backfill des nouveaux calendriers, puis stats_daily.csv et graphiques) après validation du code. Aucune requête vers Luma avant ton accord.
- Colonne backfilled dans calendar_master.csv : Non partout, Oui après backfill réussi. Demain : backfill des Non. Back Market, Crème de la Crème, HomeExchange sans identifiant : à résoudre avant.
