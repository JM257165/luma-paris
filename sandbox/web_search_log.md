# Log web search : 10 passages sur les 61 calendriers

Requête : « Luma <nom du calendrier> Paris », recherche web standard.
Critère strict : le slug de calendar_master.csv doit apparaître comme lu.ma/<slug> ou luma.com/<slug> dans les résultats.
Aucune requête vers Luma pendant les passages : seulement la recherche web.

## Passage 1

### Passage 1, lots 1 et 2 (30 requêtes)
- Retrouvés (critère strict) : CO-CTO Calendar (`luma.com/co-cto`).
- Erreurs constatées : aucune erreur technique. Requêtes homonymes (LUMA Arles, LUMAS, Luma AI) toujours présentes. Les pages d'avatars (ex. GenAI Network, Paris Hardware Meetup) ne comptent pas, le slug ne correspond pas.
- Correction programme : aucune à ce stade.

### Passage 1, lots 3 et 4 (31 requêtes, dont Dust relancé)
- Retrouvés : JAB EVENTS (`luma.com/jab`), LeClub IA (`luma.com/leclub-ia`), Women of SaaS (`luma.com/womenofsaas`).
- Dust : requête « Luma Dust Paris » relancée (oubliée dans les lots précédents), toujours non retrouvé.
- Erreurs : aucune erreur technique. Constat : les résultats sont identiques à ceux du bilan précédent pour les 61 requêtes.

## Bilan passage 1
- Retrouvés (critère strict) : 4 sur 61 = 6,6 % (CO-CTO, JAB, LeClub IA, Women of SaaS).
- Identique au bilan précédent. Aucune erreur, aucune correction de programme nécessaire.

## Passage v2 : requête « <nom court> calendar Paris events », domaines lu.ma / luma.com

Méthode : `calendar_search_v2.py`. Requête avec nom raccourci (sans suffixe « — », parenthèses, emoji, ni mot « Calendar »). Sélection : URLs luma.com/<slug> ou lu.ma/<slug> dont le titre contient « Events Calendar ». Comparaison au slug de la liste, insensible à la casse. 0 requête vers Luma.

Résultat : **17 retrouvés sur 61 = 27,9 %** (contre 4 sur 61 avec la v1).

Retrouvés : AI Salon, App Leaders Club, BioWeek 2026, borvibe, CO-CTO, Dev With AI, Dust, HelloCircle, Hexa, JAB, Nucleate, Paris Hardware Meetup, Revelo, Startup Valley, swanbase, Vercel Community, Women of SaaS.

Ce qui a changé par rapport à la v1 :
- Gagnés : AI Salon, App Leaders Club, BioWeek, borvibe, Dev With AI, Dust, HelloCircle, Hexa, Nucleate, Paris Hardware Meetup, Revelo, Startup Valley, swanbase, Vercel Community (14 gains).
- Perdus : LeClub IA. La v1 le trouvait via « Luma LeClub IA Paris », la v2 ne le fait pas avec « LeClub IA calendar Paris events ».
- Limite de la règle : DR Network (`luma.com/dr-network-calendar`) a un titre en français, « Calendrier d'événements ». La règle « Events Calendar » le rejette. Faux négatif à corriger en acceptant aussi « Calendrier d'événements ».
- Pas trouvés, car non indexés sous ce titre ou slug différent : Alan (`alan.eu`), Augmented (page `luma.com/thiga`, slug différent de `augmented-thiga`), Modal, Tandem, et les autres.

Fixtures : `fixtures/v2/lot1.json` à `lot4.json` (entrées au titre « Events Calendar » et calendriers voisins, tels que lus dans les résultats).
