## API based implementation of python libraries

http://127.0.0.1:8000/ [local]

## numpy - play api 

1 [get] api/serverhealth - check api running successfully

2 [get] api/numpyRandomArray - just to check numpy implementation - return random array data

3 [get] api/numpy-generation - generate two random array add and save as npy, txt and then feth data from npy to return json.

4 [post] api/generateNumpyBasicOperationsOfTwoArray - various numpy operations and save data as json file 

    payload exp = {
        "array1": [1,2, 34 , 4],
        "array2": [4,5, 12, 56]
    }
