# Projet IoT — Analyse de Performance

Ce projet analyse les performances d'un moteur de règles IoT.
On charge 50 fichiers JSON, on calcule des statistiques, et on affiche tout dans un dashboard interactif.

---

## Structure du projet

```
projet-performance-iot/
├── rule_engine_dataset/   → les 50 fichiers JSON (run_000.json à run_049.json)
├── visuel.py              → Phase 1 : chargement des JSON + graphiques
├── statistique.py         → Phase 2 : calcul des statistiques
├── timeline.py            → graphique Gantt (timeline d'un run)
├── app.py                 → Phase 3 : dashboard Streamlit
└── requirements.txt       → librairies Python nécessaires
```

---

## Ce que fait le projet

Chaque fichier JSON représente un **run** : une exécution d'un graphe de blocs IoT.
Chaque run contient plusieurs **blocs** (WriteVar, Aggregate, ExternalCall...) avec une durée en millisecondes.

Le projet permet de :
- voir combien de temps chaque bloc prend en moyenne
- identifier les blocs les plus lents (hotspots)
- visualiser l'ordre d'exécution des blocs sur une timeline

---

## Installation

Ouvre un terminal PowerShell dans le dossier `projet-performance-iot` et tape :

```powershell
pip install -r requirements.txt
```

Attends que l'installation se termine complètement.

---

## Lancer le dashboard

```powershell
python -m streamlit run app.py
```

Le navigateur s'ouvre automatiquement sur `http://localhost:8501`.

---

## Ce qu'on voit dans le dashboard

| Section | Description |
|---|---|
| KPIs Globaux | Taux de succès, temps moyen, nombre de runs |
| Top 3 blocs lents | Les blocs qui ralentissent le plus le système |
| Graphique par bloc | Comparaison des durées entre tous les blocs |
| Distribution | Variabilité des durées par type de bloc |
| Timeline (Gantt) | Exécution d'un run bloc par bloc dans le temps |
| Tableau complet | Toutes les statistiques détaillées |

---

## Librairies utilisées

- **pandas** : manipulation des données
- **plotly** : graphiques interactifs
- **streamlit** : dashboard web
