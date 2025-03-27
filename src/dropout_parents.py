import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# === KONFIGURACJA ===
INPUT_PATH = "data/dataset.csv"
OUT_DIR = "plots/dropout_by_parent_occupation"
HUE = "Target"
COLUMNS = ["Mother's occupation", "Father's occupation"]

# === WCZYTANIE DANYCH ===
os.makedirs(OUT_DIR, exist_ok=True)
df = pd.read_csv(INPUT_PATH)

# === GENEROWANIE WYKRESÓW ===
for col in COLUMNS:
    if col not in df.columns:
        print(f"[!] Kolumna nie istnieje: {col}")
        continue

    # Top 12 najczęstszych wartości (dla czytelności wykresu)
    top_vals = df[col].value_counts().nlargest(12).index
    df_subset = df[df[col].isin(top_vals)]

    plt.figure(figsize=(12, 6))
    sns.countplot(data=df_subset, x=col, hue=HUE, order=top_vals)
    plt.xticks(rotation=90)
    plt.title(f"Dropout vs {col}")
    plt.tight_layout()

    fname = col.replace("/", "_").replace(" ", "_").lower() + ".png"
    plt.savefig(os.path.join(OUT_DIR, fname))
    plt.close()

print("[✓] Wygenerowano wykresy dla zawodów rodziców vs Target")
