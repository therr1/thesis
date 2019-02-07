import kipoi
import kipoi_veff
from kipoi_veff import VcfWriter
import kipoi_veff.snv_predict as sp
from kipoi_veff.scores import Diff, DeepSEA_effect
from kipoi_veff.parsers import KipoiVCFParser
import pandas as pd


model_name = "DeepBind/Homo_sapiens/TF/D00299.003_SELEX_ATF7"
# get the model
model = kipoi.get_model(model_name)
# get the dataloader factory
Dataloader = model.default_dataloader

vcf_path = "../data/test.vcf"
# The output vcf path, based on the input file name    
out_vcf_fpath = vcf_path[:-4] + "%s.vcf"%model_name.replace("/", "_")
# The writer object that will output the annotated VCF
writer = VcfWriter(model, vcf_path, out_vcf_fpath)

# Information extraction from dataloader and model
model_info = kipoi_veff.ModelInfoExtractor(model, Dataloader)
# vcf_to_region will generate a variant-centered regions when presented a VCF record.
vcf_to_region = kipoi_veff.SnvCenteredRg(model_info)

dataloader_arguments = {"fasta_file": "../data/fasta_files/chr1.fa"}

sp.predict_snvs(model,
                Dataloader,
                vcf_path,
                batch_size = 32,
                dataloader_args=dataloader_arguments,
                vcf_to_region=vcf_to_region,
                #evaluation_function_kwargs={'diff_types': {'diff': Diff("mean"), 'deepsea_effect': DeepSEA_effect("mean")}},
                sync_pred_writer=writer)
vcf_reader = KipoiVCFParser(out_vcf_fpath)
entries = [el for el in vcf_reader]
#print(pd.DataFrame(entries).head().iloc[:,:7])



