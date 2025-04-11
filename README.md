# MSID Data Statistics

# Dane pochodzą z Predict Students' Dropout and Academic Success
Marital status,Application mode,Application order,Course,Daytime/evening attendance,Previous qualification,Nacionality,Mother's qualification,Father's qualification,Mother's occupation,Father's occupation,Displaced,Educational special needs,Debtor,Tuition fees up to date,Gender,Scholarship holder,Age at enrollment,International,Curricular units 1st sem (credited),Curricular units 1st sem (enrolled),Curricular units 1st sem (evaluations),Curricular units 1st sem (approved),Curricular units 1st sem (grade),Curricular units 1st sem (without evaluations),Curricular units 2nd sem (credited),Curricular units 2nd sem (enrolled),Curricular units 2nd sem (evaluations),Curricular units 2nd sem (approved),Curricular units 2nd sem (grade),Curricular units 2nd sem (without evaluations),Unemployment rate,Inflation rate,GDP,Target

## Link do danych 
https://www.kaggle.com/datasets/naveenkumar20bps1137/predict-students-dropout-and-academic-success


## Setup

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/eTraveler04/lab_MSID.git

# 2. Przejdź do katalogu repozytorium
cd nazwa-repo

# 3. Upewnij się, że jesteś na gałęzi main
git checkout main

# 4. Pobierz najnowsze zmiany z gałęzi main
git pull origin main

# 5. Środowisko
conda activate ( np. msid )
pip install -r requirements.txt
```

# Aby uruchomić wszystkie skrypty jednocześnie 
- python src/run_all.py

## Skrypt do obliczania i zapisywania wstępnych statystyk cech do pliku CSV
● Dla cech numerycznych: średnia, mediana, wartość minimalna, maksymalna,
odchylenie standardowe, 5-ty i 95-ty percentyl, liczba brakujących wartości w
kolumnie.
● Dla cech kategorialnych: liczba unikalnych klas, liczba brakujących wartości w
kolumnie, proporcja klas.

- python src/compute_stats.py

## Wykorzystanie violinplotów & boxplotów
- python src/generate_plots.py

## Error bar   
- python src/generate_error_bars.p

## Heatmap
- python src/generate_heatmanp.py

## Regresja liniowa  
- python src/generate_reg.py

## Wydrukowanie % dla płci 
- python src/analyze_dropout_gender.py





# Boxplot (czyli wykres pudełkowy) pokazuje rozkład wartości numerycznych:
● rodkowa linia: mediana
● pudełko: rozpiętość między kwartylem dolnym (Q1) a górnym (Q3)
● wąsy (whiskers): minimalne i maksymalne wartości w zakresie 1.5 * IQR
● kropki poza wąsami: potencjalne wartości odstające (outliers)

📈 Użycie: kiedy chcesz porównać rozkład liczbowych zmiennych w różnych grupach kategorycznych

# Violinplot to rozszerzony boxplot:
● pokazuje dokładniejszy kształt rozkładu za pomocą gęstości jądrowej (kernel density)
● pozwala zobaczyć np. czy rozkład jest symetryczny, jednolity, ma kilka szczytów (modów)

📈 Użycie: kiedy chcesz porównać pełny rozkład wartości numerycznych między kategoriami, nie tylko medianę i kwartyle.

# Error bars
🔗 Seaborn tutorial – error bars

Wizualizacja wartości średnich cech numerycznych z przedziałami ufności lub błędem standardowym. Pokazuje nie tylko średnią, ale też niepewność pomiaru.

📈 Dlaczego się tego używa:
● do porównywania średnich pomiędzy grupami (np. dropout vs graduate)
● do analizy zmienności cech
● do oceny pewności danych (czy grupy istotnie się różnią)

# Historiogram 
🔗 Seaborn tutorial – distributions

Histogram to wykres pokazujący rozkład wartości dla jednej zmiennej numerycznej. Oś X to przedziały, a oś Y to liczba obserwacji.

📈 Dlaczego się tego używa:
● do sprawdzenia, czy cecha ma rozkład normalny, skośny, rozproszony
● o identyfikacji wartości odstających
● do oceny gęstości danych

## Histogram :
- Analizuje tylko jedną cechę numeryczną
* Traktuje cały zbiór jako jedną grupę

## Histogram warunkowy (hue):
🔗 Histogram z hue

Histogramy pokazujące rozkład cechy oddzielnie dla każdej wartości innej cechy (np. osobno dla mężczyzn i kobiet). To histogramy z podziałem na kategorie.

📈 Dlaczego się tego używa:
● porównanie rozkładów w różnych grupach (np. Gender, Target)
● widzisz czy np. kobiety są młodsze, mają wyższe oceny itp.
● wykrywanie różnic ukrytych w ogólnej populacji

# Heatmap
To wizualna reprezentacja macierzy korelacji między zmiennymi liczbowymi. Pokazuje, jak bardzo jedna zmienna jest powiązana z drugą — zarówno co do kierunku (dodatnia/ujemna), jak i siły związku.
Heatmapę korelacji zawsze tworzy się tylko na kolumnach numerycznych, ponieważ
korelacja (np. współczynnik Pearsona) mierzy siłę i kierunek liniowego związku między zmiennymi liczbowymi.

# Regresja linowa
To technika statystyczna służąca do modelowania zależności między dwiema zmiennymi liczbowymi:

● jedna zmienna to cecha niezależna (X)
● druga to cecha zależna (Y)
● Regresja próbuje dopasować prostą linię, która najlepiej opisuje zależność między nimi.

