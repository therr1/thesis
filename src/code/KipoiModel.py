import kipoi
import kipoi_veff
from kipoi_veff import VcfWriter
import kipoi_veff.snv_predict as sp
from kipoi_veff.scores import Diff, DeepSEA_effect
from kipoi_veff.parsers import KipoiVCFParser
import pandas as pd
import os

class KipoiModel:
    def __init__(self, model_name, snp_vcf_path='../data/snp_vcfs'):
        self.model_name = model_name
        self.model_path = 'DeepBind/Homo_sapiens/TF/' + model_name
        self.model = kipoi.get_model(self.model_path)
        self.snp_vcf_path = snp_vcf_path

    def add_scores_single_chrom(self, chrom, out_dir=None):
        if out_dir is None:
            out_dir = '../data/model_scores/' + self.model_name
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        
        Dataloader = self.model.default_dataloader
        vcf_path = self.snp_vcf_path + '/' + chrom + '.vcf'
        out_vcf_fpath = out_dir + '/' + chrom + '.vcf'
        print(vcf_path)
        print(out_vcf_fpath)
        writer = VcfWriter(self.model, vcf_path, out_vcf_fpath)
        model_info = kipoi_veff.ModelInfoExtractor(self.model, Dataloader)
        # vcf_to_region will generate a variant-centered regions when presented a VCF record.
        vcf_to_region = kipoi_veff.SnvCenteredRg(model_info)

        dataloader_arguments = {"fasta_file": '../data/fasta_files/chr' + chrom + '.fa'}

        sp.predict_snvs(self.model,
                        Dataloader,
                        vcf_path,
                        batch_size = 32,
                        dataloader_args=dataloader_arguments,
                        vcf_to_region=vcf_to_region,
                        #evaluation_function_kwargs={'diff_types': {'diff': Diff("mean"), 'deepsea_effect': DeepSEA_effect("mean")}},
                        sync_pred_writer=writer)



    def add_scores(self, snp_vcf_path='../data/snp_vcfs', out_dir=None):
        if out_dir is None:
            out_dir = '../data/model_scores/' + self.model_name
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        file_names = os.listdir(self.snp_vcf_path)
        for file_name in file_names:
            chrom = file_name.split('.')[0]
            Dataloader = self.model.default_dataloader
            vcf_path = self.snp_vcf_path + '/' + file_name
            out_vcf_fpath = out_dir + '/' + chrom + '.vcf'
            print(vcf_path)
            print(out_vcf_fpath)
            writer = VcfWriter(self.model, vcf_path, out_vcf_fpath)
            model_info = kipoi_veff.ModelInfoExtractor(self.model, Dataloader)
            # vcf_to_region will generate a variant-centered regions when presented a VCF record.
            vcf_to_region = kipoi_veff.SnvCenteredRg(model_info)

            dataloader_arguments = {"fasta_file": '../data/fasta_files/chr' + chrom + '.fa'}

            sp.predict_snvs(self.model,
                            Dataloader,
                            vcf_path,
                            batch_size = 32,
                            dataloader_args=dataloader_arguments,
                            vcf_to_region=vcf_to_region,
                            #evaluation_function_kwargs={'diff_types': {'diff': Diff("mean"), 'deepsea_effect': DeepSEA_effect("mean")}},
                            sync_pred_writer=writer)








