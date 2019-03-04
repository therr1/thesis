. /broad/compbio/therr/software/miniconda3/etc/profile.d/conda.sh
conda activate thesis2
cd /broad/compbio/therr/thesis/src/code
modelname=$1
chrom=$SGE_TASK_ID
#chrom=$2
for filename in ../data/gwas_files/*.tsv; do
  python RegionTFMapper.py ${filename} ${modelname} ${chrom}
done
