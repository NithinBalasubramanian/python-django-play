from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import numpy as np

# Create your views here.

def serverHealth(request):
    return HttpResponse("Hello there is my first django api")

def numpyRandomArray(request):
    display_data = np.random.rand(2,2)*1000
    return JsonResponse({
        "data": display_data.astype(int).tolist()
    })

def numpyFileGeneration(request):
    display_data = np.random.rand(2,2)*1000
    return JsonResponse({
        "data": display_data.astype(int).tolist()
    })