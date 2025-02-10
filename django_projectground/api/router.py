from django.urls import path
from . import views

urlpatterns = [
    path("serverhealth", views.serverHealth),

    path("numpyRandomArray", views.numpyRandomArray),
    path("numpy-generation", views.numpyFileGeneration),
    path("generateNumpyBasicOperationsOfTwoArray", views.generateNumpyBasicOperationsOfTwoArray),

    path("pandas-generation", views.pandRandomGeneration),
]