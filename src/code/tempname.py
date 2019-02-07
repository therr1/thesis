import sys
import os
from RegionTFMapper import RegionTFToPhenotype
from KipoiModel import *
class ClusterJob:
    def __init__(self, gwas_file, model_name, chrom, model_base_dir='DeepBind/Homo_sapiens/TF'):
        self.gwas_file = gwas_file
        self.model_name = model_name
        self.model_path = model_base_dir + '/' + model_name
        self.chrom = chrom


    def run(self, cache_scores=True):
        phenotype_file_name = self.gwas_file.split('/')[-1]
        phenotype_number = phenotype_file_name.split('.')[0]
        out_dir='../data/output/' + phenotype_number + '/' + self.model_name
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)


        tf_chrom_file = "../data/model_scores/" + model_name + '/' + chrom + '.vcf'
        create_file = True
        if cache_scores:
            if os.path.isfile(tf_chrom_file):
                create_file = False
                print("Didn't Create File")
        if create_file:
            km = KipoiModel(self.model_name)
            km.add_scores_single_chrom(chrom) # creates the vcf file

        tf_chrom_file = "../data/model_scores/" + model_name + '/' + chrom + '.vcf'

        RTFM = RegionTFToPhenotype(self.gwas_file, self.model_name, self.chrom)
        RTFM.create_save_file()




if __name__ == '__main__':

    gwas_tsv = sys.argv[1]
    model_name = sys.argv[2]
    chrom = sys.argv[3]
    CJ = ClusterJob(gwas_tsv, model_name, chrom)
    CJ.run()