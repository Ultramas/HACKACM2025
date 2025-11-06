from django.shortcuts import render
from .models import Melody

def analyze(request):
    result = None

    if request.method == "POST":
        note_input = request.POST.get("melody", "")
        melody_obj = Melody(notes=note_input)
        result = melody_obj.analyze()

    return render(request, "analyze.html", {"result": result})


def index(request):
    result = None

    if request.method == "POST":
        note_input = request.POST.get("melody", "")
        melody_obj = Melody(notes=note_input)
        result = melody_obj.analyze()

    return render(request, "index.html", {"result": result})
