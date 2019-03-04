from kipoi_veff.parsers import KipoiVCFParser
#import matplotlib.pyplot as plt
import numpy as np
import math
import csv
import pandas as pd
import os
from CombinerFunctions import *
import time
import sys

class RegionTFToPhenotype:
    def __init__(self, gwas_file, model_name, chrom, function="dot", num_regions=100):
        self.model_name = model_name
        self.chrom = chrom
        self.gwas_file = gwas_file
        self.chrom_file = "../data/model_scores/" + model_name + "/" + chrom + ".vcf"
        self.gwas_file_number = gwas_file.split('/')[-1].split('.')[0]
        self.function = function
        #self.process_gwas_df()
        self.gwas_df = None
        self.num_regions = num_regions



    def process_gwas_df(self):
        self.gwas_df = pd.read_csv(self.gwas_file, sep='\t')
        new = self.gwas_df["variant"].str.split(":", expand=True) 
        self.gwas_df["chromosome"] = new[0]
        self.gwas_df["location"] = new[1]
        self.gwas_df["ref"] = new[2]
        self.gwas_df["alt"] = new[3]


    def z_score_hist(self):
        if self.gwas_df == None:
            self.process_gwas_df()
        tstats = np.array(self.gwas_df['tstat'])
#        plt.hist(tstats,bins=200)
#        plt.title('Histogram of TStats for GWAS Summary Statistics')
#        plt.xlabel('TStat')
#        plt.show()


    def create_pval_dictionary(self):
        if self.gwas_df == None:
            self.process_gwas_df()
        filtered = self.gwas_df[self.gwas_df['chromosome'] == self.chrom]
        final_dictionary = dict(zip(filtered['location'], filtered['tstat']))
        return final_dictionary


    def create_score_array(self):
        """
        returns an array with the following values
        [[min, max, score]]
        """
        if self.gwas_df == None:
            self.process_gwas_df()

        vcf_reader = KipoiVCFParser(self.chrom_file)
        all_elements = [el for el in vcf_reader]
        vcf_df = pd.DataFrame(all_elements)

        subset_gwas = self.gwas_df[['location','tstat','pval']]
        subset_gwas['location'] = pd.to_numeric(subset_gwas['location'])

        vcf_df['variant_pos'] = pd.to_numeric(vcf_df['variant_pos'])

        merged_df = pd.merge(vcf_df, subset_gwas, how='inner', left_on=['variant_pos'], right_on=['location'])
        merged_df = merged_df.dropna()
        min_val = min(merged_df['variant_pos'])
        max_val = max(merged_df['variant_pos'])
        print(merged_df.shape)

        number_of_bases = (max_val - min_val)


        final_values = []
        for i in range(self.num_regions):
            range_min = min_val + int(number_of_bases * i /float(self.num_regions))
            range_max = min_val + int(number_of_bases * (i + 1) /float(self.num_regions))
            temp_df = merged_df[merged_df['location'].between(range_min, range_max)]


            kipoi_scores = np.array(temp_df[temp_df.columns[5]])
            t_stats = np.array(temp_df['tstat'])

            combiner = FunctionGetter.get_function(self.function)

            # print(t_stats)
            # time.sleep(100)
            score = combiner(t_stats,kipoi_scores)
            final_values.append([range_min, range_max, score])

        return final_values





    def create_save_file(self, file_name=None, remake=False):
        if file_name == None:
            dir_name = '../data/output/' + self.gwas_file_number + '/' + self.model_name
        # print(self.gwas_file_number)
        # print(self.model_name)
        if not os.path.isdir(dir_name): 
            os.makedirs(dir_name)

        file_name = dir_name + '/' + self.chrom + ".csv"
        if os.path.isfile(file_name) and not remake:
            print("file already exists")
            return None
        score_array = self.create_score_array()
        with open(file_name, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(score_array)

        # vcf_reader = KipoiVCFParser(self.chrom_file)
        # all_scores = []
        # count = 0
        # for el in vcf_reader:
        #     score = list(el.items())[-2][1]
        #     if math.isnan(score):
        #         pass
        #     elif not score == float('inf'):
        #         all_scores.append(score)
        #     count += 1
        #     if count%10000 == 0:
        #         print(count)

        # plt.hist(all_scores,bins=100)
        # plt.title('Distribution of Logit Scores for TF SELEX_ATF7')
        # plt.xlabel('Logit Score')
        # plt.show()


if __name__ == '__main__':
    gwas_file = sys.argv[1]
    model = sys.argv[2]
    chrom = sys.argv[3]
    rtp  = RegionTFToPhenotype(gwas_file, model, chrom)
    rtp.create_save_file()
    #RTP = RegionTFToPhenotype('../data/gwas_files/20544_2.gwas.imputed_v3.both_sexes.tsv', 'D00299.003_SELEX_ATF7', '3')
    #RTP.create_vectors()
#RTP.z_score_hist()
#print(RTP.create_pval_dictionary())
#RTP.create_vector()

