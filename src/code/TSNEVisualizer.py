import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

class TSNEVisualizer:
    def __init__(self, data_file):
        all_data = []
        self.labels = []
        counter = 0
        with open(data_file) as f:
            for line in f:
                counter += 1
                if counter == 10000:
                    break
                elements = line.split(',')
                values = elements[1:]
                values = [float(value) for value in values]
                label = elements[0]
                self.labels.append(label)
                all_data.append(values)

        self.data = np.array(all_data)

    def perform_tsne(self):
        embedded = TSNE(n_components=2,verbose=1).fit_transform(self.data)
        print(embedded.shape)
        plt.scatter(embedded[:,0], embedded[:,1], s=3)
        plt.show()









if __name__ == '__main__':
    tv = TSNEVisualizer('../data/vae_results.csv')
    tv.perform_tsne()