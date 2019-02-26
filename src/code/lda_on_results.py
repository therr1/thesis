import gensim
from gensim.corpora import Dictionary
import os

class LDA_Model:
    def __init__(self,path,direction):
        """direction for words: 1 is tf, 2 is region, 3 is phenotype"""
        self.path = path
        self.direction = direction
        self.documents = {}


    def process_file(self, filepath):
        elements = filepath.split('/')
        data_index = elements.index("data")
        phenotype = elements[data_index + 2]
        tf = elements[-2]
        chrom = elements[-1].split('.')[0]
        with open(filepath) as f:
            counter = 0
            for line in f:
                elements = line.split(',')
                start = int(elements[0])
                end = int(elements[1])
                score = float(elements[2])
                if self.is_word(score):
                    final_tuple = (phenotype, tf, chrom, start, end, counter)
                    self.add_word(final_tuple)
                counter += 1

    def build_documents(self):
        if len(self.documents) != 0:
            return None
        else:
            #iterate through documents
            #self.process_file("/Users/therr/Documents/meng/research/thesis/src/data/output/20002_1286/DeepBind/Homo_sapiens/TF/D00303.002_SELEX_BARX1/1.csv")
            for subdir, dirs, files in os.walk(self.path):
                for filename in files:
                    self.process_file(os.path.join(subdir, filename))

    def perform_LDA(self, num_topics=5):
        print(self.documents)
        dct = Dictionary(self.documents.values()) 
        corpus = [dct.doc2bow(text) for text in self.documents.values()]
        lda = gensim.models.LdaModel(corpus, num_topics=num_topics, id2word=dct)

        for idx, topic in lda.print_topics(-1):
            print('Topic: {} Word: {}'.format(idx, topic))




    def add_word(self, final_tuple):
        phenotype = final_tuple[0]
        tf = final_tuple[1]
        chrom = final_tuple[2]
        start = final_tuple[3]
        end = final_tuple[4]
        counter = final_tuple[5]
        region = str(chrom) + '-' + str(counter)#str(start) + ":" + str(end)
        document = None
        word = None
        if self.direction == 1:
            document = (phenotype,region)
            word = tf
        if self.direction == 2:
            document = (region,tf)
            word = phenotype
        if self.direction == 3:
            document = (phenotype,tf)
            word = region

        if document in self.documents:
            self.documents[document].append(word)
        else:
            self.documents[document] = [word]





    def is_word(self, value):
        if abs(value) > 4:
            return True
        else:
            return False


if __name__ == '__main__':
    lm = LDA_Model("../data/output/",1)
    lm.build_documents()
    lm.perform_LDA()