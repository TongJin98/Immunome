from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Anchor
from subprocess import Popen, PIPE, STDOUT


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
'''