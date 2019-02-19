. /broad/compbio/therr/software/miniconda3/etc/profile.d/conda.sh
conda activate thesis2
cd /broad/compbio/therr/thesis/src/code
modelname=$1
chrom=$SGE_TASK_ID
for filename in ../gwas_files/*.tsv; do
  python RegionTFMapper.py ${filename} ${modelname} ${chrom}
done
