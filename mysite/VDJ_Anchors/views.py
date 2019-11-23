from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import VGene
from subprocess import Popen, PIPE, STDOUT
from .forms import UploadFileForm


def index(request):
    return render(request, 'index.html')
    #return HttpResponse("Anchors Generator for Human Vaccine Project")

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


def test2(request):
    command = ["python3", "/Users/axns/Documents/GitHub/HVP_anchors_generator/anchors_generator.py", "-i", "/Users/axns/Documents/GitHub/HVP_anchors_generator/IMGT", "-o", "/Users/axns/Desktop/untitled folder"]

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


def test3(request):

    Anchor.main("-i", "/Users/axns/Documents/GitHub/HVP_anchors_generator/IMGT", "-o", "/Users/axns/Desktop/untitled folder")

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def parse_genes(request):






'''

