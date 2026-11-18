Votre PC n'est pas concerné. Votre compte GitHub risque peu : un blocage IP touche les runs, pas le compte. Où on en est : analyse anti-ban faite, gh installé, origin renommé upstream (push désactivé), commit local ccce3f8. Bloqué : gh non connecté. Reste : auth, repo privé, push, workflow, vérif. Appris : le cron tourne sur GitHub Actions, pas sur votre PC ; quota gratuit ~2 000 min/mois en privé (à vérifier). Choix tech : Python stdlib seule, Actions plutôt que cron local, délais 3-5 s, 1 ville, 2 catégories.

Chaque jour (cron 08h UTC) sur GitHub Actions : pour Tech et AI à Paris, le scraper appelle l'endpoint Luma par pages (50 max), avec pause 3-5 s. Il déduplique par api_id, ajoute les nouveaux événements à events_master.csv et seen_events.json, puis commit le tout dans le repo.

Estimation chiffrée (semestre Tech + AI, Paris) :
- Run du 16/11 : 142 événements (tech 55, ai 87), du 16/11/2026 au 25/02/2027. Durée d'un run : environ 1 min, 4 requêtes (2 catégories × 2 pages).
- Passé (août à 15/11/2026) : 0 événement récupérable avec cet endpoint. Le paramètre de date testé est ignoré.
- Du 16/11 au 31/12/2026 : 131 événements déjà dans master (92 en novembre, 39 en décembre).
- Couverture complète du semestre : non atteignable en quelques jours. Le run ne renvoie qu'un snapshot de Luma (environ 140 événements), et l'accumulation quotidienne ne fait qu'ajouter les nouveaux.
- Prochaine étape : mesurer les nouveaux événements par jour sur 7 runs (J+7, soit le 23/11), puis estimer le délai réel.

Complétude Paris, maintenant → décembre :
Déjà captés : 131 (16/11 → 31/12). Délai estimé : ~7 jours, mesure des nouveautés sur 7 runs (23/11). Passé : aucun endpoint de passés dans le repo (seul get-paginated-events). Piste : autre endpoint ou pages Luma publiques (non vérifié).

Note Apify (à vérifier) : Point d'attention : la fiche Apify affirme que le mode calendrier renvoie les événements passés. Ce n'est pas clair ni vérifié, à tester sur un calendrier réel. Découverte, catégorie et ville ne donnent que les futurs. Coût annoncé : $0,10 pour 1 000 événements. Non utilisé, inspiration seulement.

---

Bilan 16/11 : [config.py:6](../config.py#L6) Paris seul, délais [3-5 s](../config.py#L10) ; [scraper.py:58](../scraper.py#L58) min 1 ville ; [README.md:5](../README.md#L5) crédit, [README.md:39](../README.md#L39) ; [.gitignore:20](../.gitignore#L20) sandbox/ ; origin = Jean8900/luma-paris, upstream lecture seule ; commits ccce3f8, e24989f.
