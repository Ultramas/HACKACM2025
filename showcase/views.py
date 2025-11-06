from django.shortcuts import render
from .models import Melody

def analyze(request):
    result = None

    if request.method == "POST":
        note_input = request.POST.get("melody", "")
        melody_obj = Melody(notes=note_input)
        data = melody_obj.analyze()

        # ✅ Convert dict to safe object for template
        class R: pass
        result = R()
        result.score = data["score"]
        result.feedback = data["feedback"]

    return render(request, "analyze.html", {"result": result})

def index(request):
    return render(request, "index.html")
