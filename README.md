# mummer-idotplot
Generate interactive dotplot from MUMmer4 output using plotly

[![Downloads](https://pepy.tech/badge/mummer-idotplot)](https://pepy.tech/project/mummer-idotplot)

## Installation
```
$ pip install mummer-idotplot
```
`plotly` is required to install.

## Usage

When aligning two sequences with MUMmer4, you should set an option `-F`(force 4 column output format) and `-L`(show length of query). Also, you should not use `-c` option, which change output position of match starting position and have bugs.

So for example:
If you have `chr1, chr2` in `reference.fasta`, and `contig1, contig2` in `query.fasta`
```
$ mummer -maxmatch -F -L -b -l 10 reference.fasta query.fasta > output.mum
$ mummer-idotplot output.mum output.html --ref chr1 chr2 --query contig1 contig2
$ mummer-idotplot output.mum output.html --ref chr1:0:50000 chr2:100:20000 --query contig1 contig2  # you can specify the region to plot
$ open output.html  # you'll see dotplot in your browser
```

