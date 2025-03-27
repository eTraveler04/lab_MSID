import argparse, sys, os
import pandas as pd
import matplotlib.pyplot as plt

def main(input_path, out_dir):
    df = pd.read_csv(sys.stdin) if input_path in ('-', None) else pd.read_csv(input_path)
    os.makedirs(out_dir, exist_ok=True)

    for col in df.select_dtypes(include='number').columns:
        data = df[col].dropna()
        if data.empty:
            continue

        plt.figure()
        plt.violinplot(data, showmeans=True)
        plt.title(f'Violinplot: {col}')
        plt.ylabel(col)

        safe = col.replace('/', '_').replace(' ', '_')
        plt.savefig(os.path.join(out_dir, f'{safe}_violin.png'))
        plt.close()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--input', default='-', help="Path to CSV file or '-' for stdin")
    p.add_argument('--out_dir', default='violin_plots', help="Output directory")
    args = p.parse_args()
    main(args.input, args.out_dir)
