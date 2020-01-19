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



def parse_d_genes(infile):
    '''Find the 3'end extra nucleotide, sequence, 5'end extra nucleotide for
    three different reading frames.

    Attributes
    ----------
        infile (str): full path to input file
    '''

    # dictionary to store resulting data
    data = {'five_prime_extra_frame_one' : [],
            'sequence_frame_one' : [],
            'three_prime_extra_frame_one' : [],
            'five_prime_extra_frame_two' : [],
            'sequence_frame_two' : [],
            'three_prime_extra_frame_two' : [],
            'five_prime_extra_frame_three' : [],
            'sequence_frame_three' : [],
            'three_prime_extra_frame_three' : [],
            'accessions' : [],
            'functionalitys' : [],
            'partials' : [],
            'genes' : [],
            'alleles' : []
            }

    for seq_record in SeqIO.parse(infile, "fasta"):
        three_prime_extras = []
        five_prime_extras = []
        three_amino_acids = []

        # try out 3 different frames
        for i in range(3):

            # save 5' extra nucleotides to five_prime_extras
            five_prime_extra = seq_record.seq[0:i]
            five_prime_extras.append (five_prime_extra)
            #split record to match triplets
            seq_record_temp = seq_record.seq[i:]
            floor = math.floor(len(seq_record_temp)/3)
            index = len(seq_record_temp) - (floor*3)

            #save 3' extra nucleotides to three_prime_extra
            if index != 0:
                three_prime_extra = seq_record.seq[-(index):]
                three_prime_extras.append (three_prime_extra)
                seq_record_temp = seq_record_temp[:-(index)]
                # translating from dna to amino acid
                translated_seq = seq_record_temp.translate()
                three_amino_acids.append (translated_seq)
            else:
                three_prime_extras.append ("")
                translated_seq = seq_record_temp.translate()
                three_amino_acids.append (translated_seq)

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

        #add data to library
        data['genes'].append(gene)
        data['alleles'].append(allele)
        data['accessions'].append(accession)
        data['functionalitys'].append(functionality)
        data['partials'].append(partial)

        data['five_prime_extra_frame_one'].append(five_prime_extras[0])
        data['sequence_frame_one'].append(three_amino_acids[0])
        data['three_prime_extra_frame_one'].append(three_prime_extras[0])

        data['five_prime_extra_frame_two'].append(five_prime_extras[1])
        data['sequence_frame_two'].append(three_amino_acids[1])
        data['three_prime_extra_frame_two'].append(three_prime_extras[1])

        data['five_prime_extra_frame_three'].append(five_prime_extras[2])
        data['sequence_frame_three'].append(three_amino_acids[2])
        data['three_prime_extra_frame_three'].append(three_prime_extras[2])

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
