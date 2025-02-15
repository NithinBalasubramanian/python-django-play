from django.urls import path
from . import views

urlpatterns = [
    path("serverhealth", views.serverHealth),

    path("numpyRandomArray", views.numpyRandomArray),
    path("numpy-generation", views.numpyFileGeneration),
    path("generateNumpyBasicOperationsOfTwoArray", views.generateNumpyBasicOperationsOfTwoArray),

    path("pandas-generation", views.pandRandomGeneration),
    path("fetchDataFromReferenceFiles", views.fetchDataFromReferenceFiles),
    path("fetchHeaderColumnsFromFile", views.fetchHeaderColumnsFromFile),
    path("fetchDataBasedOnHeader", views.fetchDataBasedOnHeader),
    path("fetchDataBasedOnArrayOfHeader", views.fetchDataBasedOnArrayOfHeader),

    path("uploadFileApiAndFetchData", views.uploadFileApiAndFetchData)
]