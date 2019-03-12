from keras.layers import Input, Dense, Lambda
from keras.models import Model
from keras.datasets import mnist
from keras.losses import mse, binary_crossentropy
import numpy as np
from VaeLoader import VaeLoader
from keras import backend as K
import csv




class Autoencoder:
    def __init__(self, dataloader, encoding_dim=32, encoder_type="var"):
        self.encoding_dim = encoding_dim
        self.dataloader = dataloader
        self.input_dim = self.dataloader.get_dim()
        self.training_data = self.dataloader.get_training_data()
        self.batch_size = 256
        self.autoencoder = None
        print(self.training_data)
        self.encoder_type = encoder_type
        if encoder_type == "var":
            self.create_var_encoder()
        else: 
            self.create_encoder()
        self.is_trained = False


    def create_encoder(self):

        input_img = Input(shape=(self.input_dim,))
        encoded = Dense(self.encoding_dim, activation='relu')(input_img)
        decoded = Dense(self.input_dim, activation='sigmoid')(encoded)
        self.autoencoder = Model(input_img, decoded)
        self.encoder = Model(input_img, encoded)

        # create a placeholder for an encoded (32-dimensional) input
        encoded_input = Input(shape=(self.encoding_dim,))
        # retrieve the last layer of the autoencoder model
        decoder_layer = self.autoencoder.layers[-1]
        # create the decoder model
        self.decoder = Model(encoded_input, decoder_layer(encoded_input))

        self.autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')


    def create_var_encoder(self):
        print("YO")
        intermediate_dim = 64
        inputs = Input(batch_shape=(self.batch_size, self.input_dim))
        x = Dense(intermediate_dim, activation='relu')(inputs)
        z_mean = Dense(self.encoding_dim)(x)
        z_log_var = Dense(self.encoding_dim)(x)
        z = Lambda(sampling, output_shape=(self.encoding_dim,), name='z')([z_mean, z_log_var])
        self.encoder = Model(inputs, [z_mean, z_log_var, z], name='encoder')


        latent_inputs = Input(shape=(self.encoding_dim,), name='z_sampling')
        x = Dense(intermediate_dim, activation='relu')(latent_inputs)
        outputs = Dense(self.input_dim, activation='sigmoid')(x)
        self.decoder = Model(latent_inputs, outputs, name='decoder')

        outputs = self.decoder(self.encoder(inputs)[2])
        self.autoencoder = Model(inputs, outputs, name='vae_mlp')

        reconstruction_loss = binary_crossentropy(inputs,outputs)
        reconstruction_loss *= self.input_dim
        kl_loss = 1 + z_log_var - K.square(z_mean) - K.exp(z_log_var)
        kl_loss = K.sum(kl_loss, axis=-1)
        kl_loss *= -0.5
        vae_loss = K.mean(reconstruction_loss + kl_loss)
        self.autoencoder.add_loss(vae_loss)
        self.autoencoder.compile(optimizer='adam')



    def train_encoder(self, epochs=100):
        self.autoencoder.fit(self.training_data,
                epochs=epochs,
                batch_size=256,
                shuffle=True)
        self.is_trained = True

    def get_encodings(self, epochs=100):
        if not self.is_trained:
            self.train_encoder(epochs=epochs)
        predictions = self.encoder.predict(self.training_data)
        return predictions[2]

    def save_encodings(self, outpath='../data/vae_results.csv', epochs=100):
        result_file = open(outpath,'w')
        wr = csv.writer(result_file)

        labels = self.dataloader.get_labels()
        predictions = self.get_encodings(epochs=epochs)
        print(len(labels))
        print(len(predictions))
        for ix, prediction in enumerate(predictions):
            final_line = []
            prediction = list(prediction)
            label = labels[ix]
            final_line.append(label)
            final_line.extend(prediction)
            wr.writerow(final_line)



def sampling(args):
    """Reparameterization trick by sampling from an isotropic unit Gaussian.
    # Arguments
        args (tensor): mean and log of variance of Q(z|X)
    # Returns
        z (tensor): sampled latent vector
    """
    z_mean, z_log_var = args
    batch = K.shape(z_mean)[0]
    dim = K.int_shape(z_mean)[1]
    # by default, random_normal has mean = 0 and std = 1.0
    epsilon = K.random_normal(shape=(batch, dim))
    return z_mean + K.exp(0.5 * z_log_var) * epsilon


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
    dl = VaeLoader("../data/model_scores", limit=10000, chrom=3)
    x_training_data = dl.get_training_data()
    autoe = Autoencoder(dl)
    # autoe.create_encoder()
    autoe.save_encodings(epochs=100)

