from django.shortcuts import render

def visualizer(request):
    return render(request, "visualizer.html")
