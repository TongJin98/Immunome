from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Anchor
from subprocess import Popen, PIPE, STDOUT
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage

#import different packages
import sys
from Bio import SeqIO
import csv
import math
import re
import xlwt
import os


def index(request):
    return render(request, 'index.html')
    #return HttpResponse("Anchors Generator for Human Vaccine Project")


# single file upload
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            #data=request.FILES['document']

            # get url of file
            fs = FileSystemStorage()
            name = fs.save(request.FILES['document'].name, request.FILES['document'])
            url = '/Users/pc/Desktop/Senior_Year/Senior Design/Immunome/mysite' + fs.url(name)
            analyze_fasta(url)
            #analyze_fasta(Anchor.objects.get(description='test5').document.read())
            #return redirect('process')
            return HttpResponse('success')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def analyze_fasta(infile):
    data = parse_j_genes(infile)
    print(data)

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
# def process(request):


# multiple files upload
# class FileFieldView(FormView):
#     form_class = FileFieldForm
#     template_name = 'upload.html'  # Replace with your template.
#     success_url = '...'  # Replace with your URL or reverse().
#
#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         files = request.FILES.getlist('file_field')
#         if form.is_valid():
#             for f in files:
#                 ...  # TODO something with each file.
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

# def test1(request):
#     command = ["pip", "-h"]
#     try:
#         process = Popen(command, stdout=PIPE, stderr=STDOUT)
#         output = process.stdout.read()
#         exitstatus = process.poll()
#         if (exitstatus==0):
#                 result = "Helper message: "
#                 return HttpResponse(result + str(output))
#         else:
#                 result = "Fail"
#                 return HttpResponse(result)
#
#     except Exception as e:
#                 result = "Fail with exception"
#                 return HttpResponse(result)
