#!/usr/bin/python

from Bio import SeqIO
import sys
import os

def ungap_seq(record):
    record.seq = record.seq.ungap('-').ungap('.')
    return record

def main(argv):
    in_folder = argv[0]
    out_folder = argv[1]
    for filename in os.listdir(in_folder):
        sequences = SeqIO.parse(os.path.join(in_folder, filename), "fasta")
        out_handle = open(os.path.join(out_folder, filename), 'w')

        seq_iterator = (ungap_seq(record) \
            for record in sequences)

        SeqIO.write(seq_iterator, out_handle, 'fasta')

if __name__ == "__main__":
  main(sys.argv[1:])