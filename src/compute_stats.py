import argparse
import sys
import json
import pandas as pd

# === NUMERIC FEATURE STATS ===
# Oblicza statystyki opisowe dla cech numerycznych:
# średnia, mediana, min, max, odchylenie standardowe,
# 5-ty i 95-ty percentyl, liczba braków

def numeric_stats(df: pd.DataFrame) -> pd.DataFrame:
    stats = df.describe(percentiles=[.05, .95]).T  # T = transpozycja, kolumny jako wiersze
    stats['missing'] = df.isna().sum()  # liczba brakujących wartości
    stats.rename(columns={'50%': 'median', '5%': '5th_pct', '95%': '95th_pct'}, inplace=True)
    return stats[['mean', 'median', 'min', 'max', 'std', '5th_pct', '95th_pct', 'missing']]


# === CATEGORICAL FEATURE STATS ===
# Rozdziela obliczenia na dwa zestawy:
# - distribution: proporcje wartości
# - summary: liczba unikalnych klas i braki

def categorical_stats(df: pd.DataFrame):
    distribution_rows = []
    summary_rows = []
    total = len(df)

    for col in df.columns:
        unique = df[col].nunique(dropna=True)  # liczba unikalnych klas
        missing = df[col].isna().sum()  # liczba braków

        summary_rows.append({
            'feature': col,
            'unique_classes': unique,
            'missing': missing
        })

        for val, cnt in df[col].value_counts(dropna=False).items():
            distribution_rows.append({
                'feature': col,
                'value': val,
                'proportion': cnt / total
            })

    return pd.DataFrame(summary_rows), pd.DataFrame(distribution_rows)


# === MAIN FUNCTION ===
# Wczytuje plik CSV i plik JSON z konfiguracją,
# wybiera kolumny numeryczne i kategorialne,
# generuje statystyki i zapisuje je jako pliki CSV

def main(input_path, config_path, numeric_out, categorical_summary_out, categorical_distribution_out):
    df = pd.read_csv(sys.stdin) if input_path in ('-', None) else pd.read_csv(input_path)

    with open(config_path) as f:
        config = json.load(f)

    numeric_cols = config.get('numeric_columns', [])
    categorical_cols = config.get('categorical_columns', [])

    num_df = numeric_stats(df[numeric_cols])
    cat_summary_df, cat_dist_df = categorical_stats(df[categorical_cols])

    num_df.to_csv(numeric_out)
    cat_summary_df.to_csv(categorical_summary_out, index=False)
    cat_dist_df.to_csv(categorical_distribution_out, index=False)


# === ARGUMENTY Z LINI KOMEND ===
# Ustawiono domyślne ścieżki, aby nie trzeba było ich podawać przy każdym uruchomieniu

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/dataset.csv', help="Path to CSV file")
    parser.add_argument('--config', default='config/plot_config.json', help="Path to JSON config file")
    parser.add_argument('--numeric_out', default='data/results/numeric_stats.csv')
    parser.add_argument('--categorical_summary_out', default='data/results/categorical_summary.csv')
    parser.add_argument('--categorical_distribution_out', default='data/results/categorical_distribution.csv')
    args = parser.parse_args()
    main(
        args.input,
        args.config,
        args.numeric_out,
        args.categorical_summary_out,
        args.categorical_distribution_out
    )   
