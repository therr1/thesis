from keras.layers import Input, Dense
from keras.models import Model
from keras.datasets import mnist
import numpy as np
from VaeLoader import VaeLoader


class Autoencoder:
    def __init__(self, dataloader, encoding_dim=32):
        self.encoding_dim = encoding_dim
        self.dataloader = dataloader
        self.input_dim = self.dataloader.get_dim()
        self.training_data = self.dataloader.get_training_data()
        print(self.training_data)

    def create_encoder(self):
        input_img = Input(shape=(self.input_dim,))
        encoded = Dense(self.encoding_dim, activation='relu')(input_img)
        decoded = Dense(self.input_dim, activation='sigmoid')(encoded)
        autoencoder = Model(input_img, decoded)
        encoder = Model(input_img, encoded)

        # create a placeholder for an encoded (32-dimensional) input
        encoded_input = Input(shape=(self.encoding_dim,))
        # retrieve the last layer of the autoencoder model
        decoder_layer = autoencoder.layers[-1]
        # create the decoder model
        decoder = Model(encoded_input, decoder_layer(encoded_input))

        autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

        autoencoder.fit(self.training_data, self.training_data,
                epochs=50,
                batch_size=256,
                shuffle=True)


# class Dataloader:
#     def __init__(self):
#         pass

#     def get_dim(self):
#         return 768

#     def get_training_data(self):
#         (x_train, _), (x_test, _) = mnist.load_data()
#         x_train = x_train.astype('float32') / 255.
#         x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
#         print(x_train[0])
#         return x_train

if __name__ == '__main__':
    dl = VaeLoader("../data/model_scores")
    x_training_data = dl.get_training_data()
    autoe = Autoencoder(dl)
    autoe.create_encoder()




