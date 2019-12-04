'''anchors_generator.py

This python file runs to read in fasta file of V genes or J genes in T-cell
or B-cell to translate DNA genes to amino acids and then finding the index of
the last occurrence of cysteine in the V genes or the first occurence of
phenylalanine followed by glycine in J genes.
'''
import argparse
import sys
from Bio import SeqIO
import csv
import math
import re
import xlwt
import os

def main(args):

    # Read in command line arguments to variables
    input_dir = args.i
    output_dir = args.o

    if output_dir[-1] is not "/":
        output_dir += "/"

    try:
        os.makedirs(output_dir)
    except:
        pass

    #run with python excelScript.py
    book = xlwt.Workbook()

    for filename in sorted(os.listdir(input_dir), key=lambda x: x.split('.')[0][-1]):
        infile = os.path.join(input_dir, filename)
        filename = filename.split('.')[-2]
        sheet = book.add_sheet(filename)
        output_filename = f"{output_dir}{filename}"

        #if 'J-REGION' in [a for a in open(infile)][0]:
        first_line = [a for a in open(infile)][0]
        if re.split(string=first_line, pattern=r"[0-9\-]+\*")[0][-1] == 'J':
            v_or_j = 'J'
        elif re.split(string=first_line, pattern=r"[0-9\-]+\*")[0][-1] == 'V':
            v_or_j = 'V'
        else:
            v_or_j = args.t.upper()

        if v_or_j == "V" :
            output_data = parse_v_genes(infile)
            write_excel_sheet_v(sheet, output_data)
        else:
            output_data = parse_j_genes(infile)
            write_excel_sheet_j(sheet, output_data)

    excel_file_name = output_dir + "contributions.xls"
    book.save(excel_file_name)



def parse_j_genes(infile):
    '''Find the anchors in a j genes file

    Attributes
    ----------
        infile (str): full path to input file
    '''

    # dictionary to store resulting data
    data = {'results': [],
            'indexs' : [],
            'error_results' :[],
            'error_indexs' : [],
            'sequence' : [],
            'extras' : [],
            'amino_acids' : [],
            'gene_names' : [],
            'accessions' : [],
            'functionalitys' : [],
            'partials' : [],
            'genes' : [],
            'alleles' : []
            }

    for seq_record in SeqIO.parse(infile, "fasta"):
        ind = []
        extra_indexs = []
        three_amino_acids = []
        reading_frams = []

        # try out 3 different frames
        for i in range(3):

            # split record to match triplets
            seq_record_temp = seq_record.seq[i:]
            floor = math.floor(len(seq_record_temp)/3)
            index = len(seq_record_temp) - (floor*3)
            if index != 0:
                seq_record_temp = seq_record_temp[:-(index)]

            # translating from dna to amino acid and find first (F/W)X(S/T)
            translated_seq = seq_record_temp.translate()
            three_amino_acids.append (translated_seq)
            position = -1
            m = re.search('[FW]G.?G[ST]', str(translated_seq))
            if m:
                position = m.start()
            index_F = ((position*3)+i)
            ind.append(index_F)
            reading_frams.append(i)

        #get the gene name
        if "|" not in seq_record.description:
            gene_name = seq_record.description
            accession = ""
            functionality = ""
            partial = ""
        else:
            splitted = seq_record.description.split('|')
            gene_name = splitted[1]
            accession = splitted[0]
            functionality = splitted[3]
            partial = splitted[13]

        splitted_gene_name = gene_name.split('*')
        gene = splitted_gene_name[0]
        allele = splitted_gene_name[1][0:2]

        # look for only positive indexs
        pos_idx = [i for i in ind if i >=0]

        if len(pos_idx) != 0:
            pos_idx = min(pos_idx)

            #get the reading frame
            reading_frame_index = ind.index(pos_idx)
            reading_frame = reading_frame_index + 1

            #get the amino_acids with the correct reading frame
            amino_acid = three_amino_acids[reading_frame-1]

            # get the amino acids from the beginning to the first F
            amino_acid_index = int((pos_idx-reading_frame+1)/3)+1
            amino_acid = amino_acid[0:amino_acid_index]

            pos_idx = str(pos_idx)

            data['indexs'].append(pos_idx)
            data['results'].append(seq_record.description)

            # get the extras
            extra = seq_record.seq[0:reading_frame-1]
            data['extras'].append(extra)
            data['amino_acids'].append(amino_acid)
            data['genes'].append(gene)
            data['alleles'].append(allele)
            data['gene_names'].append(gene_name)
            data['accessions'].append(accession)
            data['functionalitys'].append(functionality)
            data['partials'].append(partial)

        else:
            data['error_indexs'].append(str(0))
            data['error_results'].append(seq_record.description)
            data['sequence'].append(seq_record.seq)

    return data


