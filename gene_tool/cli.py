import argparse
import os
import pandas as pd
import tempfile

from gene_tool.blast import (
    make_blast_db,
    run_blastn,
    get_all_dbs
)
from gene_tool.parser import parse_blast
from gene_tool.alignment import write_alignment_fasta, run_mafft, check_mafft


# ==============================
# BUILD DATABASES
# ==============================

def build_ncbi_dbs(ncbi_dir, db_root):

    os.makedirs(db_root, exist_ok=True)

    for root, dirs, files in os.walk(ncbi_dir):

        for file in files:
            if not file.endswith(".fna"):
                continue

            fasta_path = os.path.join(root, file)
            sample_id = file.replace(".fna", "")

            sample_db_dir = os.path.join(db_root, sample_id)
            os.makedirs(sample_db_dir, exist_ok=True)

            out_prefix = os.path.join(sample_db_dir, "db")

            if os.path.exists(out_prefix + ".nsq"):
                print(f"[SKIP] {sample_id}")
                continue

            print(f"[BUILD] {sample_id}")
            make_blast_db(fasta_path, out_prefix)


def build_ww_dbs(ww_dir, db_root):

    os.makedirs(db_root, exist_ok=True)

    for fasta in os.listdir(ww_dir):
        if not fasta.endswith(".fasta"):
            continue

        sample_id = fasta.split(".")[0]

        fasta_path = os.path.join(ww_dir, fasta)
        sample_db_dir = os.path.join(db_root, sample_id)

        os.makedirs(sample_db_dir, exist_ok=True)

        out_prefix = os.path.join(sample_db_dir, "db")

        if os.path.exists(out_prefix + ".nsq"):
            print(f"[SKIP] {sample_id}")
            continue

        print(f"[BUILD] {sample_id}")
        make_blast_db(fasta_path, out_prefix)


# ==============================
# DETECTION
# ==============================

def run_detection(query, db_root, output_file, align=False):

    dbs = get_all_dbs(db_root)

    if not dbs:
        print("[ERROR] No databases found.")
        return

    all_results = []

    for db in dbs:
        sample_id = os.path.basename(os.path.dirname(db))

        with tempfile.NamedTemporaryFile(delete=True) as tmp:

            run_blastn(query, db, tmp.name)

            if os.path.getsize(tmp.name) > 0:
                with open(tmp.name) as f:
                    blast_output = f.read()

                df = parse_blast(blast_output, sample_id)
                all_results.append(df)

    if not all_results:
        print("[INFO] No hits found.")
        return

    final_df = pd.concat(all_results)
    final_df.to_csv(output_file, sep="\t", index=False)

    print(f"[DONE] Results saved to {output_file}")

    # ==============================
    # ALIGNMENT (FIXED INDENTATION)
    # ==============================
    if align:

        if not check_mafft():
            print("[WARNING] MAFFT not found, skipping alignment")
            return

        base = os.path.splitext(output_file)[0]
        alignment_file = f"{base}_alignment.fasta"

        # ---- Write sequences ----
        write_alignment_fasta(final_df, alignment_file)

        # ---- Check BEFORE MAFFT ----
        if not os.path.exists(alignment_file) or os.path.getsize(alignment_file) == 0:
            print("[WARNING] Alignment file empty before MAFFT — skipping")
            return

        print(f"[DEBUG] File size before MAFFT: {os.path.getsize(alignment_file)}")

        # ---- Run MAFFT safely ----
        tmp_aln = alignment_file + ".tmp"

        run_mafft(alignment_file, tmp_aln)

        # ---- Check MAFFT output ----
        if not os.path.exists(tmp_aln) or os.path.getsize(tmp_aln) == 0:
            print("[WARNING] MAFFT output empty — keeping original sequences")
            return

        # ---- Replace ONLY if valid ----
        os.replace(tmp_aln, alignment_file)

        print(f"[DONE] Alignment saved to {alignment_file}")


# ==============================
# CLI ENTRY POINT
# ==============================

def main():
    parser = argparse.ArgumentParser(prog="gene_tool")

    subparsers = parser.add_subparsers(dest="command")

    # ------------------------------
    # BUILD
    # ------------------------------
    build = subparsers.add_parser("build-db")

    build.add_argument("--ww_dir", default="data/")
    build.add_argument("--ncbi_dir")

    build.add_argument("--ww", action="store_true")
    build.add_argument("--ncbi", action="store_true")
    build.add_argument("--all", action="store_true")

    # ------------------------------
    # DETECT
    # ------------------------------
    detect = subparsers.add_parser("detect")

    detect.add_argument("-q", "--query", required=True)
    detect.add_argument("-o", "--output", default="results.tsv")
    detect.add_argument("--align", action="store_true")

    detect.add_argument("--ww", action="store_true")
    detect.add_argument("--ncbi", action="store_true")
    detect.add_argument("--all", action="store_true")

    args = parser.parse_args()

    DB_DIR = "db"
    NCBI_DB = os.path.join(DB_DIR, "ncbi")
    WW_DB = os.path.join(DB_DIR, "ww")

    # ------------------------------
    # BUILD
    # ------------------------------
    if args.command == "build-db":

        if not (args.ww or args.ncbi or args.all):
            print("[ERROR] Specify --ww, --ncbi, or --all")
            return

        if args.ncbi or args.all:
            if not args.ncbi_dir:
                print("[ERROR] Provide --ncbi_dir")
                return
            build_ncbi_dbs(args.ncbi_dir, NCBI_DB)

        if args.ww or args.all:
            build_ww_dbs(args.ww_dir, WW_DB)

    # ------------------------------
    # DETECT
    # ------------------------------
    elif args.command == "detect":

        if not os.path.exists(DB_DIR):
            print("[ERROR] Run build-db first.")
            return

        if args.all:
            search_dir = DB_DIR
        elif args.ww:
            search_dir = WW_DB
        elif args.ncbi:
            search_dir = NCBI_DB
        else:
            print("[ERROR] Specify --ww, --ncbi, or --all")
            return

        run_detection(args.query, search_dir, args.output, args.align)

    else:
        parser.print_help()