from django.shortcuts import render
from .models import Melody

def analyze(request):
    result = None
    if request.method == "POST":
        melody_obj = Melody(notes=request.POST.get("melody"))
        result = melody_obj.analyze()

    return render(request, "analyze.html", {"result": result})
