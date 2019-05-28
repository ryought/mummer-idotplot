#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import argparse

def main():
    parser = argparse.ArgumentParser(description='mummer-idotplot: MUMmer4 Interactive Dotplot Generator')
    parser.add_argument('mum_filename', type=str, help='MUMmer4 output filename. It must be generated from MUMmer4 with -L -F option and without -c option.')
    parser.add_argument('output_filename', type=str, help='output HTML filename. The filename must be ended with ".html".')
    parser.add_argument('--refs', required=True, nargs='+', help='space-delimited list of sequence ids of reference(fasta) to show in plot. To show specific region of the sequence, you can write <sequence id>:<start position (bp)>:<end position (bp)>.')
    parser.add_argument('--querys', required=True, nargs='+', help='space-delimited list of sequence ids of query(fasta) to show in plot. To show specific region of the sequence, you can write <sequence id>:<start position (bp)>:<end position (bp)>.')
    args = parser.parse_args()

    refs = []
    querys = []

    pat = re.compile(r'^(.+):([0-9]+):([0-9]+)$')

    for r in args.refs:
        match = pat.match(r)
        if match:
            refs.append((match.group(1), int(match.group(2)), int(match.group(3))))
        else:
            refs.append((r, None, None))

    for r in args.querys:
        match = pat.match(r)
        if match:
            querys.append((match.group(1), int(match.group(2)), int(match.group(3))))
        else:
            querys.append((r, None, None))


    from .mummer_interactive_dotplot import parse_mums, draw_map_plotly_multi
    mum, single_ref = parse_mums(args.mum_filename)
    draw_map_plotly_multi(
            mum,
            refs=refs,
            querys=querys,
            single_ref=single_ref,
            html=args.output_filename)

if __name__ == '__main__':
    main()
