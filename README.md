# mummer-interactive-dotplot

## Installation
```
$ pip install mummer-idotplot
```
requirement: plotly

## Usage

```
mapping
$ mummer -mum -b -c -l 1000 reference.fasta query.fasta
visualizing
$ mummer-idotplot mummeroutput.mum output.html --ref chr1 chr2 --query contig5 contig9
```

where `chr1, chr2` is in `reference.fasta`, and `contig5, contig9` is in `query.fasta`


