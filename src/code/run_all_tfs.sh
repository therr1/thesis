cat ../data/tfs.txt | while read line
do
  qsub -l os=RedHat7 -t 1-23 -e /broad/compbio/therr/error.txt -o /broad/compbio/therr/output.txt /broad/compbio/therr/thesis/src/code/runner.sh $line
done
