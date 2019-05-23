#!/usr/bin/env python
# -*- coding: utf-8 -*-

def main():
    import argparse
    parser = argparse.ArgumentParser(description='mummer-idotplot: MUMmer4 Interactive Dotplot Generator')
    parser.add_argument('mum_filename', type=str, help='mummer4 output filename')
    parser.add_argument('output_filename', type=str, help='output html filename')
    parser.add_argument('--refs', required=True, nargs='+', help='list of sequence ids of reference(fasta) to show in plot')
    parser.add_argument('--querys', required=True, nargs='+', help='list of sequence ids of query(fasta) to show in plot')
    args = parser.parse_args()

    from .mummer_interactive_dotplot import parse_mums, draw_map_plotly_multi
    mum, single_ref = parse_mums(args.mum_filename)
    draw_map_plotly_multi(
            mum,
            refs=args.refs,
            querys=args.querys,
            single_ref=single_ref,
            html=args.output_filename)

if __name__ == '__main__':
    main()
