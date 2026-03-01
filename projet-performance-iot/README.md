# PROJET IOT - ANALYSE DE PERFORMANCE

Ce projet analyse les performances d'un moteur de règles IoT. On charge 50 fichiers JSON, on calcule des statistiques, et on affiche tout dans un dashboard interactif.

---

# STRUCTURE DU PROJET

projet-performance-iot/

├── rule_engine_dataset/ → les 50 fichiers JSON (run_000.json à run_049.json)<br>
├── data.py → Phase 1 : chargement des JSON + graphiques<br>
├── statistique.py → Phase 2 : calcul des statistiques<br>
├── timeline.py → graphique Gantt (timeline d'un run)<br>
├── app.py → Phase 3 : dashboard Streamlit<br>
└── requirements.txt → librairies Python nécessaires

---

# CE QUE FAIT LE PROJET

Chaque fichier JSON représente un run : une exécution d'un graphe de blocs IoT. Chaque run contient plusieurs blocs (WriteVar, Aggregate, ExternalCall...) avec une durée en millisecondes.

Le projet permet de :

. Voir combien de temps chaque bloc prend en moyenne<br>
. Identifier les blocs les plus lents (hotspots)<br>
. visualiser l'ordre d'exécution des blocs sur une timeline<br>

---

# INSTALLATION

. Ouvre un terminal PowerShell dans le dossier projet-performance-iot et tape :<br>
. pip install -r requirements.txt<br>
. Attends que l'installation se termine complètement.

## LANCER LE DASHBOARD

python -m streamlit run app.py

### Le navigateur s'ouvre automatiquement sur http://localhost:8501

# CE QU'ON VOIT DANS LE DASHBOARD

Section.....................................Description

KPIs Globaux.....................Taux de succès, temps moyen, nombre de runs<br>
Top 3 blocs lents................Les blocs qui ralentissent le plus le système<br>
Graphique par bloc...............Comparaison des durées entre tous les blocs<br>
Distribution.....................Variabilité des durées par type de bloc<br>
Timeline (Gantt).................Exécution d'un run bloc par bloc dans le temps<br>
Tableau complet..................Toutes les statistiques détaillées

---

# lIBRAIRIES UTILISEES

pandas : manipulation des données<br>
plotly : graphiques interactifs<br>
streamlit : dashboard web

---
