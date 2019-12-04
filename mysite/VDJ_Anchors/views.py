from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Anchor
from subprocess import Popen, PIPE, STDOUT
from .forms import UploadFileForm

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
            #return HttpResponseRedirect('/success/url/')
            return HttpResponse(form.document)
    else:
        form = UploadFileForm()
    #return render(request, 'upload.html', {'form': form})
    return render(request, 'upload.html',{
        'form': form
    })


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

'''def test1(request):
    command = ["pip", "-h"]
    try:
        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        output = process.stdout.read()
        exitstatus = process.poll()
        if (exitstatus==0):
                result = "Helper message: "
                return HttpResponse(result + str(output))
        else:
                result = "Fail"
                return HttpResponse(result)

    except Exception as e:
                result = "Fail with exception"
                return HttpResponse(result)
'''
