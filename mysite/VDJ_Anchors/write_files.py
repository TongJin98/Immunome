'''anchors_generator.py

This python file runs to generate anchor_file (csv), error_file (csv),
extra_nucleotide_files (csv) and excel_sheets containing gene, allele,
extra_nucleotides, amino_acids, accession, functionfunctionality and partial.
'''
import argparse
import sys
from Bio import SeqIO
import csv
import math
import re
import xlwt
import os
from django.http import HttpResponse


def generate_anchor_file(fileName, results, indexs):
    '''generate the anchor file for both v genes and j genes

    Attributes
    ----------
        fileName (str): file name for the anchor file generated
        results (list): list of results
        indexs (list): list of indexs
    '''
    response = HttpResponse(content_type = 'test/csv')
    response['Content-Disposition'] = 'attachment; filename = "GenerateAnchor.csv"'
    fieldnames = ['gene','anchor_index']
    csv_writer = csv.DictWriter(response,fieldnames=fieldnames,delimiter=';')
    csv_writer.writeheader()

    for result, index in zip(results, indexs):
        csv_writer.writerow({'gene': result, 'anchor_index': index})
    return response



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




def write_excel_sheet_d(sheet, output_data):
    '''Generate the excel sheet for d genes with
       gene, allele, amino_acids, extra_nucleotides on both 5' end and 3'end of
       three different reading frams, accession, functionfunctionality and partial

    Attributes
    ----------
        sheet: the sheet to write into
    '''

    header = ['gene','allele', 'sequence_frame_1',
              '3_prime_extra_frame_1', '5_prime_extra_frame_2',
              'sequence_frame_2', '3_prime_extra_frame_2',
              '5_prime_extra_frame_3', 'sequence_frame_3',
              '3_prime_extra_frame_3', 'accession','functionality','partial']
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

    for row, sequence_one in enumerate(output_data['sequence_frame_one']):
        sheet.write(row+1, 2, str(sequence_one), styles[genes[row]])

    for row, three_one in enumerate(output_data['three_prime_extra_frame_one']):
        sheet.write(row+1, 3, str(three_one), styles[genes[row]])

    for row, five_two in enumerate(output_data['five_prime_extra_frame_two']):
        sheet.write(row+1, 4, str(five_two), styles[genes[row]])

    for row, sequence_two in enumerate(output_data['sequence_frame_two']):
        sheet.write(row+1, 5, str(sequence_two), styles[genes[row]])

    for row, three_two in enumerate(output_data['three_prime_extra_frame_two']):
        sheet.write(row+1, 6, str(three_two), styles[genes[row]])

    for row, five_three in enumerate(output_data['five_prime_extra_frame_three']):
        sheet.write(row+1, 7, str(five_three), styles[genes[row]])

    for row, sequence_three in enumerate(output_data['sequence_frame_three']):
        sheet.write(row+1, 8, str(sequence_three), styles[genes[row]])

    for row, three_three in enumerate(output_data['three_prime_extra_frame_three']):
        sheet.write(row+1, 9, str(three_three), styles[genes[row]])

    for row, accession in enumerate(output_data['accessions']):
        sheet.write(row+1, 10, accession, styles[genes[row]])

    for row, functionality in enumerate(output_data['functionalitys']):
        sheet.write(row+1, 11, functionality, styles[genes[row]])

    for row, partial in enumerate(output_data['partials']):
        sheet.write(row+1, 12, partial, styles[genes[row]])
