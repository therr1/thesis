import pandas_plink
import vcf
import time
import pandas as pd
import numpy as np
import math
import time

class GenotypeMatrix2:
    def __init__(self, chrom):
        """
        positions is a list of positions of the variants.
        """
        self.chrom = chrom
        self.plink_path = '/broad/compbio/data/1KG_phase3/plink/chr' + str(chrom)
        self.bim, _, self.bed = pandas_plink.read_plink(self.plink_path)
        self.indexes = ['pos', 'a1', 'a0']
        self.bim_indexed = self.bim.set_index(self.indexes)

    def get_matrix(self, variants):
        mask = self.bim_indexed.index.isin(variants)
        matches = self.bim[mask][self.indexes]
        people = self.bim_indexed['i'][mask].to_numpy()
        rows = self.bed[people].compute()
        rows_fixed = 2 - rows
        return rows_fixed, matches



    def get_Rinverse(self, variants, var_cutoff = 0.99):
        matrix, matches = self.get_matrix(variants)
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
        return r_inv, matches

        





if __name__ == '__main__':
    gm = GenotypeMatrix2(3)
    locations = [(63664, 'T', 'G'),(63701, 'C', 'A')]
    #locations = None
    r_inv, indices = gm.get_Rinverse(locations)
    print(indices)
    print(r_inv)





# class DataThing:
#     def __init__(self, chrom):
#         filename = 'chr%d' % chrom
#         self.bim, _, self.bed = pandas_plink.read_plink(filename)
#         self.indexes = ['pos', 'a1', 'a0']
#         self.bim_indexed = self.bim.set_index(self.indexes)

#     def get_matrix(self, variants):
#         mask = self.bim_indexed.index.isin(variants)
#         matches = self.bim[mask][self.indexes]
#         people = self.bim_indexed['i'][mask].to_numpy()
#         rows = self.bed[people].compute()
#         rows_fixed = 2 - rows
#         return rows_fixed, matches

# dt = DataThing(1)
# variants = [ 
#     (11008, 'C', 'G'),
#     (11009, 'C', 'G'),
# ]
# result = dt.get_matrix(variants)
# print('result', result)
