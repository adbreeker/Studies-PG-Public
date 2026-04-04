# Elements of Bioinformatics

This repository contains coursework for Elements of Bioinformatics, focused on practical problem solving, algorithm design, and implementation of core bioinformatics methods in Python. The work is organized as a progression from basic sequence manipulation to alignment, assembly, phylogeny, and biological databases.

## 🧭 Course Overview

The course combines:
- Rosalind-based algorithmic exercises.
- Lab experiments that merge multiple solved tasks into small end-to-end pipelines.
- Visual analysis using plots and summary statistics.
- Report-style interpretation of biological results.

In total, this project includes:
- 5 implementation-heavy labs with standalone problem solutions and experiment scripts.
- 1 report-focused lab dedicated to biological databases and evidence analysis.
- Reusable helper logic for sequence parsing, transformations, and comparisons.
- Validation screenshots and figures stored in each lab's Images directory.

## 🎯 Learning Goals

By working through this repository, the main learning goals are to:
- Understand and implement fundamental sequence operations on DNA, RNA, and proteins.
- Apply dynamic programming techniques to sequence comparison problems.
- Build intuition for assembly and overlap-based reconstruction.
- Work with phylogenetic distances and tree representations (including Newick).
- Practice reproducible analysis and concise interpretation of computational results.

## 🧪 Lab-by-Lab Topics

- **Lab1:** DNA/RNA basics, reverse complement, Hamming distance, motifs, translation, GC content.
- **Lab2:** ORFs, RNA splicing, motifs in proteins, consensus/profile, protein mass, mRNA inference.
- **Lab3:** Sequence comparison and dynamic programming (LCS, edit distance, global/local alignment).
- **Lab4:** Overlap graphs, shortest superstring assembly, read error correction, RNA matching variants.
- **Lab5:** Population/tree tasks, distance matrices, Newick parsing, phylogenetic reconstruction.
- **Lab6:** Report-style work on biological databases, evidence quality, and reproducibility.

Typical workflow in each lab:
- Solve individual Rosalind tasks as dedicated problem files.
- Reuse those implementations inside experiment.py.
- Run experiments on provided input files.
- Generate charts and short interpretations in the lab README.

## 📁 Repository Structure

```text
Lab1/..Lab5/   problem solutions + experiment.py + Inputs/ + Images/
Lab6/          final report material
SPOJ/          additional algorithmic practice (Python/C++)
requirements.txt
```

Notes:
- Each lab directory contains its own README with explanations and result snapshots.
- Inputs are mainly Rosalind datasets stored in per-lab Inputs folders.
- Images contains generated plots and validation evidence.

## 🛠️ Tech Stack

- Python 3
- biopython
- matplotlib
- requests
- pyperclip

Primary language and style:
- Most tasks are implemented in clear, direct Python scripts.
- Some additional algorithmic exercises are included in SPOJ (Python/C++).

## ▶️ Setup and Run

Install dependencies once:

```bash
pip install -r requirements.txt
```

Run an experiment (example):

```bash
python Lab3/experiment.py
```

You can also run problem-level scripts directly, for example:

```bash
python Lab1/problem1_DNA.py
python Lab4/problem3_CORR.py
```

## ✅ Validation and Outputs

The repository includes:
- Rosalind pass confirmations for the covered tasks.
- Lab-level result summaries.
- Generated figures such as nucleotide composition plots, ORF distributions, dotplots, overlap statistics, and phylogenetic visualizations.

This makes it possible to inspect both correctness (problem solving) and interpretation (analysis quality).

## 📚 Learning Outcome

The course builds a practical path from sequence basics to higher-level computational biology topics. It emphasizes:
- implementable algorithms,
- reusable code across tasks,
- reproducible experiments,
- and clear communication of results.

Overall, this repository documents hands-on training in computational bioinformatics through a mix of algorithmic exercises and mini research-style analyses.
