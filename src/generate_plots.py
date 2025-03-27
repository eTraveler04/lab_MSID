import argparse
import sys
import os
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === BOXPLOT & VIOLINPLOT GENERATOR ===
# Tworzy wykresy boxplot i violinplot dla każdej pary: kolumna numeryczna + hue
# Dodatkowo tworzy wspólny wykres dla pierwszych dwóch hue na raz (combined)

def generate_box_violin_plots(df, numeric_cols, hue_cols, out_dir):
    box_dir = os.path.join(out_dir, "boxplots")
    violin_dir = os.path.join(out_dir, "violinplots")
    combined_dir = os.path.join(out_dir, "combined_plots")
    os.makedirs(box_dir, exist_ok=True)
    os.makedirs(violin_dir, exist_ok=True)
    os.makedirs(combined_dir, exist_ok=True)

    for num_col in numeric_cols:
        if num_col not in df.columns:
            print(f"[!] Pominięto brakującą kolumnę numeryczną: {num_col}")
            continue
        for hue_col in hue_cols:
            if hue_col not in df.columns:
                print(f"[!] Pominięto brakującą kolumnę hue: {hue_col}")
                continue

            print(f"[*] Tworzenie wykresów dla: {num_col} by {hue_col}")

            safe_num = num_col.replace('/', '_').replace(' ', '_')
            safe_hue = hue_col.replace('/', '_').replace(' ', '_')
            fname = f"{safe_num}_by_{safe_hue}.png"

            # Boxplot
            plt.figure(figsize=(8, 5))
            sns.boxplot(data=df, x=hue_col, y=num_col)
            plt.title(f"Boxplot: {num_col} by {hue_col}")
            plt.tight_layout()
            plt.savefig(os.path.join(box_dir, fname))
            plt.close()

            # Violinplot
            plt.figure(figsize=(8, 5))
            sns.violinplot(data=df, x=hue_col, y=num_col)
            plt.title(f"Violinplot: {num_col} by {hue_col}")
            plt.tight_layout()
            plt.savefig(os.path.join(violin_dir, fname))
            plt.close()

        # === COMBINED PLOT: pierwsze dwa hue w jednym ===
        if len(hue_cols) >= 2:
            hue1, hue2 = hue_cols[0], hue_cols[1]
            if hue1 in df.columns and hue2 in df.columns:
                print(f"[*] Tworzenie COMBINED wykresu dla: {num_col} by {hue1} + {hue2}")
                plt.figure(figsize=(8, 5))
                sns.boxplot(data=df, x=hue1, y=num_col, hue=hue2)
                plt.title(f"Combined Boxplot: {num_col} by {hue1} and {hue2}")
                plt.tight_layout()
                fname = f"{safe_num}_by_{hue1}_and_{hue2}.png".replace(' ', '_')
                plt.savefig(os.path.join(combined_dir, fname))
                plt.close()


# === MAIN FUNCTION ===
# Wczytuje dane i konfigurację, generuje wykresy

def main(input_path, config_path, out_dir):
    print(f"[*] Wczytywanie pliku CSV: {input_path}")
    df = pd.read_csv(sys.stdin) if input_path in ('-', None) else pd.read_csv(input_path)
    print("[✓] Plik CSV wczytany. Liczba kolumn:", len(df.columns))

    print(f"[*] Wczytywanie konfiguracji: {config_path}")
    with open(config_path) as f:
        config = json.load(f)

    numeric_cols = config.get('numeric_columns', [])
    hue_cols = config.get('hue_columns', [])

    print("[✓] Kolumny numeryczne:", numeric_cols)
    print("[✓] Kolumny hue:", hue_cols)

    generate_box_violin_plots(df, numeric_cols, hue_cols, out_dir)


# === CLI ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/dataset.csv', help="Path to CSV file")
    parser.add_argument('--config', default='config/plot_config.json', help="Path to JSON config file")
    parser.add_argument('--out_dir', default='plots', help="Output folder for plots")
    args = parser.parse_args()
    main(args.input, args.config, args.out_dir)
