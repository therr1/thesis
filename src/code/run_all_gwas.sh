cat ../data/tfs.txt | while read line
do
  qsub -l h_vmem=10G -l os=RedHat7 -P compbio_lab -t 1 /broad/compbio/therr/thesis/src/code/runner_gwas.sh $line
done
