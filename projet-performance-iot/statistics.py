import pandas as pd
import plotly.express as px

def profiling_par_block(df):
    stats = df.groupby(["block_id", "class"])["duration_ms"].agg(mean_ms="mean", max_ms="max", count="count").reset_index()
    stats = stats.sort_values("mean_ms", ascending=False).reset_index(drop=True)
    stats["mean_ms"] = stats["mean_ms"].round(1)
    stats["max_ms"] = stats["max_ms"].round(1)
    return stats

def top3_blocs_lents(stats):
    return stats.nlargest(3, "mean_ms").reset_index(drop=True)

def taux_succes(df):
    runs = df.drop_duplicates("run_id")
    succes = (runs["status"] == "SUCCESS").sum()
    total = len(runs)
    return round(succes / total * 100, 1)

def temps_moyen_total(df):
    runs = df.drop_duplicates("run_id")
    return round(runs["total_ms"].mean(), 1)

def plot_hotspots(stats):
    top10 = stats.head(10).copy()
    fig = px.bar(
        top10, x="mean_ms", y="block_id", color="class", orientation="h",
        title="Top 10 blocs les plus lents",
        labels={"mean_ms": "Durée moyenne (ms)", "block_id": "Bloc", "class": "Type"},
        text="mean_ms",
    )
    fig.update_traces(texttemplate="%{text:.0f} ms", textposition="outside")
    fig.update_yaxes(autorange="reversed")
    return fig
