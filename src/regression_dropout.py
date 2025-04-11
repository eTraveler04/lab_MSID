import argparse
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

def main():
    # Użycie argparse do pobrania ścieżki do pliku CSV z danymi
    parser = argparse.ArgumentParser(description='Regresja logistyczna dropout na podstawie Age at enrollment.')
    parser.add_argument('--data', type=str, default='data/dataset.csv', help='Ścieżka do pliku CSV z danymi')
    parser.add_argument('--summary_out', type=str, default='model_summary.txt', help='Ścieżka do zapisu podsumowania modelu w formacie tekstowym')
    args = parser.parse_args()

    # Sprawdzenie, czy plik istnieje
    if not os.path.exists(args.data):
        raise FileNotFoundError(f"Plik {args.data} nie istnieje.")

    # Wczytanie danych
    data = pd.read_csv(args.data)
    print("Pierwsze kilka wierszy danych:")
    print(data.head())

    # Stworzenie zmiennej binarnej 'is_dropout'
    # Przyjmujemy, że gdy wartość w kolumnie Target to 'Dropout' (bez względu na wielkość liter), przyjmujemy 1, w przeciwnym razie 0.
    data['is_dropout'] = data['Target'].apply(lambda x: 1 if x.strip().lower() == 'dropout' else 0)

    # Wybór jednego predyktora: 'Age at enrollment'
    X = data[['Age at enrollment']]
    y = data['is_dropout']

    # Dodanie stałej (intercept) do modelu
    X = sm.add_constant(X)

    # Dopasowanie modelu logistycznego (Logit)
    logit_model = sm.Logit(y, X)
    result = logit_model.fit(disp=False)  # disp=False, aby nie wypisywać zbędnych informacji podczas dopasowania

    print("\nPodsumowanie modelu:")
    print(result.summary())

    # Zapis podsumowania modelu jako tekst do pliku
    summary_text = result.summary2().as_text()
    with open(args.summary_out, 'w') as f:
        f.write(summary_text)
    print(f"\nPodsumowanie modelu zapisane do pliku: {args.summary_out}")

    # Przygotowanie wizualizacji:
    # Tworzymy wektor wartości 'Age at enrollment' w obrębie przedziału danych
    age_min = data['Age at enrollment'].min()
    age_max = data['Age at enrollment'].max()
    age_range = np.linspace(age_min, age_max, 300)

    # Przygotowanie DataFrame do predykcji
    X_vis = pd.DataFrame({'const': 1, 'Age at enrollment': age_range})
    predicted_prob = result.predict(X_vis)

    # Ustawienie stylu dla wykresu przy użyciu seaborn
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 5))
    plt.plot(age_range, predicted_prob, label='Prawdopodobieństwo dropout', color='blue')
    plt.xlabel('Age at enrollment')
    plt.ylabel('Prawdopodobieństwo dropout')
    plt.title('Wpływ wieku przy rekrutacji na prawdopodobieństwo dropout')
    plt.legend()
    plt.grid(True)

    # Utworzenie katalogu na wykresy jeśli nie istnieje
    os.makedirs('plots', exist_ok=True)
    # Zapis wykresu
    plot_path = os.path.join('plots', 'reg_dropout.png')
    plt.savefig(plot_path)
    print(f"Wykres zapisany do: {plot_path}")
    plt.show()

if __name__ == '__main__':
    main()
