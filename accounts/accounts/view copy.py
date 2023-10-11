from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as drf_status
import requests

class GetBalanceSumView(APIView):
    def get(self, request):
        # Retrieve dynamic start_date and end_date from query parameters
        start_date = request.GET.get('start_date', '2023-01-01')
        end_date = request.GET.get('end_date', '2023-10-01')

        # Define the URL for the Odoo API
        url = "http://13.49.59.166:8069/sum_bal"

        # Define the request payload (JSON data) with dynamic dates
        payload = {
            "jsonrpc": "2.0",
            "params": {
                "login": "sugam.pandey@gmail.com",
                "password": "sugam@kmnss!23#",
                "db": "KMNSS",
                "start_date": start_date,
                "end_date": end_date
            }
        }

        try:
            # Send a POST request to the Odoo API
            response = requests.post(url, json=payload)

            # Check if the request was successful (HTTP status code 200)
            if response.status_code == 200:
                result = response.json()

                # Extract the relevant data from the JSON response
                status = result.get('result', {}).get('status')
                response_data = result.get('result', {}).get('response', [])
                total_balance = result.get('result', {}).get('total_balance')
                message = result.get('result', {}).get('message')

                # Construct the response JSON
                response_data = {
                    "status": status,
                    "response": response_data,
                    "total_balance": total_balance,
                    "message": message
                }

                return Response(response_data, status=drf_status.HTTP_200_OK)

            else:
                # Handle the case when the API request is not successful
                error_message = f"API request failed with status code {response.status_code}"
                return Response({"error": error_message}, status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.RequestException as e:
            # Handle other request-related errors (e.g., network issues)
            error_message = f"API request failed: {e}"
            return Response({"error": error_message}, status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR)
