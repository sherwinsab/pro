# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def signup(requset):
    template = loader.get_template('signup.html')
    return HttpResponse(template.render())

def signin(requset):
    template = loader.get_template('signin.html')
    return HttpResponse(template.render())

def product_listing(requset):
    template = loader.get_template('product_listing.html')
    return HttpResponse(template.render())