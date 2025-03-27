import subprocess

# === ŚCIEŻKI DO SKRYPTÓW ===
scripts = [
    "src/compute_stats.py",
    "src/generate_plots.py",
    "src/generate_error_bars.py",
    "src/generate_heatmap.py",
    "src/generate_reg.py",
    "src/dropout_parents.py",
    "src/generate_hist.py"
]

print("[✓] Uruchamianie wszystkich etapów analizy danych...\n")

for script in scripts:
    print(f"[*] Uruchamiam: {script}")
    try:
        subprocess.run(["python", script], check=True)
        print(f"[✓] Zakończono: {script}\n")
    except subprocess.CalledProcessError as e:
        print(f"[!] Błąd w czasie wykonywania {script}: {e}\n")

print("[✓] Wszystkie skrypty wykonane.")
