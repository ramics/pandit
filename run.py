#!/usr/bin/python

import getopt
import os
import pickle
import subprocess
from subprocess import PIPE
import sys
from Bio import AlignIO
from Bio.Align import AlignInfo
from Bio.Alphabet import generic_dna

def run(in_folder, ref_folder, command_file):

    results = {}

    for filename in os.listdir(in_folder):
        in_file = os.path.join(in_folder, filename)
        out_file = "temp_out_" + os.path.basename(command_file)
        ref_file = os.path.join(ref_folder, filename)
        commands = ["/bin/bash", command_file, 
                    in_file,
                    out_file]
        subprocess.call(subprocess.list2cmdline(commands), \
            shell=True)

        ref = AlignIO.read(open(ref_file), "fasta", alphabet=generic_dna)
        summary = AlignInfo.SummaryInfo(ref)
        info_content = summary.information_content(0, len(ref[0]),
                                                 chars_to_ignore = ['N'])
        length = len(ref[0])

        commands = ["qscore", "-test", out_file, "-ref", 
            ref_file, "-cline", "-modeler", "-seqdiffwarn", "-truncname"]

        p = subprocess.Popen(commands, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        try:
            q = float(output.split(";")[2].split('=')[1])
            tc = float(output.split(";")[3].split('=')[1])
            cline = float(output.split(";")[4].split('=')[1])
            modeler = float(output.split(";")[5].split('=')[1])
        except IndexError:
            print subprocess.list2cmdline(commands)
            print output
            print err
            sys.exit(1)

        #os.unlink(out_file)

        result = {
            "length": length,
            "info_content": info_content,
            "scores": [q, tc, cline, modeler]
        }

        results[filename] = result

    out_path = "out/"+os.path.basename(command_file)
    out = open(out_path, "wb")
    pickle.dump(results, out, -1)


def main(argv):

    in_folder = ""
    ref_folder = ""
    command_file = ""

    try:
        opts, args = getopt.getopt(argv,"i:r:c:",[
            "in-folder=",
            "ref-folder=",
            "command-file="
        ])
    except getopt.GetoptError:
        print '[ERROR] Syntax: run.py -i in-folder -r ref-folder -c command-file'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-c", "--command-file"):
            command_file = arg
        elif opt in ("-i", "--in-folder"):
            in_folder = arg
        elif opt in ("-r", "--ref-folder"):
            ref_folder = arg

    run(in_folder, ref_folder, command_file)



if __name__ == "__main__":
    main(sys.argv[1:])