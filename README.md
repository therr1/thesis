
# thesis

qsub -t 1-24 -l os=RedHat7 -l h_vmem=10G -P compbio_lab -e /broad/compbio/therr/error2.txt -o /broad/compbio/therr/output2.txt /broad/compbio/therr/thesis/src/code/runner_gwas.sh DeepBind/Homo_sapiens/TF/D00299.003_SELEX_ATF7/ 

https://broad.service-now.com/nav_to.do?uri=%2Fsp%3Fid%3Dkb_article%26sys_id%3D63354be4137f0b00449fb86f3244b049

python RegionTFMapper.py ../data/gwas_files/20002_1288.gwas.imputed_v3.both_sexes.tsv DeepBind/Homo_sapiens/TF/D00299.003_SELEX_ATF7/ 3

/home/unix/therr/opt/glibc-2.17/lib/ld-linux-x86-64.so.2 /broad/compbio/therr/software/miniconda3/envs/thesis2/bin/python tempname.py ../data/gwas_files/20544_2.gwas.imputed_v3.both_sexes.tsv D00299.003_SELEX_ATF7 3

use UGER
ish -l os=RedHat7 -l h_vmem=10G -l h_rt=24:00:00

export LD_LIBRARY_PATH=/home/unix/therr/opt/glibc-2.17/lib

qsub -l os=RedHat7 -t 1-23 -e /broad/compbio/therr/error.txt -o /broad/compbio/therr/output.txt /broad/compbio/therr/thesis/src/code/runner.sh D00290.003_SELEX_ALX3

qsub -t 1-24 ./runner.sh D00290.003_SELEX_ALX3

python tempname.py ../data/gwas_files/20544_2.gwas.imputed_v3.both_sexes.tsv D00299.003_SELEX_ATF7 3
