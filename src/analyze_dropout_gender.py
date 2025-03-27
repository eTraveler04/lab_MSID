import pandas as pd

def main(input_path="data/dataset.csv"):
    # Wczytanie danych
    # print("halo")
    df = pd.read_csv(input_path)

    # Filtrowanie studentów, którzy zrezygnowali
    dropouts = df[df["Target"] == "Dropout"]

    # Obliczenie udziału płci wśród Dropout (0 = mężczyzna, 1 = kobieta)
    gender_percent = dropouts["Gender"].value_counts(normalize=True) * 100

    # Wyświetlenie wyników
    print("Udział płci wśród studentów, którzy zrezygnowali ze studiów (Dropout):\n")
    print(f"Mężczyźni: {gender_percent.get(0, 0):.2f}%")
    print(f"Kobiety: {gender_percent.get(1, 0):.2f}%")

if __name__ == "__main__":
    main()