def parse_v_genes(infile):
    '''Find the anchors in a v genes file

    Attributes
    ----------
        infile (str): full path to input file
    '''

    # dictionary to store resulting data
    data = {'results': [],
            'indexs' : [],
            'error_results' :[],
            'error_indexs' : [],
            'sequence' : [],
            'extras' : [],
            'amino_acids' : [],
            'gene_names' : [],
            'accessions' : [],
            'functionalitys' : [],
            'partials' : [],
            'genes' : [],
            'alleles' : []
            }

    for seq_record in SeqIO.parse(infile, "fasta"):
        floor = math.floor(len(seq_record.seq)/3)
        index = len(seq_record.seq) - (floor*3)
        if index != 0:
            extra = seq_record.seq[-(index):]
            seq_record.seq = seq_record.seq[:-(index)]
        #find the index of last C
        anchor_index = str(seq_record.seq.translate().rfind('C')*3)

        #get the amino acids starting from the last C
        translated = seq_record.seq.translate()
        reverse_index_C = len(translated)-translated.rfind('C')
        amino_acid = translated[-(reverse_index_C):]

        #get the gene name
        if "|" not in seq_record.description:
            gene_name = seq_record.description
            accession = ""
            functionality = ""
            partial = ""
        else:
            splitted = seq_record.description.split('|')
            gene_name = splitted[1]
            accession = splitted[0]
            functionality = splitted[3]
            partial = splitted[13]

        splitted_gene_name = gene_name.split('*')
        gene = splitted_gene_name[0]
        allele = splitted_gene_name[1][0:2]

        #filter out abnormal V genes
        threshold = len(seq_record.seq)/2
        if int(anchor_index) > threshold:
            data['results'].append(seq_record.description)
            data['indexs'].append(anchor_index)
            data['extras'].append(extra)
            data['amino_acids'].append(amino_acid)
            data['gene_names'].append(gene_name)
            data['genes'].append(gene)
            data['alleles'].append(allele)
            data['accessions'].append(accession)
            data['functionalitys'].append(functionality)
            data['partials'].append(partial)
        else:
            data['error_indexs'].append(anchor_index)
            data['error_results'].append(seq_record.description)
            data['sequence'].append(seq_record.seq)

    return data



def generate_anchor_file(fileName, results, indexs):
    '''generate the anchor file for both v genes and j genes

    Attributes
    ----------
        fileName (str): file name for the anchor file generated
        results (list): list of results
        indexs (list): list of indexs
    '''
    fileName = fileName + '.csv'
    with open(fileName, 'w') as csv_file:
        fieldnames = ['gene','anchor_index']
        csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames,delimiter=';')
        csv_writer.writeheader()

        for result, index in zip(results, indexs):
            csv_writer.writerow({'gene': result, 'anchor_index': index})



def generate_error_file(fileName, error_results, sequence, error_indexs):
    # only works for csv files
    '''Generate the error anchor file for v genes with no C or C apearance
       in the begenning of the chain and generate the error anchor file for j
       genes with no [FW]GXG[ST]


    Attributes
    ----------
        fileName (str): file name for the complementary anchor file generated
    '''
    fileName = fileName.split('.csv')[0] + '_error.csv'
    with open(fileName, 'w') as csv_file:
        fieldnames = ['gene','sequence','anchor_index']
        csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames,delimiter=';')
        csv_writer.writeheader()

        for error_result, seq, error_index in zip(error_results, sequence, error_indexs):
            csv_writer.writerow({'gene': error_result, 'sequence':seq,'anchor_index': error_index})



def generate_extra_nucleotides_file_Vgene(fileName, gene_names, extras,
                                          amino_acids, accessions,
                                          functionalitys, partials):
    '''Generate the extra nucleotide file for v genes contaning extra nucleotide
        before the amino acids


    Attributes
    ----------
        fileName (str): file name for the complementary anchor file generated
    '''

    fileName = fileName.split('.csv')[0] + '_extra_nucleotides.csv'
    with open(fileName, 'w') as csv_file:
        fieldnames = ['gene_name','amino_acids','extra_nucleotides','accession','functionality','partial']
        csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames,delimiter=';')
        csv_writer.writeheader()

        for gene_name, amino_acid, extra, accession, functionality, partial in zip(gene_names, amino_acids, extras, accessions, functionalitys, partials):
            csv_writer.writerow({'gene_name': gene_name, 'amino_acids': amino_acid,'extra_nucleotides': extra,'accession':accession,'functionality':functionality,'partial':partial})


