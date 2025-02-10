## API based implementation of python libraries

http://127.0.0.1:8000/ [local]

## numpy - play api 

1 __[get] api/serverhealth__ - check api running successfully

2 __[get] api/numpyRandomArray__ - just to check numpy implementation - return random array data

3 __[get] api/numpy-generation__ - generate two random array add and save as npy, txt and then feth data from npy to return json.

4 __[post] api/generateNumpyBasicOperationsOfTwoArray__ - various numpy operations and save data as json file 

    payload exp = {
        "array1": [1,2, 34 , 4],
        "array2": [4,5, 12, 56]
    }

## pandas - play api

5 __[get] api/pandRandomGeneration__ - Pandas check static datafram setup , save as csv and export as json