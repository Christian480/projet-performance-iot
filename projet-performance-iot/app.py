import streamlit as st
import pandas as pd
import plotly.express as px
import glob
import json
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Data Profiler IoT", layout="wide")
st.title(" Projet : Analyse de Performance IoT")
st.markdown("Outil d'Observabilité Experte pour identifier les hotspots d'exécution.")

# --- PHASE 1 : INGESTION & TRAITEMENT [cite: 95, 96] ---
def load_data(folder_path):
    all_runs_metadata = []
    all_trace_steps = []
    
    # 1. Scan du dossier pour trouver les 50 fichiers JSON 
    files = glob.glob(os.path.join(folder_path, "*.json"))
    
    if not files:
        st.error(f"Aucun fichier trouvé dans le dossier {folder_path}")
        return None, None

    for file in files:
        # 3. Nettoyage & Gestion des exceptions (Try/Except) [cite: 99]
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                
                # Récupération des infos générales du run [cite: 65, 76]
                info = data.get("run_info", {})
                all_runs_metadata.append(info)
                
                # Récupération de la trace d'exécution [cite: 66, 83]
                run_id = info.get("run_id")
                for step in data.get("execution_trace", []):
                    step["run_id"] = run_id  # On lie l'étape au run_id
                    all_trace_steps.append(step)
                    
        except Exception as e:
            # Si un fichier est corrompu, on l'affiche mais on continue 
            st.warning(f"Erreur de lecture sur le fichier {file} : {e}")
            continue
            
    # 2. Transformation en DataFrames Pandas [cite: 98]
    df_runs = pd.DataFrame(all_runs_metadata)
    df_traces = pd.DataFrame(all_trace_steps)
    
    return df_runs, df_traces

# Chargement effectif des données
# On suppose que le dossier est dans le même répertoire que le script [cite: 18]
df_runs, df_traces = load_data("rule_engine_dataset")

if df_runs is not None:
    # --- PHASE 2 : ANALYSE (PROFILING) [cite: 100, 102] ---
    st.header(" Analyse Globale des Performances")
    
    # Calcul de la moyenne et du max par block_id [cite: 102, 118]
    profiling_df = df_traces.groupby("block_id")["duration_ms"].agg(["mean", "max", "count"]).reset_index()
    profiling_df.columns = ["ID du Bloc", "Moyenne (ms)", "Maximum (ms)", "Nombre d'appels"]
    
    # Détection du Bottleneck (les 3 plus lents) [cite: 103]
    bottlenecks = profiling_df.sort_values(by="Moyenne (ms)", ascending=False).head(3)
    
    # Affichage des KPIs 
    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre de Runs", len(df_runs))
    col2.metric("Temps Moyen Global", f"{df_runs['total_ms'].mean():.2f} ms")
    col3.metric("Taux de Succès", f"{(df_runs['status'] == 'SUCCESS').mean()*100:.1f}%")

    # --- PHASE 3 : VISUALISATION INTERACTIVE [cite: 108, 109] ---
    
    # Sélection d'un Run spécifique pour le détail [cite: 118, 122]
    st.subheader("Analyse détaillée d'un Run")
    selected_run = st.selectbox("Choisir un Run ID pour voir la Timeline", df_runs["run_id"].unique())
    *
    # Filtrage des données pour le run sélectionné 
    run_detail = df_traces[df_traces["run_id"] == selected_run].sort_values("step")
    
    # Timeline Plotly (Graphique de Gantt simplifié) [cite: 111, 118]
    fig = px.bar(
        run_detail, y
        x="duration_ms", 
        y="block_id", 
        color="class", 
        orientation='h',
        title=f"Chronologie de l'exécution : {selected_run}",
        labels={"duration_ms": "Durée (ms)", "block_id": "ID du Bloc"},
        hover_data=["step", "input", "output"] # 
    )
    st.plotly_chart(fig, use_container_width=True)

    # Affichage du tableau de profiling 
    st.subheader(" Statistiques par Bloc")
    st.dataframe(profiling_df.style.highlight_max(axis=0, subset=["Moyenne (ms)"], color='lightcoral'))