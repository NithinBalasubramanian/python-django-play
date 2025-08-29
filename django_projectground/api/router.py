from django.urls import path
from . import views
from .Container import MatlibplotController

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

    path("uploadFileApiAndFetchData", views.uploadFileApiAndFetchData),
    path("fetchValuesOfColumSelected", views.fetchValuesOfColumSelected),
    path("generateExcelByColumns", views.generateExcelByColumns),

    path("downloadCSV", views.dowmloadCheck),

    # Graph based API calls 

    path("matplot", MatlibplotController.chart_api),
    path("generateGraph",MatlibplotController.generateGraph)
]