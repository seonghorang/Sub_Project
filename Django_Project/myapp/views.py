from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .forms import Uploadfileform
from .utils import handle_uploaded_file

def index(request):
    return render(request, 'index.html')

def range(request):
    if request.method == "POST":
        form = Uploadfileform(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse('File uploaded and processed.')
        else:
            return HttpResponse('Invalid form.')
    else:
        form = Uploadfileform()
        return render(request, 'range.html', {'form': form})


