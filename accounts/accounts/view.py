import xmlrpc.client
from django.http import JsonResponse
from django.views import View
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class GetBalanceSumView(View):
    def get(self, request):
        # Retrieve dynamic start_date and end_date from query parameters
        start_date = request.GET.get('start_date', '2023-01-01')
        end_date = request.GET.get('end_date', '2023-10-01')

        # Log the request parameters for debugging
        logging.debug(f"Request Parameters - start_date: {start_date}, end_date: {end_date}")

        # Define the URL for the Odoo XML-RPC server
        url = 'http://13.49.59.166:8069'
        db = 'KMNSS'
        username = 'sugam.pandey@gmail.com'
        password = 'sugam@kmnss!23#'

        # Replace these with your target date range
        target_date_start = '2020-10-01'
        target_date_end = '2027-10-31'

        try:
            # Authenticate and get user ID
            common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
            models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
            uid = common.authenticate(db, username, password, {})

            # Call the getbalance method with both date range parameters
            balances = models.execute_kw(
                db,
                uid,
                password,
                'account.account',
                'getbalance',
                [target_date_start, target_date_end],
                {}
            )

            # Initialize the total balance variable
            total_balance = 0.0

            # Check if balances is a list and not empty
            if isinstance(balances, list) and balances:
                for balance in balances:
                    # Add the balance to the total balance
                    total_balance += balance['balance']

                # Construct the response JSON
                response_data = {
                    "status": "success",
                    "response": balances,
                    "total_balance": total_balance,
                    "message": "Balances retrieved successfully."
                }

                return JsonResponse(response_data, status=200)

            else:
                return JsonResponse({"status": "error", "message": "No balances found."}, status=500)

        except xmlrpc.client.Fault as err:
            return JsonResponse({"status": "error", "message": f"XML-RPC Fault: {err}"}, status=500)
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"An error occurred: {e}"}, status=500)
