import vcf
import time
import pandas as pd
import numpy as np
import math

class GenotypeMatrix:
    def __init__(self, chrom, start, end):
        """
        positions is a list of positions of the variants.
        """
        self.chrom = chrom

        self.start = start
        self.end = end

        self.vcf_file = '../data/1kg/chr' + str(chrom) + '.vcf.gz'
        self.dataframe = None

    def get_dataframe(self):
        all_variants = {}

        reader = vcf.Reader(filename=self.vcf_file, compressed=True)
        entries = reader.fetch(3,self.start,self.end)
        for entry in entries:
            position = entry.POS
            reference = entry.alleles[0]
            alternate = str(entry.alleles[1])
            samples = entry.samples
            inner_dict = {}
            for call in samples:
                inner_dict[call.sample] = call.gt_type


            
            all_variants[(position,reference,alternate)] = inner_dict

        final_dataframe = pd.DataFrame.from_dict(all_variants, orient='index')
        print(final_dataframe)
        final_dataframe.fillna(0)
        self.dataframe = final_dataframe

    def get_Rinverse(self, locations=None, var_cutoff = 0.99):
        if self.dataframe == None:
            self.get_dataframe()
        matrix = None
        indices = np.array(self.dataframe.index)
        print(locations)
        if locations is None:
            matrix = self.dataframe.values
        else:

            filtered = self.dataframe[self.dataframe.index.isin(locations)]
            matrix = filtered.values
            indices = np.array(filtered.index)
        num_individuals = matrix.shape[1]

        matrix = matrix.transpose()
        matrix = matrix/math.sqrt(num_individuals)
        u,s,vh = np.linalg.svd(matrix)
        variances= s*s
        total_variance = sum(variances)
        target = var_cutoff*total_variance

        var_sum = 0
        index = 0
        for variance in variances:
            if var_sum < target:
                var_sum += variance
                index += 1
            else:
                break

        
        s_inv_squared = s ** -2
        s_inv_squared[index:] = 0
        r_inv = (vh.transpose()).dot(np.diag(s_inv_squared)).dot(vh)
        return r_inv, indices

        





if __name__ == '__main__':
    gm = GenotypeMatrix(3, 50000,65000)
    locations = [(63664, 'T', 'G'),(63701, 'C', 'A')]
    #locations = None
    r_inv, indices = gm.get_Rinverse(locations=locations)
    print(indices)
    print(r_inv)



