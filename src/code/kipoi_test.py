import kipoi
model = kipoi.get_model('DeepBind/Homo_sapiens/TF/D00311.003_SELEX_BHLHE23')

pred = model.pipeline.predict_example()

# Download example dataloader kwargs
dl_kwargs = {'intervals_file': 'example/intervals_file', 'fasta_file': 'example/fasta_file'}

# Get the dataloader and instantiate it
dl = model.default_dataloader(**dl_kwargs)
# get a batch iterator
it = dl.batch_iter(batch_size=4)
# predict for a batch
while(True):
    batch = next(it)
    print(model.predict_on_batch(batch['inputs']))

#print(model.predict_on_batch(dl['inputs']))