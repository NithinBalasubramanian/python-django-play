## API based implementation of python libraries

http://127.0.0.1:8000/ [local]

## numpy - play api 

1 __[get] api/serverhealth__ - check api running successfully

2 __[get] api/numpyRandomArray__ - just to check numpy implementation - return random array data

3 __[get] api/numpy-generation__ - generate two random array add and save as npy, txt and then feth data from npy to return json.

4 __[post] api/generateNumpyBasicOperationsOfTwoArray__ - various numpy operations and save data as json file 


    payload :

    {
        "array1": [1,2, 34 , 4],
        "array2": [4,5, 12, 56]
    }

## pandas - play api

5 __[get] api/pandRandomGeneration__ - Pandas check static datafram setup , save as csv and export as json

6 __[post] api/fetchDataFromReferenceFiles__ - Fetch file from existing reference file and send in json format , fetch based on file type and count based data

    payload :

    {
        "file": "csv",
        "count": 25
    }

7 __[post] api/fetchHeaderColumnsFromFile__ - Fetch headers from reference file and send the header columns

    payload:

    {
        "file_url": "/filesource/refsource/bios.csv"
    }

    Output Example:

    data = {[
        "athlete_id",
        "name",
        "born_date",
        "born_city",
        "born_region",
        "born_country",
        "NOC",
        "height_cm",
        "weight_kg",
        "died_date"
    ]}


8 __[post] api/fetchDataBasedOnHeader__ - Once fetch header send headers to get single particular column by sending header

    payload:

    {
        "header": "name",
        "count": 25
    }

    Example Output:

    data = [
        "Jean-François Blanchy",
        "Arnaud Boetsch"
    ]

9 __[post] api/fetchDataBasedOnArrayOfHeader__ - Once fetch header send headers to get only particular columns

    payload:

    {
        "file_url": "/filesource/refsource/bios.csv",
        "headers": ["name", "born_country"],
        "count": 25
    }

    Example output:

    "data": [
        {
            "name": "Jean-François Blanchy",
            "born_country": "FRA"
        },
        {
            "name": "Arnaud Boetsch",
            "born_country": "FRA"
        },
        {
            "name": "Jean Borotra",
            "born_country": "FRA"
        },
        {
            "name": "Jacques Brugnon",
            "born_country": "FRA"
        }
    ]

10 __[post] api/uploadFileApiAndFetchData__ - Upload file and save in folder and fetch data and list


    payload: [form-data]

    {
        "file": "files" select csv or excel,
        "count" : 20
    }


11 __[post] api/fetchValuesOfColumSelected__ - set file , filed will give count , further add search and subfield to get count of subfields

    payload:

    {
        "file_url": "/filesource/refsource/bios.csv",
        "field": "born_country",
        "search": "IND",  or "USA" [optional]
        "sub_field": "born_region"  or "born_city" [optional]
    }

    output without optional

    {
    "data": [
        {
            "born_country": "USA",
            "count": 9641
        },
        {
            "born_country": "GER",
            "count": 6891
        },
        {
            "born_country": "GBR",
            "count": 5792
        },
        {
            "born_country": "FRA",
            "count": 5143
        },
        {
            "born_country": "ITA",
            "count": 4709
        },
        {
            "born_country": "CAN",
            "count": 4616
        },
        {
            "born_country": "RUS",
            "count": 4276
        },
        {
            "born_country": "AUS",
            "count": 3009
        }
    ]}


    output with option given

    {
    "data": [
        {
            "born_region": "Punjab",
            "count": 94
        },
        {
            "born_region": "Maharashtra",
            "count": 56
        },
        {
            "born_region": "West Bengal",
            "count": 49
        },
        {
            "born_region": "Haryana",
            "count": 43
        }
    ]   
    }