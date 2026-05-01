import pandas as pd
from io import StringIO


def parse_blast(blast_output, sample_id):
    cols = [
        "query_id",
        "subject_id",
        "percent_identity",
        "alignment_length",
        "mismatches",
        "gap_opens",
        "query_start",
        "query_end",
        "subject_start",
        "subject_end",
        "evalue",
        "bit_score",
        "query_sequence",
        "subject_sequence"
    ]

    if not blast_output.strip():
        return pd.DataFrame(columns=cols + ["sample"])

    df = pd.read_csv(StringIO(blast_output), sep="\t", names=cols)
    df["sample"] = sample_id

    return df