import gensim
from gensim.corpora import Dictionary
import os
import pandas as pd

class TensorAnalyzer:
    def __init__(self,path):
        """direction for words: 1 is tf, 2 is region, 3 is phenotype"""
        self.path = path
        self.phenotypes = {} # dict of phenotypes, transcription factors
        self.dataframe = None

    def process_file(self, filepath):
        elements = filepath.split('/')
        data_index = elements.index("data")
        phenotype = elements[data_index + 2]
        tf = elements[-2]
        chrom = elements[-1].split('.')[0]
        with open(filepath) as f:
            counter = 0
            final_elements = {}
            for line in f:
                elements = line.split(',')
                start = int(elements[0])
                end = int(elements[1])
                score = float(elements[2])
                # if self.is_word(score):
                #     final_tuple = (phenotype, tf, chrom, start, end, counter)
                #     self.add_word(final_tuple)
                label = str(chrom) + '-' + str(counter)
                final_elements[label] = score
                counter += 1

        if phenotype in self.phenotypes:
            tfs = self.phenotypes[phenotype]
            tfs[tf] = final_elements
        else:
            self.phenotypes[phenotype] = {tf: final_elements}

    def build_dataframe(self):
        if len(self.phenotypes) != 0:
            return None
        else:
            counter = 0
            #iterate through documents
            #self.process_file("/Users/therr/Documents/meng/research/thesis/src/data/output/20002_1286/DeepBind/Homo_sapiens/TF/D00303.002_SELEX_BARX1/1.csv")
            for subdir, dirs, files in os.walk(self.path):
                for filename in files:
                    counter += 1
                    self.process_file(os.path.join(subdir, filename))
                    if (counter % 100) == 0:
                        print(counter)
        self.dataframe = pd.concat({k: pd.DataFrame(v) for k, v in self.phenotypes.items()})
        self.dataframe.to_pickle('../data/tensor.pkl')




if __name__ == '__main__':
    ta = TensorAnalyzer("../data/output/")
    ta.build_dataframe()
    print(ta.dataframe)
    #lm.perform_LDA()
