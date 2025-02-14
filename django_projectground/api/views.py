from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import os

import numpy as np
import pandas as pd

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
    
# post method 
def generateNumpyBasicOperationsOfTwoArray(request):
    data = json.loads(request.body)
    if (data and data['array1'] and data['array2']):
        try:
            arr1 = np.array(data['array1'])
            arr2 = np.array(data['array2'])
            arr = np.array((arr1, arr2), dtype=int)
            added_arr = np.add(arr1, arr2)
            subtracted_arr = np.subtract(arr1, arr2)
            multipy_arr = np.multiply(arr1, arr2)
            flatterened = arr.flatten()

            a = {
                "message": "success",
                "data" : {
                    "array": arr.tolist(),
                    "added": added_arr.tolist(),
                    "subtract": subtracted_arr.tolist(),
                    "multiply": multipy_arr.tolist(),
                    "flattern": flatterened.tolist(),
                    "mean": int(flatterened.mean()),
                    "max": int(flatterened.max()),
                    "min": int(flatterened.min())
                }
            }

            file_dir = "./filesource/generated/numpy-files/"
            os.makedirs(file_dir, exist_ok=True)
            file_path = os.path.join(file_dir, "data.json")

            # Save as JSON
            with open(file_path, 'w') as f:
                json.dump(a, f, indent=4)  # Use indent for pretty printing (optional)

            # with open(file_path, 'r') as f:
            #     loaded_data = json.load(f)

        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=500)
    else:
        a = {
            "message": "failed"
        }
    return JsonResponse(a)

def pandRandomGeneration(request):
    try:
        data = pd.DataFrame({
            "Name": ["nithin", "kiran", "sam", "barath"],
            "age": ["27", "28", "31", "29"]
        })  

        # Convert to a format suitable for JSON (list of dictionaries)
        data_list = data.to_dict(orient='records')  # 'records' format is often best

        data.to_csv("./filesource/generated/pandas-files/panda-1-test.csv")

        returnData = {
            "data": data_list
        }
        return JsonResponse(returnData)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
    
def fetchDataFromReferenceFiles(request):
    try:
        payload = json.loads(request.body)
        
        if (payload and payload["file"] == "csv"):
            data = pd.read_csv("./filesource/refsource/bios.csv") # csv is fetched faster than excel
        else:
           data= pd.read_excel("./filesource/refsource/olympics-data.xlsx")
        
        if (payload and payload["count"]):
            data_list = data.head(payload["count"]).to_dict(orient='records') 
        else:
            data_list = data.head(10).to_dict(orient='records') 

        
        return JsonResponse({ 
            "message": "Data fetched successfully", 
            "fileTypeExtracted": payload["file"], 
            "length": payload["count"], 
            "data": data_list
        }, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)