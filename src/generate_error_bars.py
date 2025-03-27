import os
import math
import pandas as pd
import matplotlib.pyplot as plt

# === ŚCIEŻKI ===
INPUT_PATH = "data/dataset.csv"
OUT_DIR = "plots/error_bars"
CHUNK_SIZE = 10

# === WCZYTYWANIE ===
os.makedirs(OUT_DIR, exist_ok=True)
df = pd.read_csv(INPUT_PATH)
numeric_cols = df.select_dtypes(include='number').columns.tolist()

# === FUNKCJA TWORZĄCA ERROR BAR DLA PODANYCH KOLUMN ===
def plot_error_bars(df, cols, title, filename):
    subset = df[cols]
    means = subset.mean()
    ci = 1.96 * subset.sem()
    medians = subset.median()

    fig, ax = plt.subplots(figsize=(14, len(cols) * 0.6 + 2))
    ax.errorbar(x=means.values, y=means.index, xerr=ci.values, fmt='o', capsize=5, label="Mean ± 95% CI", color='blue')
    ax.scatter(medians.values, means.index, marker='s', color='red', label="Median")
    ax.axvline(0, color='gray', linestyle='--', linewidth=0.8)
    ax.set_title(title)
    ax.set_xlabel("Wartość")
    ax.legend()
    ax.grid(axis='x', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    output_path = os.path.join(OUT_DIR, filename)
    try:
        fig.savefig(output_path)
    except Exception as e:
        print(f"[!] Błąd zapisu pliku {output_path}: {e}")
    plt.close(fig)

# === WYKRES ZBIORCZY ===
plot_error_bars(df, numeric_cols, "Mean ±95% CI — All Numeric Features", "all_numeric.png")

# === WYKRESY PODZIELONE NA CZĘŚCI ===
for i in range(math.ceil(len(numeric_cols) / CHUNK_SIZE)):
    chunk = numeric_cols[i * CHUNK_SIZE:(i + 1) * CHUNK_SIZE]
    title = f"Mean ±95% CI — Features {i * CHUNK_SIZE + 1}–{min((i + 1) * CHUNK_SIZE, len(numeric_cols))}"
    fname = f"chunk_{i + 1}.png"
    plot_error_bars(df, chunk, title, fname)

# === WYKRESY DLA POJEDYNCZYCH CECH ===
for col in numeric_cols:
    plot_error_bars(df, [col], f"Mean ±95% CI — {col}", f"single_{col.replace('/', '_').replace(' ', '_')}.png")

print("[✓] Wygenerowano wykresy error bars")