import argparse, sys, os
import pandas as pd
import matplotlib.pyplot as plt # do wkyresów skrzynkowych 

def main(input_path, out_dir):
    # Wczytanie
    df = pd.read_csv(sys.stdin) if input_path in ('-', None) else pd.read_csv(input_path)
    os.makedirs(out_dir, exist_ok=True)

    # Dla każdej cechy numerycznej
    for col in df.select_dtypes(include='number').columns:
        plt.figure()
        df.boxplot(column=col)
        plt.title(f'Boxplot: {col}')
        plt.tight_layout()
        safe_col = col.replace('/', '_').replace(' ', '_')
        filename = f"{safe_col}_boxplot.png"
        plt.savefig(os.path.join(out_dir, filename))
        plt.close()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--input', default='-', help="Path to CSV or '-' for stdin")
    p.add_argument('--out_dir', default='plots', help="Folder for PNG files")
    args = p.parse_args()
    main(args.input, args.out_dir)
