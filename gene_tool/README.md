# \# gene\_tool

# 

# A command-line tool for detecting target genes (e.g., \*ompR\*) across bacterial genome assemblies using custom or NCBI-derived databases.

# 

# \---

# 

# \## 🚀 Overview

# 

# `gene\_tool` enables users to:

# 

# \* Build searchable gene databases from genome assemblies

# \* Detect query genes across multiple genomes

# \* Work with NCBI genome datasets (e.g., \*Escherichia coli\*)

# \* Integrate into larger antimicrobial resistance (AMR) workflows

# 

# \---

# 

# \## ⚙️ Installation

# 

# Clone the repository and install locally:

# 

# ```bash

# https://github.com/AkshatArora654/Locus.git

# cd path/to/dir

# pip install -e .

# ```

# 

# \---

# 

# \## 📦 Input Requirements

# 

# \* Genome assemblies in FASTA format (`.fna`)

# \* Query gene sequence in FASTA format

# \* Assemblies can be downloaded from NCBI using the `datasets` CLI

# 

# \---

# 

# \## 🧬 Example Workflow

# 

# \### 1. Download genomes from NCBI

# 

# ```bash

# datasets summary genome taxon "Escherichia coli" \\

# &#x20; --assembly-level complete,chromosome \\

# &#x20; --assembly-source refseq \\

# &#x20; --as-json-lines | \\

# dataformat tsv genome --fields accession > accessions.tsv

# 

# tail -n +2 accessions.tsv | head -100 > first100\_accessions.txt

# 

# datasets download genome accession \\

# &#x20; --inputfile first100\_accessions.txt \\

# &#x20; --include genome,gff3,gbff \\

# &#x20; --filename ecoli\_100.zip

# 

# python -m zipfile -e ecoli\_100.zip .

# ```

# 

# \---

# 

# \### 2. Organize genome files

# 

# Move and rename genome files into a single directory:

# 

# ```bash

# mkdir ncbi\_assemblies

# 

# for dir in ncbi\_dataset/data/\*; do

# &#x20;   acc=$(basename "$dir")

# &#x20;   cp "$dir"/\*.fna "ncbi\_assemblies/${acc}.fna"

# done

# ```

# 

# \---

# 

# \### 3. Build database

# 

# ```bash

# gene\_tool build-db --ncbi\_dir ncbi\_assemblies/ --db\_dir ecoli\_db/

# ```

# 

# \---

# 

# \### 4. Detect gene of interest

# 

# ```bash

# gene\_tool detect -q ompR.fasta --db\_dir ecoli\_db/

# ```

# 

# \---

# 

# \## 📊 Output

# 

# The tool produces tabular output containing:

# 

# \* Genome accession

# \* Gene detected

# \* Alignment metrics (identity, coverage, etc.)

# 

# Example:

# 

# ```

# Genome        Gene    Identity    Coverage

# GCF\_000005845 ompR    99.2        100

# ```

# 

# \---

# 

# \## 🧠 Key Features

# 

# \* Scalable to hundreds or thousands of genomes

# \* Compatible with NCBI datasets CLI workflows

# \* Modular design for integration into AMR pipelines

# \* Supports custom genome collections

# 

# \---

# 

# \## 📁 Project Structure

# 

# ```

# gene\_tool/

# ├── gene\_tool/          # source code

# ├── data/               # optional test data

# ├── tests/              # unit tests

# ├── README.md

# ├── setup.py

# └── requirements.txt

# ```

# 

# \---

# 

# \## ⚠️ Notes

# 

# \* Ensure genome files are properly named and formatted (`.fna`)

# \* Large genome downloads may require significant disk space

# \* Database build time depends on number of genomes

# 

# \---

# 

# \## 🔧 Future Development

# 

# \* Integration with AMR detection tools (e.g., AMRFinderPlus)

# \* Metadata integration (host, location, clinical source)

# \* Parallelized database building and querying

# \* Support for additional input formats

# 

# \---

# 

# \## 👤 Author

# 

# Developed by Akshat Arora

# 

# \---

# 

# \## 📜 License

# 

# Private repository — not for distribution.



