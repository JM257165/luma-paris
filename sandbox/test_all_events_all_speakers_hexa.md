# Test : tous les événements et tous les speakers (calendrier Hexa, août–déc. 2026)

Note : la demande parlait d'« Exa ». Le calendrier testé depuis le début est Hexa (`cal-v1gaUIroyMZE7bW`). Exa n'avait pas de slug de calendrier trouvé, donc on a traité Hexa.

## Objectif

Récupérer tous les événements de Hexa dans la période août–décembre 2026, avec leurs speakers (nom, lien, bio) et leur organisateur (nom du calendrier), sans prendre de risque de blocage.

## Boucle d'essais

1. **Tentative 1 : requête de lecture (sans écriture)**
   - `python backfill_calendar.py`
   - Résultat : 2 requêtes (`past` page 1 : 69 entrées, `future` page 1 : 5 entrées), aucune erreur, environ 10 secondes.
   - Vérification : `has_more = false` et pas de `next_cursor` sur les deux pages, donc la pagination est complète. Le passé remonte à décembre 2023.
   - Apprentissage : la réponse précédente de 15 entrées était partielle. La réponse complète tient en une page.

2. **Tentative 2 : écriture à partir des JSON bruts (`--from-raw --write`)**
   - Aucune nouvelle requête. Les 20 événements de la période sont ajoutés à `events_master.csv`.
   - Vérification : 172 lignes au total, 20 avec organisateur, en-tête de 37 colonnes.

## Résultats

- 20 événements dans la période (août–déc. 2026), 0 déjà connu, 20 nouveaux.
- Organisateurs : Hexa (14), Hexa House (2), Startup Valley, Lucis Club, HYPE: IRL tech events, GTM World Tour (1 chacun).
- 5 événements ont des speakers, 50 speakers au total.

## Point à vérifier

Les 5 événements avec speakers ont exactement **10 speakers chacun**. C'est peut-être une limite de l'API (`featured_guests` tronqué à 10), et pas le nombre réel. On ne peut pas le trancher sans comparer avec la page de l'événement sur lu.ma. C'est aussi pour ça que `MAX_SPEAKERS = 10` avait été choisi : à surveiller si un événement en affiche plus.

## Décisions prises

- `first_seen` = date du backfill (2026-11-18). Ce n'est pas la date de première publication.
- Les 152 anciennes lignes (discover) n'ont pas d'organisateur : colonne vide.
- Catégorie = « calendrier » pour ces 20 lignes, faute de catégorie fournie par l'endpoint calendrier.
- Le JSON brut est gardé hors dépôt, dans `C:\Users\jeanm\luma-backfill-raw`. Il contient des bios et des liens personnels.

## Garde-fous utilisés

- Requêtes en série, pause de 3 à 5 s entre chaque.
- Arrêt immédiat sur 403, 429 ou erreur réseau, sans retry.
- Pages bornées à 10 par période (2 utilisées).

## Reste à faire

- Vérifier le plafond de 10 speakers sur une page lu.ma.
- Demander le feu vert avant d'élargir à d'autres calendriers.
