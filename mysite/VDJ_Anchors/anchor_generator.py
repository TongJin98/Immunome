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
from . import parse_genes
from . import write_files
from django.http import HttpResponse


def V_or_J_or_D(infile):
    first_line = str([a for a in infile][0])
    if re.split(string=first_line, pattern=r"[0-9\-]+\*")[0][-1] == 'J':
        v_or_j_or_d = 'J'
    elif re.split(string=first_line, pattern=r"[0-9\-]+\*")[0][-1] == 'V':
        v_or_j_or_d = 'V'
    elif re.split(string=first_line, pattern=r"[0-9\-]+\*")[0][-1] == 'D':
        v_or_j_or_d = 'D'
    else: print("Fasta file does not follow convetions")
    return v_or_j_or_d


def analyze_fasta(infile, v_or_j_or_d):
    output_filename = "current_ouput_file"

    if v_or_j_or_d == "V" :
        output_data = parse_genes.parse_v_genes(infile)
        #print("This is a V file"+str(output_data['results'][0]))
        response = write_files.generate_anchor_file(output_filename,
                 output_data['results'],
                 output_data['indexs'])
    elif v_or_j_or_d == "D" :
        output_data = parse_genes.parse_d_genes(infile)
        response = write_files.generate_anchor_file(output_filename,
                 output_data['results'],
                 output_data['indexs'])
    else:
        output_data = parse_genes.parse_j_genes(infile)
        response = write_files.generate_anchor_file(output_filename,
                 output_data['results'],
                 output_data['indexs'])
    return response


def excel_for_multiple_fasta(infiles):
    response = xlwt.Workbook()
    for infile in infiles:
        #print(infile)
        #print(type(infile))
        sheet = response.add_sheet(str(infile))
        #print(sheet)

        if V_or_J_or_D(infile) == 'V':
            output_data = parse_genes.parse_v_genes(infile)
            write_files.write_excel_sheet_v(sheet, output_data)
        elif V_or_J_or_D(infile) == 'D':
            output_data = parse_genes.parse_d_genes(infile)
            write_files.write_excel_sheet_d(sheet, output_data)
        else:
            output_data = parse_genes.parse_j_genes(infile)
            write_files.write_excel_sheet_j(sheet, output_data)

    response.save('contributions.xls')
    return response
