# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import os

# # === KONFIGURACJA ===
# INPUT_PATH = "data/dataset.csv"
# OUT_DIR = "plots/dropout_by_parent_occupation"
# HUE = "Target"
# COLUMNS = ["Mother's occupation", "Father's occupation"]

# # === WCZYTANIE DANYCH ===
# os.makedirs(OUT_DIR, exist_ok=True)
# df = pd.read_csv(INPUT_PATH)

# # === GENEROWANIE WYKRESÓW ===
# for col in COLUMNS:
#     if col not in df.columns:
#         print(f"[!] Kolumna nie istnieje: {col}")
#         continue

#     # Top 12 najczęstszych wartości (dla czytelności wykresu)
#     top_vals = df[col].value_counts().nlargest(12).index
#     df_subset = df[df[col].isin(top_vals)]

#     plt.figure(figsize=(12, 6))
#     sns.countplot(data=df_subset, x=col, hue=HUE, order=top_vals)
#     plt.xticks(rotation=90)
#     plt.title(f"Dropout vs {col}")
#     plt.tight_layout()

#     fname = col.replace("/", "_").replace(" ", "_").lower() + ".png"
#     plt.savefig(os.path.join(OUT_DIR, fname))
#     plt.close()

# print("[✓] Wygenerowano wykresy dla zawodów rodziców vs Target")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# === KONFIGURACJA ===
INPUT_PATH = "data/dataset.csv"
HUE = "Target"

# Kolumny do analizy
occupation_columns = ["Mother's occupation", "Father's occupation"]
qualification_columns = ["Mother's qualification", "Father's qualification"]

# Katalogi wyjściowe
OUT_DIR_OCCUPATION = "plots/dropout_by_parent_occupation"
OUT_DIR_QUALIFICATION = "plots/dropout_by_parent_qualification"

# === WCZYTANIE DANYCH ===
os.makedirs(OUT_DIR_OCCUPATION, exist_ok=True)
os.makedirs(OUT_DIR_QUALIFICATION, exist_ok=True)
df = pd.read_csv(INPUT_PATH)

# === FUNKCJA GENERUJĄCA WYKRESY ===
def generate_plots(columns, out_dir, title_prefix):
    for col in columns:
        if col not in df.columns:
            print(f"[!] Kolumna nie istnieje: {col}")
            continue

        # Top 12 najczęstszych wartości dla czytelności wykresu
        top_vals = df[col].value_counts().nlargest(12).index
        df_subset = df[df[col].isin(top_vals)]

        plt.figure(figsize=(12, 6))
        sns.countplot(data=df_subset, x=col, hue=HUE, order=top_vals)
        plt.xticks(rotation=90)
        plt.title(f"{title_prefix} vs {col}")
        plt.tight_layout()

        fname = col.replace("/", "_").replace(" ", "_").lower() + ".png"
        plt.savefig(os.path.join(out_dir, fname))
        plt.close()

# === GENEROWANIE WYKRESÓW ===
generate_plots(occupation_columns, OUT_DIR_OCCUPATION, "Dropout")
generate_plots(qualification_columns, OUT_DIR_QUALIFICATION, "Dropout")

print("[✓] Wygenerowano wykresy dla zawodów i kwalifikacji rodziców vs Target")
