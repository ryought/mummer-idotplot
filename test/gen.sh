for ref in ref_single.fasta ref_multi.fasta
do
  for query in single.fasta multi.fasta
  do
    echo $ref $query $ref.$query.mum
    # -F: required
    mummer -mum -F -c -b -l 2 $ref $query > $ref.$query.mum
    # mummer -maxmatch -F -b -c -l 2 $ref $query > $ref.$query.mum
  done
done
