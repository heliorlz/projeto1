from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(
        request,
        "recipes/home.html",
        context={
            "name": "Curso Django Web e REST Framework",
        },
    )


def contato(request):
    return HttpResponse("Contato")


def sobre(request):
    return HttpResponse("Sobre")
