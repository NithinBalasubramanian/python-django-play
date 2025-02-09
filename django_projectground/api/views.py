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
    try:
        array1 = np.random.rand(2,2)*1000
        array2 = np.random.rand(2,2)*1000
        result = np.add(array1, array2)
        np.save("./filesource/generated/numpy-files/random_array.npy", result)
        result.astype(int).tofile("./filesource/generated/numpy-files/random_array.txt", sep=",")
        fetchedResult = np.load("./filesource/generated/numpy-files/random_array.npy")
        return JsonResponse({
            "message": "array saved as npy and text file and fethed successfully",
            "data": fetchedResult.astype(int).tolist()
        })
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)