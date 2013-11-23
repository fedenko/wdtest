from django.shortcuts import render
from django.views.generic import ListView

from .models import Image


class Home(ListView):
    template_name = "imglist/home.html"
    model = Image
    context_object_name = 'images'
