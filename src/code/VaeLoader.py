import os
import time
from kipoi_veff.parsers import KipoiVCFParser
import numpy as np
import time
import math


class VaeLoader:
    def __init__(self, path, chrom=None, limit=10000):
        self.path = path
        self.model_names = set()
        self.snps = {}
        self.chrom = chrom
        self.limit = limit

    def build_snps(self):
        if len(self.snps) != 0:
            return None
        else:
            process_count=0
            #iterate through files
            #self.process_file("/Users/therr/Documents/meng/research/thesis/src/data/output/20002_1286/DeepBind/Homo_sapiens/TF/D00303.002_SELEX_BARX1/1.csv")
            for subdir, dirs, files in os.walk(self.path):
                for filename in files:
                    if self.chrom == None or str(self.chrom) == filename.split('.')[0]:    
                        self.process_file(os.path.join(subdir, filename))
                        process_count+=1
                if process_count >= self.limit:
                    return None

    def process_file(self, filename):
        model_name = filename.split('/')[-2]
        self.model_names.add(model_name)
        vcf_reader = KipoiVCFParser(filename)
        for el in vcf_reader:
            chrom = el['variant_chr']
            position = el['variant_pos']
            score = list(el.values())[5]
            snp_name = str(chrom) + '-' + str(position)
            if snp_name not in self.snps:
                self.snps[snp_name] = {}
            self.snps[snp_name][model_name] = score

    def get_training_data(self):
        if len(self.snps) == 0:
            self.build_snps()
        all_vectors = []
        model_names_list = list(self.model_names)
        print(model_names_list)
        for snp in self.snps:
            vector = []
            values = self.snps[snp]
            for model_name in model_names_list:
                
                if model_name in values:
                    value = values[model_name]
                    if math.isnan(value):
                        vector.append(0)
                    else:
                        vector.append(value)
                else:
                    vector.append(0)
            all_vectors.append(vector)
        return np.array(all_vectors)


    def get_dim(self):
        if len(self.snps) == 0:
            self.build_snps()
        return len(self.model_names)





if __name__ == '__main__':
    vae = VaeLoader("blah")
    vae.process_file("../data/model_scores/DeepBind/Homo_sapiens/TF/D00299.003_SELEX_ATF7/3.vcf")






