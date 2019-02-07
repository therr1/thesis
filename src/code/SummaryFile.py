import csv
import vcf

class SummaryFile:
    def __init__(self, summary_file):
        self.summary_file = summary_file
        self.out_directory = 'snp_vcfs'


    def create_vcfs(self, outpath=None):

        with open(self.summary_file) as tsvin:
            tsvin = csv.reader(tsvin, delimiter='\t')
            vcf_reader = vcf.Reader(filename='../data/example.vcf')
            vcf_writers = {}
            for i in range(1,23):
                vcf_writers[i] = vcf.Writer(open('../data/' + self.out_directory + '/' + str(i) + '.vcf', 'w'), vcf_reader)
            vcf_writers['X'] = vcf.Writer(open('../data/' + self.out_directory + '/' + 'X' + '.vcf', 'w'), vcf_reader)
            vcf_writers['Y'] = vcf.Writer(open('../data/' + self.out_directory + '/' + 'Y' + '.vcf', 'w'), vcf_reader)
            vcf_writers['MT'] = vcf.Writer(open('../data/' + self.out_directory + '/' + 'MT' + '.vcf', 'w'), vcf_reader)

            header = next(tsvin)
            idd = 0
            for row in tsvin:
                variant = row[0]
                [chrom, position, ref, alt] = variant.split(':')
                if RepresentsInt(chrom):
                    chrom = int(chrom)
                vcf_writer = vcf_writers[chrom]
                alt = vcf.model._Substitution(alt)
                record = vcf.model._Record(chrom, int(position), idd, ref, [alt], None, None, None, None, 0)
                vcf_writer.write_record(record)
                idd += 1
                if idd%10000 == 0:
                    print(idd)

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


#sf = SummaryFile('../data/205442.gwas.imputed_v3.both_sexes.tsv')
#sf.create_vcf()

