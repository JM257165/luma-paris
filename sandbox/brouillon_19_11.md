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

Je comprends l'idée : une liste de 120 entreprises (Next 40 et French Tech 120), un onglet de recherche « Luma + entreprise » par nom, puis un tri manuel par toi. Ce tri à la main est acceptable. Un script qui tape dans Google et ouvre les onglets à ta place reste de l'automatisation de Google : je ne le code pas. Je peux à la place fournir la liste de requêtes à copier toi-même.

Risque : automatiser Google expose à un blocage (CAPTCHA, « trafic inhabituel ») et à une violation de ses conditions, même avec délais aléatoires. Je ne détaille pas comment échapper à la détection, et on n'automatise pas.

Ce qui est juste et faux : lire le code source des pages n'est pas la brique interdite, l'interdit est l'automatisation des requêtes Google (conditions d'usage). Trouver une URL Luma ne suffit pas : il faut vérifier que c'est bien le calendrier de l'entreprise. Aucune brique de ce type n'est codée.

Idée (non codée) : classer les URLs Luma (calendrier ou événement) par leur signature, en règles ou avec un petit modèle. Possible hors ligne sur des URLs déjà obtenues, sans requête vers Luma. L'interdit reste l'automatisation des requêtes Google, pas ce tri.

## À faire

- Passe de rattrapage (plus tard, pas aujourd'hui) : repasser sur les calendriers déjà connus et sur tous les événements. Certains n'ont pas été renseignés (organisateur, speakers) alors que Luma les fournit. Compléter sans écraser les champs remplis.

## Graphique (non codé)

- Courbe du nombre de calendriers par jour, dans le README, pour repérer la stagnation. Plateau ≠ exhaustivité : discover ne montre que les événements à venir, donc les calendriers sans événement futur n'apparaissent pas.
- Discover mondial (toutes les villes) : non retenu en l'état. Il faudrait un volume de requêtes vers Luma bien plus élevé, sur un endpoint non documenté. Toute extension demande ton accord et une vérification des conditions d'usage.
