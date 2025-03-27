import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import json

# === ŚCIEŻKI ===
INPUT_PATH = "data/dataset.csv"
CONFIG_PATH = "config/plot_config.json"
OUT_DIR = "plots/histograms"

# === WCZYTYWANIE ===
df = pd.read_csv(INPUT_PATH)
with open(CONFIG_PATH) as f:
    config = json.load(f)

numeric_cols = config.get("numeric_columns", [])
hue_cols = config.get("hue_columns", [])

os.makedirs(OUT_DIR, exist_ok=True)

# === GENEROWANIE HISTOGRAMÓW ===
for col in numeric_cols:
    if col not in df.columns:
        continue

    safe_col = col.replace("/", "_").replace(" ", "_").lower()

    # Histogram zwykły
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x=col, kde=True)
    plt.title(f"Histogram: {col}")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, f"{safe_col}.png"))
    plt.close()

    # Histogram warunkowy (dla każdej kolumny hue osobno)
    for hue in hue_cols:
        if hue not in df.columns:
            continue

        plt.figure(figsize=(8, 5))
        sns.histplot(data=df, x=col, hue=hue, kde=True, multiple="stack")
        plt.title(f"Histogram: {col} by {hue}")
        plt.tight_layout()
        fname = f"{safe_col}_by_{hue.replace(' ', '_').lower()}.png"
        plt.savefig(os.path.join(OUT_DIR, fname))
        plt.close()

print("[✓] Histogramy wygenerowane.")
