import subprocess
import os


def make_blast_db(fasta, out_prefix):
    subprocess.run([
        "makeblastdb",
        "-in", fasta,
        "-dbtype", "nucl",
        "-out", out_prefix
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def run_blastn(query, db, output):
    subprocess.run([
        "blastn",
        "-query", query,
        "-db", db,
        "-outfmt",
        "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qseq sseq",
        "-out", output
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def get_all_dbs(db_root):
    dbs = []

    for root, _, files in os.walk(db_root):
        for file in files:
            if file.endswith(".nsq"):
                dbs.append(os.path.join(root, file.replace(".nsq", "")))

    return dbs