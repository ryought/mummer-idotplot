# mummer-idotplot
Generate interactive dotplot from mummer4 output using plotly

## Installation
```
$ pip install mummer-idotplot
```
`plotly` is required to install.

## Usage

When aligning two sequences with MUMmer4, you should set an option `-F`(force 4 column output format). Also, you should not use `-c` option, which change output position of match starting position.

So for example:
If you have `chr1, chr2` in `reference.fasta`, and `contig1, contig2` in `query.fasta`
```
$ mummer -maxmatch -F -b -l 10 reference.fasta query.fasta > output.mum
$ mummer-idotplot output.mum output.html --ref chr1 chr2 --query contig1 contig2
$ open output.html
```

