import json
import glob
import os
import pandas as pd
import plotly as px

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rule_engine_dataset")

def load_runs(data_dir=DATA_DIR):
    records = []
    for filepath in glob.glob(os.path.join(data_dir, "run_*.json")):
        try:
            with open(filepath, encoding="utf-8") as f:
                data = json.load(f)
            ri = data["run_info"]
            for block in data["execution_trace"]:
                records.append({
                    "run_id": ri["run_id"],
                    "graph_id": ri["graph_id"],
                    "status": ri["status"],
                    "total_ms": ri["total_ms"],
                    "timestamp": ri["timestamp"],
                    "step": block["step"],
                    "block_id": block["block_id"],
                    "class": block["class"],
                    "duration_ms": block["duration_ms"],
                })
        except:
            print("fichier corrompu ignoré : " + filepath)
    return pd.DataFrame(records)

def build_gantt_df(df_run):
    df = df_run.sort_values("step").copy()
    df["start_ms"] = df["duration_ms"].cumsum() - df["duration_ms"]
    df["end_ms"] = df["duration_ms"].cumsum()
    base = pd.Timestamp("2000-01-01")
    df["Start"] = base + pd.to_timedelta(df["start_ms"], unit="ms")
    df["Finish"] = base + pd.to_timedelta(df["end_ms"], unit="ms")
    return df

def plot_timeline(run_id, df_all):
    df_run = df_all[df_all["run_id"] == run_id]
    df_gantt = build_gantt_df(df_run)
    fig = px.timeline(
        df_gantt, x_start="Start", x_end="Finish", y="block_id", color="class",
        title="Timeline d'exécution - " + run_id,
        hover_data={"step": True, "duration_ms": True, "Start": False, "Finish": False},
    )
    fig.update_xaxes(tickformat="%M:%S.%L", title_text="Temps cumulé (ms)")
    fig.update_yaxes(autorange="reversed", title_text="Bloc")
    fig.update_layout(height=max(300, 60 * len(df_gantt)))
    return fig

if __name__ == "__main__":
    df = load_runs()
    if df.empty:
        print("Aucun fichier JSON trouvé.")
    else:
        first_run = df["run_id"].iloc[0]
        fig = plot_timeline(first_run, df)
        fig.show()
