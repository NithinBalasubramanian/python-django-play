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
from io import StringIO, BytesIO 
import csv
from django.http import FileResponse
import requests
from urllib.parse import urlparse

import io
import matplotlib.pyplot as plt
from django.http import FileResponse, HttpResponse

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

# to remove nan for a proper json export
def clearData(data):
    return data.replace({np.nan: None})

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

                        # to remove nan for a proper json export
                        display_data_cleaned = clearData(display_data)

                        #Convert to list of dictionaries for JSON serialization:
                        return JsonResponse({"data": display_data_cleaned.to_dict(orient='records')})

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

def generateExcelByColumns(request):
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

                        display_data.to_csv("."+file+"_generated"+ ext)

                        url = "."+file+"_generated"+ ext

                        #Convert to list of dictionaries for JSON serialization:
                        return JsonResponse({'message': 'File generated successfully', 'url': url})


            else:
                return JsonResponse({"error": "'headers' must be a list"}, status=400)

        else:
            return JsonResponse({"error": "Missing 'headers' key in payload"}, status=400)
 
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
    

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


@csrf_exempt
def dowmloadCheck(request):
      # Generate data for the CSV

     # Ensure this is a POST request
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON in request body."}, status=400)

    if "file_url" in payload:
        file_url = payload["file_url"]
        
        # Parse the URL to get the file name and extension
        # parsed_url = urlparse(file_url)
        # file_name = os.path.basename(file_url)
        
        file_base, ext = os.path.splitext(file_url) # Renamed 'file' to 'file_base' to avoid confusion
        ext = ext.lower() # Normalize the extension to lowercase.

        data = None
        try:
            # Use the imported 'requests' library here
            # response = requests.get(file_url, stream=True)
            # response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            
            # # Read content into a BytesIO buffer
            # file_content_buffer = BytesIO(response.content)

            if ext == ".csv":
                data = pd.read_csv("./"+ file_url)
            elif ext == ".xlsx":
                try:
                    data = pd.read_excel("./"+ file_url, engine='openpyxl')
                except ImportError:
                    return JsonResponse({"error": "Missing 'openpyxl' library. Please install it (pip install openpyxl)."}, status=500)
                except Exception as e:
                    return JsonResponse({"error": f"Error reading XLSX file: {str(e)}. Ensure file is valid Excel format."}, status=400)
            elif ext == ".xls":
                try:
                    data = pd.read_excel("./"+ file_url, engine='xlrd')
                except ImportError:
                    return JsonResponse({"error": "Missing 'xlrd' library. Please install it (pip install xlrd)."}, status=500)
                except Exception as e:
                    return JsonResponse({"error": f"Error reading XLS file: {str(e)}. Ensure file is valid Excel format."}, status=400)
            else:
                print(f"Unsupported file type: {ext}")
                return JsonResponse({"error": f"Unsupported file type: {ext}"}, status=400)

            # return JsonResponse({"data": data})


        except requests.exceptions.RequestException as e:
            # Specific error for issues with fetching the URL
            return JsonResponse({"error": f"Error fetching file from URL: {str(e)}"}, status=400)
        except Exception as e:
            # Catch any other unexpected errors during file processing
            return JsonResponse({"error": f"An unexpected error occurred during file processing: {str(e)}"}, status=500)
            
        if data is None:
            return JsonResponse({"error": "Could not process file. Data is empty or unsupported."}, status=500)

        # Create an in-memory text buffer for CSV writing
        csv_buffer = StringIO()
        # Use pandas to write DataFrame to CSV directly into the StringIO buffer
        data.to_csv(csv_buffer, index=False) # index=False prevents writing the DataFrame index as a column

        # Get the string value from the StringIO buffer
        csv_string = csv_buffer.getvalue()

        # Encode the string to bytes and create a BytesIO object
        # FileResponse expects a file-like object that provides bytes
        response_buffer = BytesIO(csv_string.encode('utf-8'))

        # Create the FileResponse
        # FileResponse takes a file-like object (BytesIO in this case)
        django_response = FileResponse(response_buffer, content_type='text/csv') # Renamed to avoid confusion with 'requests' response

        # Set the Content-Disposition header for download
        django_response['Content-Disposition'] = 'attachment; filename="my_generated_data.csv"'

        return django_response
