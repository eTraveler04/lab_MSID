import argparse
import os
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === REGRESSION PLOT GENERATOR ===
# Tworzy wykresy regresji liniowej dla każdej pary cech numerycznych

def generate_regression_plots(df, numeric_cols, out_dir):
    reg_dir = os.path.join(out_dir, "regression")
    os.makedirs(reg_dir, exist_ok=True)

    for i, col1 in enumerate(numeric_cols):
        for col2 in numeric_cols[i+1:]:
            plt.figure(figsize=(8, 5))
            sns.regplot(data=df, x=col1, y=col2, scatter_kws={"s": 10}, line_kws={"color": "red"})
            plt.title(f"Linear Regression: {col2} ~ {col1}")
            plt.tight_layout()
            filename = f"{col2.replace('/', '_').replace(' ', '_')}_vs_{col1.replace('/', '_').replace(' ', '_')}.png"
            plt.savefig(os.path.join(reg_dir, filename))
            plt.close()

# === MAIN FUNCTION ===
# Wczytuje dane i konfigurację, generuje wykresy regresji

def main(input_path, config_path, out_dir):
    print(f"[*] Wczytywanie pliku CSV: {input_path}")
    df = pd.read_csv(input_path)
    print("[✓] Plik CSV wczytany. Liczba kolumn:", len(df.columns))

    print(f"[*] Wczytywanie konfiguracji: {config_path}")
    with open(config_path) as f:
        config = json.load(f)

    numeric_cols = config.get("numeric_columns", [])
    print("[✓] Kolumny numeryczne:", numeric_cols)

    generate_regression_plots(df, numeric_cols, out_dir)

# === CLI ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/dataset.csv', help="Path to CSV file")
    parser.add_argument('--config', default='config/plot_config.json', help="Path to JSON config file")
    parser.add_argument('--out_dir', default='plots', help="Output folder for plots")
    args = parser.parse_args()
    main(args.input, args.config, args.out_dir)