# Locus

A lightweight command-line tool to detect specific gene variants (e.g., *ompR*) across bacterial genome assemblies using custom or NCBI datasets.

---

## Features

* Build BLAST databases from genome assemblies
* Detect query genes across multiple isolates
* Support for both local (e.g. wastewater) and NCBI datasets
* Optional multiple sequence alignment using MAFFT
* Clean, combined output for downstream analysis

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/AkshatArora654/Locus
cd Locus
```

---

### 2. Create environment (recommended)

```bash
conda create -n locus python=3.10
conda activate locus
```

---

### 3. Install dependencies

```bash
conda install -c bioconda blast mafft
pip install pandas
```

---

### 4. Install Locus

```bash
pip install -e .
```

---

## Input Requirements

### Genome assemblies

* Format: `.fasta` or `.fna`
* One file per isolate

### Query gene

* Format: FASTA (DNA sequence)

Example:

```
>ompR
ATGCGT...
```

---

## Usage

### 1. Build BLAST databases

#### Local isolates (e.g. wastewater)

```bash
locus build-db --ww --ww_dir data/
```

#### NCBI genomes

```bash
locus build-db --ncbi --ncbi_dir ncbi_assemblies/
```

#### Both datasets

```bash
locus build-db --all --ww_dir data/ --ncbi_dir ncbi_assemblies/
```

---

### 2. Detect gene

```bash
locus detect -q ompR.fasta --ncbi --output results.tsv
```

---

### 3. Run alignment (optional)

```bash
locus detect -q ompR.fasta --ncbi --output results.tsv --align
```

---

## Output

### 1. Results table (TSV)

Example:

```
results.tsv
```

Contains:

* query_id
* subject_id
* percent_identity
* alignment_length
* mismatches
* gap_opens
* query_start / end
* subject_start / end
* evalue
* bit_score
* query_sequence
* subject_sequence
* sample

---

### 2. Alignment file (optional)

Generated when `--align` is used:

```
results_alignment.fasta
```

Can be visualized in:

* Jalview
* AliView
* MEGA

---

## Example Workflow

```bash
# Build databases
locus build-db --ncbi --ncbi_dir ncbi_assemblies/

# Detect gene
locus detect -q ompR.fasta --ncbi --output ompR_results.tsv --align
```

---

## Directory Structure

```
db/
├── ww/
│   ├── sample1/
│   │   └── db.*
│   └── sample2/
│       └── db.*
└── ncbi/
    ├── GCF_XXXXX/
    │   └── db.*
```

---

## Notes

* Requires BLAST+ (`makeblastdb`, `blastn`)
* Alignment requires MAFFT
* Temporary files are handled automatically
* Results are combined into a single output file

---

## Limitations

* Uses BLAST hit sequences (may be partial gene fragments)
* Multiple hits per isolate are not yet filtered

---

## Future Improvements

* Full gene extraction using BLAST coordinates
* Best-hit filtering per isolate
* Variant calling and comparison
* Integration with GFF/GBFF annotations

---

## Author

Akshat Arora
