from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
import json
import os
import re

import numpy as np
import pandas as pd
from urllib.parse import unquote

# Create your views here.

def clean_column_names(columns):
    return [re.sub(r'\s+', ' ', col).replace('\u00a0', '').strip() for col in columns]


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
    
def fetchHeaderColumnsFromFile(request):
    try:
        payload = json.loads(request.body)

        if "file_url" in payload:

            file, ext = os.path.splitext(payload["file_url"])  # Split filename and extension
            ext = ext.lower() # Normalize the extension to lowercase.

            if ext == ".csv":
                data = pd.read_csv("./" + payload["file_url"]) # csv is fetched faster than excel
            elif ext == ".xlsx" or ext == ".xls":  # Handle both xlsx and xls
                data = pd.read_excel("./" + payload["file_url"]) # csv is fetched faster than excel
            else:
                print(f"Unsupported file type: {ext}")
                return None, None  # Or raise an exception if you prefer      
                  
            headers = data.columns.tolist()

            
            return JsonResponse({ 
                "message": "Header fetched successfully", 
                "data": headers
            }, safe=False)
        else:
            return JsonResponse({
                "error": "No files path found"
            })
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)

def fetchDataBasedOnHeader(request):
    try:
        payload = json.loads(request.body)
        data = pd.read_csv("./filesource/refsource/bios.csv")
        if "header" in payload:  # Check if the key exists (important!)
            header = payload["header"]

            if isinstance(header, str): #Check if it is a string.
                if header in data.columns: #Check if header exists in the dataframe.
                    if "count" in payload:
                        display_data = data[header].head(payload["count"])
                    else:
                        display_data = data[header].head(15)
                    return JsonResponse({ 
                        "message": "Filtered data fetched successfully", 
                        "data": display_data.tolist()
                    }, safe=False)

                else:
                    return JsonResponse({"error": f"Header '{header}' not found in CSV"}, status=400)

            else:
                return JsonResponse({"error": "Header must be a string"}, status=400)

        else:
            return JsonResponse({"error": "Missing 'header' key in payload"}, status=400)
      
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
    

@csrf_exempt
def fetchDataBasedOnArrayOfHeader(request):
    try:
        payload = json.loads(request.body)
        if "file_url" in payload:

            file, ext = os.path.splitext(payload["file_url"])  # Split filename and extension
            ext = ext.lower() # Normalize the extension to lowercase.

            if ext == ".csv":
                data = pd.read_csv("./" + payload["file_url"]) # csv is fetched faster than excel
            elif ext == ".xlsx" or ext == ".xls":  # Handle both xlsx and xls
                data = pd.read_excel("./" + payload["file_url"]) # csv is fetched faster than excel
            else:
                print(f"Unsupported file type: {ext}")
                return None, None  # Or raise an exception if you prefer            
        
        else:
            return JsonResponse({
                "error": "No files path found"
            })

        if "headers" in payload:  # Changed key to "headers" (plural)
            headers = payload["headers"]

            if isinstance(headers, list):  # Must be a list of headers

                # Check if all headers exist in the dataframe.
                if all(h in data.columns for h in headers):
                        if "count" in payload:
                            display_data = data[headers].head(payload["count"])
                        else:
                            display_data = data[headers].head(15)

                        #Convert to list of dictionaries for JSON serialization:
                        return JsonResponse({"data": display_data.to_dict(orient='records')})

                else:
                    missing_headers = [h for h in headers if h not in data.columns]
                    return JsonResponse({"error": f"Headers '{', '.join(missing_headers)}' not found in CSV"}, status=400)

            else:
                return JsonResponse({"error": "'headers' must be a list"}, status=400)

        else:
            return JsonResponse({"error": "Missing 'headers' key in payload"}, status=400)
 
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
    
    
@csrf_exempt
def uploadFileApiAndFetchData(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            target_folder = "./filesource/refsource/uploaded"
            count = request.POST.get('count') 

            target_folder = os.path.normpath(target_folder)
            if target_folder.startswith(".."):
                return JsonResponse({'error': 'Invalid target folder'}, status=400)

            file_path = os.path.join(target_folder, uploaded_file.name.replace(' ', '_'))
            file_name = default_storage.save(file_path, uploaded_file)
            file_url = default_storage.url(file_name)
            file_url = unquote(file_url).replace(' ', '_')  # Decode %20 into space

            file, ext = os.path.splitext(file_url)
            ext = ext.lower()

            if ext == ".csv":
                data = pd.read_csv("./" + file_url) # csv is fetched faster than excel
            elif ext == ".xlsx" or ext == ".xls":  # Handle both xlsx and xls
                data = pd.read_excel("./" + file_url) # csv is fetched faster than excel
            else:
                print(f"Unsupported file type: {ext}")
                return None, None  # Or raise an exception if you prefer  

            data.columns = clean_column_names(data.columns)
            data = data.replace({np.nan: None})          
        
            if count:
                fetched_data = data.head(int(count))
            else:
                fetched_data = data.head(20)


            return JsonResponse({'message': 'File uploaded successfully', 'file_url': file_url, 'fetched_data': fetched_data.to_dict(orient='records')}, status=200)

        else:
            return JsonResponse({'error': 'No file provided'}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

def fetchValuesOfColumSelected(request):
    try:

        payload = json.loads(request.body)

        if "file_url" in payload:

            file, ext = os.path.splitext(payload["file_url"])  # Split filename and extension
            ext = ext.lower() # Normalize the extension to lowercase.

            if ext == ".csv":
                data = pd.read_csv("./" + payload["file_url"]) # csv is fetched faster than excel
            elif ext == ".xlsx" or ext == ".xls":  # Handle both xlsx and xls
                data = pd.read_excel("./" + payload["file_url"]) # csv is fetched faster than excel
            else:
                print(f"Unsupported file type: {ext}")
                return None, None  # Or raise an exception if you prefer            
        
        else:
            return JsonResponse({
                "error": "No files path found"
            })

        if "field" in payload:
            if "search" in payload and "sub_field" in payload:
                result_data = data[data[payload["field"]]== payload["search"]][payload["sub_field"]].value_counts().reset_index()
            else:
                result_data = data[payload["field"]].value_counts().reset_index()

            #Convert to list of dictionaries for JSON serialization:
            return JsonResponse({"data": result_data.to_dict(orient='records')})

            
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500) 