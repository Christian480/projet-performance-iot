import streamlit as st
from data import load_runs, plot_timeline, plot_distribution
from statistics import profiling_par_block, top3_blocs_lents, taux_succes, temps_moyen_total, plot_hotspots

st.set_page_config(page_title="IoT Performance Dashboard", page_icon="", layout="wide")
st.title("Observabilité IoT — Analyse de Performance")

st.cache_data
def get_data():
    return load_runs()

df = get_data()

if df.empty:
    st.error("Aucun fichier JSON trouvé.")
    st.stop()

stats = profiling_par_block(df)
top3 = top3_blocs_lents(stats)

st.header(" KPIs Globaux")
c1, c2, c3 = st.columns(3)
c1.metric("Taux de succès", str(taux_succes(df)) + " %")
c2.metric("Temps moyen total", str(temps_moyen_total(df)) + " ms")
c3.metric("Runs analysés", df["run_id"].nunique())

st.header(" Top 3 blocs les plus lents")
for i, row in top3.iterrows():
    st.warning("#" + str(i+1) + " — " + row["block_id"] + " (" + row["class"] + ") → moy. " + str(row["mean_ms"]) + " ms | max " + str(row["max_ms"]) + " ms")

st.header("Analyse par Bloc")
col_l, col_r = st.columns(2)
with col_l:
    st.plotly_chart(plot_hotspots(stats), use_container_width=True)
with col_r:
    st.plotly_chart(plot_distribution(df), use_container_width=True)

st.header("Timeline d'Exécution")
run_ids = sorted(df["run_id"].unique())
selected = st.selectbox("Choisir un run :", run_ids)
st.plotly_chart(plot_timeline(selected, df), use_container_width=True)

with st.expander(" Tableau de profiling"):
    st.dataframe(stats, use_container_width=True)
    

