import numpy as np
import pandas as pd
from urllib.parse import unquote
from io import StringIO, BytesIO 
from django.http import HttpResponse, JsonResponse
import json

from django.http import FileResponse
import requests
from urllib.parse import urlparse

import io
import matplotlib.pyplot as plt
from django.http import FileResponse, HttpResponse

#  Simple test graph api 

def chart_api(request):
    # Data for the grouped bar chart
    fruits = ['Apples', 'Bananas', 'Cherries', 'Dates']
    sales_2023 = [400, 350, 300, 450]
    sales_2024 = [450, 400, 320, 470]
    target_sales = [420, 380, 310, 460]

    # Set up the plot (from the previous example)
    bar_width = 0.25
    x_positions = np.arange(len(fruits))

    # Create a new Matplotlib figure
    plt.figure(figsize=(10, 6))

    plt.bar(x_positions - bar_width, sales_2023, color='skyblue', width=bar_width, label='2023 Sales')
    plt.bar(x_positions, sales_2024, color='orange', width=bar_width, label='2024 Sales')
    plt.bar(x_positions + bar_width, target_sales, color='green', width=bar_width, label='Target Sales')

    plt.title('Fruit Sales Comparison')
    plt.xlabel('Fruits')
    plt.ylabel('Sales')
    plt.xticks(x_positions, fruits)
    plt.legend()
    plt.tight_layout() # Adjusts plot to prevent labels from being cut off

    # --- This is the key part for the API response ---

    # Create an in-memory buffer
    buf = io.BytesIO()

    # Save the plot to the buffer as a PNG image
    plt.savefig(buf, format='png')

    # Close the plot figure to free up memory
    plt.close()

    # Rewind the buffer's cursor to the beginning
    buf.seek(0)

    # Return the buffer content as a FileResponse with the correct content type
    return FileResponse(buf, content_type='image/png')

def generateGraph(request):

    # {
    # "graphType": "bar",
    # "data_x": [1,5,7,8],
    # "data_y": [10,5,10,20],
    # "title": "Test graph",
    # "labelx": "X-count",
    # "labely": "Y-Count"
    # }

    try:
        payload = json.loads(request.body)
        graphType = payload.get('graphType', 'bar')
        title = payload.get("title", "Graph")
        data_x = payload.get("data_x")
        data_y = payload.get("data_y")
        xlabel = payload.get("labelx", "X")
        ylabel = payload.get("labely", "Y")


        if data_x and data_y:
            plt.figure(figsize=(10, 6))

            if graphType.lower() == 'bar':
                plt.bar(data_x, data_y)
            elif graphType.lower() == 'plot':
                plt.plot(data_x, data_y)
            elif graphType.lower() == 'barh':
                plt.barh(data_x, data_y)
            elif graphType.lower() == 'scatter':
                plt.scatter(data_x, data_y)
            else:
                plt.plot(data_x, data_y)

            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.legend()
            plt.tight_layout()
            # plt.grid(True)
            # Create an in-memory buffer
            buf = io.BytesIO()

            # Save the plot to the buffer as a PNG image
            plt.savefig(buf, format='png')

            # Close the plot figure to free up memory
            plt.close()

            # Rewind the buffer's cursor to the beginning
            buf.seek(0)

            # Return the buffer content as a FileResponse with the correct content type
            return FileResponse(buf, content_type='image/png')
        else:
            return JsonResponse({
                "error": "Provide proper data"
            })

    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)