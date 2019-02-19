import RegionTFToPhenotype


class GWASJob:
    def __init__(self, gwas_file, model_name, chrom, function="dot"):
        self.model_name = model_name
	self.chrom = chrom
	self.gwas_file = gwas_file

    def run(self):
        TFM = RegionTFToPhenotype(self.gwas_file, self.model_name, self.chrom)
        RTFM.create_save_file()


