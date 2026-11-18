Chrome a révélé api.luma.com/calendar/get-items (period=past). Hexa : 15 passés (juil.–nov. 2026) en une requête, avec pagination. Hôtes partout, intervenants sur 2 événements (20 noms), pas d'entreprise. Brut sauvé en local. Reste : pagination, règle d'extraction, backfill lent.

---

To-do :
- Suivre la pagination (next_cursor) sur Hexa.
- Définir la règle d'extraction : organisateur, intervenant, société (bio ou site).
- Décider si on récupère les descriptions (1 requête par événement).
- Collecter les calendriers tech/IA des runs futurs jusqu'à fin 2026.
- Backfill lent : pause 3 à 5 s entre requêtes, dédupliquer, écrire le CSV historique.
