# from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse


def index(request):
    response = """
        <div style="text-align:right;">
          <a href={}>About</a>
        </div>
        Rango says hey there partner!
    """.format(reverse('about'))
    return HttpResponse(response)


def about(request):
    response = """
        <div style="text-align:right;">
          <a href={}>Index</a>
        </div>
        Rango says here is the about page.
    """.format(reverse('index'))
    return HttpResponse(response)
