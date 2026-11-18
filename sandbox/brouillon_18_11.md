Ajout : colonne « organisateur » (nom du calendrier) dans l'Excel. Test sur Hexa : tous les événements et speakers du semestre, si tu valides les requêtes.

---

Ce qu'on a appris :
- IMPORTDATA lit le CSV brut : l'URL GitHub « blob » renvoie du HTML, il faut raw.githubusercontent.com.
- Les intervenants viennent de featured_guests : nom, bio courte, LinkedIn, site, réseaux. Pas de champ entreprise.
- Sur Hexa, 2 événements sur 15 ont des intervenants, dont 10 chacun : d'où n = 10.
- Le même endpoint get-items donne le passé et le futur d'un calendrier.

Ce qui est fait (en local, non commité) :
- config.py : MAX_SPEAKERS = 10, colonnes générées (3 par speaker, 36 au total).
- scraper.py : build_speaker_link (LinkedIn, puis site, X, Instagram, TikTok, YouTube), extract_speakers, event_to_row.
- events_master.csv : en-tête migré, 152 lignes conservées, colonnes speaker vides.
- Test hors réseau sur le brut Hexa : extraction OK, liens LinkedIn corrects.

Reste :
- Valider, puis commiter et pousser le code (le bot tourne encore sur l'ancien code).
- Vérifier si la réponse discover contient featured_guests, sinon les nouveaux événements resteront vides.
- Remplir les anciennes lignes via les calendriers, une fois les requêtes autorisées (pauses 3 à 5 s).
- Liste des calendriers tech/IA parisiens à valider avant de parcourir.
