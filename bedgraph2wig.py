#!/usr/bin/env python3

"""
Simple script to convert 'bedgraph' file to non-sparse 'wig' format.
Copyright 2018 Thaddeus Seher
"""

# Example 'bedgraph' input:
#   Ca21chr4        0       11      0.15647
#   Ca21chr4        11      12      0.20862
#   Ca21chr4        12      28      0.26078
#   Ca21chr4        28      45      0.31294
#   Ca21chr4        45      49      0.26078
#   Ca21chr1        3188509 3188512 0.36509
#   Ca21chr1        3188512 3188515 0.41725
#   Ca21chr1        3188515 3188520 0.36509
#   Ca21chr1        3188520 3188535 0.31294
#   Ca21chr2        0       3       0.52156
#   Ca21chr2        3       6       0.57372
#   Ca21chr2        6       15      0.62587
#   Ca21chr2        15      16      0.67803

# Example 'wig' output:
#   track type=WIG
#   variableStep chrom=Ca21chr4
#   0       0.15647
#   1       0.15647
#   2       0.15647
#   3       0.15647
#   4       0.15647
#   5       0.15647
#   variableStep chrom=Ca21chr5
#   0       0.59534
#   1       0.64113
#   2       0.68693
#   3       0.68693
#   4       0.72828

import sys
import argparse

def parse_arguments():
    # Create the parent argument parser
    parser = argparse.ArgumentParser(
        description="Simple program to convert 'bedgraph' files to non-sparse 'wig' format.",
        epilog="example:\n  python3 bedgraph2wig.py input.bedgraph > output.wig",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Required arguments
    parser.add_argument('bedgraph', nargs='?', metavar='*.bedgraph',
        type=argparse.FileType('r'), default=sys.stdin,
        help="Path the the 'bedgraph' file to convert")
    
    # Optional arguments
    parser.add_argument('-o', '--output', metavar='*.wig',
        type=argparse.FileType('w'), default=sys.stdout,
        help="Send output to this file instead of STDOUT")
    
    return parser.parse_args()

def main():
    # Parse the arguments
    args = parse_arguments()
    
    print('track type=WIG', file=args.output)
    name = None
    pos = 0
    for line in args.bedgraph:
        sline = line.rstrip().split("\t")
        if (sline[0] != name):
            print('variableStep chrom='+sline[0], file=args.output)
            name = sline[0]
        start, end = int(sline[1]), int(sline[2])
        for i in range(pos, start):
            print(str(i)+"\t"+"0.00000", file=args.output)
        for i in range(start, end):
            print(str(i)+"\t"+sline[3], file=args.output)
        pos = end

if (__name__ == '__main__'):
    main()