# pandit

Benchmark any nucleotide aligner against 7,738 PANDIT reference alignments.

- `DNA_alignments/`: the curated reference alignments
- `raw_sequences/`: the same sequences with gaps stripped, ready to align
- `run.py`: runs your aligner on every family and scores it with `qscore` (Q, TC, Cline, Modeler)
- `ungap.py`: regenerates `raw_sequences/` from `DNA_alignments/`

## Run

Write a shell script that takes an input FASTA and an output path:

```
# mafft.sh
mafft "$1" > "$2"
```

Then:

```
mkdir out
python run.py -i raw_sequences -r DNA_alignments -c mafft.sh
```

Scores, alignment length and information content per family land in `out/mafft.sh` as a pickle.

Requires Python 2, Biopython (1.77 or earlier) and [`qscore`](https://www.drive5.com/qscore/) on your path.