def generate_extra_nucleotides_file_Jgene(fileName, gene_names, extras,
                                          amino_acids, accessions,
                                          functionalitys, partials):
    '''Generate the extra nucleotide file for j genes contaning extra nucleotide
        after the amino acids


    Attributes
    ----------
        fileName (str): file name for the complementary anchor file generated
    '''

    fileName = fileName.split('.csv')[0] + '_extra_nucleotides.csv'
    with open(fileName, 'w') as csv_file:
        fieldnames = ['gene_name','extra_nucleotides','amino_acids','accession','functionality','partial']
        csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames,delimiter=';')
        csv_writer.writeheader()

        for gene_name, extra, amino_acid, accession, functionality, partial in zip(gene_names, extras, amino_acids, accessions, functionalitys, partials):
            csv_writer.writerow({'gene_name': gene_name,'extra_nucleotides': extra,'amino_acids':amino_acid,'accession':accession,'functionality':functionality,'partial':partial})



def write_excel_sheet_j(sheet, output_data):
    '''Generate the excel sheet for j genes with
       gene, allele, extra_nucleotides, amino_acids,
       accession, functionfunctionality and partial


    Attributes
    ----------
        sheet: the sheet to write into
    '''

    header = ['gene','allele','extra_nucleotides','amino_acids','accession','functionality','partial']
    output_data = {k: [x for _, _, x in sorted(zip(output_data['genes'], output_data['alleles'], v), key=lambda pair: (pair[0],pair[1]))] for k,v in output_data.items()}

    # set cell color
    genes = output_data['genes']
    colors = ['light_blue','light_green', 'light_orange','light_turquoise','light_yellow'] * int(len(set(genes)) / 5 + 1)

    styles = {g:xlwt.easyxf(f'pattern: pattern solid, fore_colour {c};') for g,c in zip(sorted(set(genes),key=genes.index), colors)}

    for column, heading in enumerate(header):
        sheet.write(0, column, heading)

    for row, gene in enumerate(output_data['genes']):
        sheet.write(row+1, 0, str(gene), styles[genes[row]])

    for row, allele in enumerate(output_data['alleles']):
        sheet.write(row+1, 1, int(allele), styles[genes[row]])

    for row, extra_nucleotides in enumerate(output_data['extras']):
        sheet.write(row+1, 2, str(extra_nucleotides), styles[genes[row]])

    #partials

    for row, amino in enumerate(output_data['amino_acids']):
        sheet.write(row+1, 3, str(amino), styles[genes[row]])

    for row, accession in enumerate(output_data['accessions']):
        sheet.write(row+1, 4, str(accession), styles[genes[row]])

    for row, functionality in enumerate(output_data['functionalitys']):
        sheet.write(row+1, 5, str(functionality), styles[genes[row]])

    for row, partial in enumerate(output_data['partials']):
        sheet.write(row+1, 6, partial, styles[genes[row]])





def write_excel_sheet_v(sheet, output_data):
    '''Generate the excel sheet for v genes with
       gene, allele, amino_acids, extra_nucleotides,
       accession, functionfunctionality and partial


    Attributes
    ----------
        sheet: the sheet to write into
    '''

    header = ['gene','allele','amino_acids','extra_nucleotides','accession','functionality','partial']
    output_data = {k: [x for _, _, x in sorted(zip(output_data['genes'], output_data['alleles'], v), key=lambda pair: (pair[0],pair[1]))] for k,v in output_data.items()}

    # set cell color
    genes = output_data['genes']
    colors = ['light_blue','light_green', 'light_orange','light_turquoise','light_yellow'] * int(len(set(genes)) / 5 + 1)

    styles = {g:xlwt.easyxf(f'pattern: pattern solid, fore_colour {c};') for g,c in zip(sorted(set(genes),key=genes.index), colors)}

    for column, heading in enumerate(header):
            sheet.write(0, column, heading)

    for row, gene in enumerate(output_data['genes']):
        sheet.write(row+1, 0, str(gene), styles[genes[row]])

    for row, allele in enumerate(output_data['alleles']):
        sheet.write(row+1, 1, int(allele), styles[genes[row]])

    for row, amino in enumerate(output_data['amino_acids']):
        sheet.write(row+1, 2, str(amino), styles[genes[row]])

    for row, extra_nucleotides in enumerate(output_data['extras']):
        sheet.write(row+1, 3, str(extra_nucleotides), styles[genes[row]])

    for row, accession in enumerate(output_data['accessions']):
        sheet.write(row+1, 4, str(accession), styles[genes[row]])

    for row, functionality in enumerate(output_data['functionalitys']):
        sheet.write(row+1, 5, str(functionality), styles[genes[row]])

    for row, partial in enumerate(output_data['partials']):
        sheet.write(row+1, 6, partial, styles[genes[row]])



if __name__ == '__main__':

    # Set commend line arugments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help = 'path to the input file')
    parser.add_argument('-o', help = 'path to the output file')
    args = parser.parse_args()

    if (args.i == None or args.o == None):
        print("Command line arugment error\nCorrect Usage:\npython anchors_generator.py -i <full path of input file> -o <full path to output file>")
        sys.exit()
    main(args)
