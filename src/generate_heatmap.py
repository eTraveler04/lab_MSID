import argparse
import os
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# === HEATMAP GENERATOR ===
# Tworzy heatmapę korelacji dla cech numerycznych
def generate_heatmap(df, numeric_cols, out_dir):
    heatmap_dir = os.path.join(out_dir, "heatmap")
    os.makedirs(heatmap_dir, exist_ok=True)

    # Oblicz macierz korelacji
    corr = df[numeric_cols].corr()

    # Zapisz heatmapę do pliku PNG
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True, cbar=True)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(os.path.join(heatmap_dir, "correlation_heatmap.png"))
    plt.close()

    # Zapisz ranking korelacji do pliku tekstowego
    mask = ~np.tril(np.ones(corr.shape)).astype(bool)
    correlation_ranking = (
        corr.where(mask)
            .stack()
            .reset_index()
            .rename(columns={0: 'correlation', 'level_0': 'feature_1', 'level_1': 'feature_2'})
            .sort_values(by='correlation', ascending=False)
    )
    ranking_path = os.path.join(heatmap_dir, "correlation_ranking.txt")
    with open(ranking_path, 'w') as f:
        f.write("Correlation Ranking (highest to lowest):\n\n")
        for _, row in correlation_ranking.iterrows():
            f.write(f"{row['feature_1']} ↔ {row['feature_2']}: {row['correlation']:.2f}\n")

    # Dodatkowy wydruk korelacji między approved 1st sem a enrolled 2nd sem
    col_a = "Curricular units 1st sem (approved)"
    col_b = "Curricular units 2nd sem (enrolled)"
    if col_a in df.columns and col_b in df.columns:
        val = df[col_a].corr(df[col_b])
        print("[✓] Korelacja między approved 1st sem a enrolled 2nd sem:", round(val, 4))

        # Podsumowanie interpretacyjne
        print("\n[📊] WNIOSKI:")
        print(f"- Korelacja między liczbą zaliczonych przedmiotów w 1 semestrze a zapisanymi w 2 semestrze wynosi {round(val, 2)}.")
        if val > 0.7:
            print("- Jest to silna dodatnia korelacja. Studenci, którzy więcej zaliczają w 1 semestrze, częściej zapisują się na więcej przedmiotów w 2 semestrze.")
        elif val > 0.4:
            print("- Jest to umiarkowana korelacja. Można założyć, że wyniki w 1 semestrze częściowo wpływają na zaangażowanie w 2 semestrze.")
        else:
            print("- Korelacja jest słaba. Nie widać wyraźnego związku między tymi cechami.")


# === MAIN FUNCTION ===
# Wczytuje dane i konfigurację, generuje heatmapę
def main(input_path, config_path, out_dir):
    print(f"[*] Wczytywanie pliku CSV: {input_path}")
    df = pd.read_csv(input_path)
    print("[✓] Plik CSV wczytany. Liczba kolumn:", len(df.columns))

    print(f"[*] Wczytywanie konfiguracji: {config_path}")
    with open(config_path) as f:
        config = json.load(f)

    numeric_cols = config.get("numeric_columns", [])
    print("[✓] Kolumny numeryczne:", numeric_cols)

    generate_heatmap(df, numeric_cols, out_dir)


# === CLI ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/dataset.csv', help="Path to CSV file")
    parser.add_argument('--config', default='config/plot_config.json', help="Path to JSON config file")
    parser.add_argument('--out_dir', default='plots', help="Output folder for plots")
    args = parser.parse_args()
    main(args.input, args.config, args.out_dir)
