# pandit

**Benchmark any DNA aligner against 7,738 curated PANDIT alignments.**

[PANDIT](https://doi.org/10.1093/nar/gkj087) pairs Pfam protein-domain families with their coding-DNA alignments, which makes it a ready-made truth set for aligners that work on coding sequence. This repo packages that truth set with a harness that runs your aligner over every family and scores the result with [qscore](https://www.drive5.com/qscore/).

## Contents

| Path | What it is |
|---|---|
| `DNA_alignments/` | 7,738 reference DNA alignments, one per Pfam family |
| `raw_sequences/` | The same sequences with gaps stripped: the aligner's input |
| `ungap.py` | Regenerates `raw_sequences/` from `DNA_alignments/` |
| `run.py` | Runs an aligner over every family and scores it |

## Run a benchmark

Write a shell script that takes an input FASTA and an output path:

```
# mafft.sh
mafft "$1" > "$2"
```

Then:

```
mkdir -p out
python run.py -i raw_sequences -r DNA_alignments -c mafft.sh
```

Results are pickled to `out/mafft.sh` as a dict keyed by family:

```python
{"PF00001_DNAalignments.txt": {
    "length": ...,        # reference alignment length
    "info_content": ...,  # information content of the reference
    "scores": [Q, TC, Cline, Modeler]}}
```

## Requirements

Python 2, Biopython < 1.78 and `qscore` on your `PATH`.
