import subprocess
import os
import pandas as pd


# ==============================
# CHECK MAFFT
# ==============================
def check_mafft():
    try:
        subprocess.run(
            ["mafft", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except FileNotFoundError:
        return False


# ==============================
# WRITE FASTA FOR ALIGNMENT
# ==============================
def write_alignment_fasta(df, outfile):

    if df.empty:
        print("[WARNING] No data for alignment")
        return

    # Keep only valid sequences
    valid_df = df[
        df["subject_sequence"].notna() &
        (df["subject_sequence"] != "")
    ]

    if valid_df.empty:
        print("[WARNING] No valid sequences found for alignment")
        return

    count = 0

    with open(outfile, "w") as f:
        for _, row in valid_df.iterrows():

            seq = row["subject_sequence"]

            # Extra safety: skip very short junk hits
            if len(seq) < 30:
                continue

            header = f">{row['sample']}|{row['subject_id']}"

            f.write(header + "\n")
            f.write(seq + "\n")

            count += 1

    print(f"[INFO] Wrote {count} sequences to {outfile}")


# ==============================
# RUN MAFFT (SAFE)
# ==============================
def run_mafft(input_fasta, output_fasta):

    with open(output_fasta, "w") as out:
        result = subprocess.run(
            ["mafft", "--auto", input_fasta],
            stdout=out,
            stderr=subprocess.PIPE,
            text=True
        )

    if result.returncode != 0:
        print("[ERROR] MAFFT failed:")
        print(result.stderr)