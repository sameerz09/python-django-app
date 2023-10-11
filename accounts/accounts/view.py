import xmlrpc.client
from django.http import JsonResponse
from rest_framework.views import APIView
from datetime import datetime

class GetBalanceSumView(APIView):
    def get(self, request):
        # Replace these with your Odoo server details
        odoo_url = 'http://13.49.59.166:8069'
        odoo_db = 'KMNSS'
        odoo_username = 'sugam.pandey@gmail.com'
        odoo_password = 'sugam@kmnss!23#'

        # Replace these with your target date range
        start_date = request.GET.get('start_date', '2023-01-01')
        end_date = request.GET.get('end_date', '2023-10-01')
        selected_account_id = request.GET.get('selected_account_id', '7')

        # Check if "end_date" is not provided or in an incorrect format
#        if not end_date:
 #           return JsonResponse({"error": "End date is required."}, status=400)

        try:
            # Create XML-RPC server proxies for common and models
            common = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/common')
            models = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/object')

            # Authenticate and get user ID
            uid = common.authenticate(odoo_db, odoo_username, odoo_password, {})

            # Call the getbalance method with date range parameters and the selected account ID
            balances = models.execute_kw(
                odoo_db,
                uid,
                odoo_password,
                'account.account',
                'getbalance',
                [start_date, end_date, selected_account_id],
                {}
            )

            # Initialize the total balance variable and response data list
            total_balance = 0.0
            response_data = []

            if not balances:
                return JsonResponse({"message": "No data available", "response": []})

            for balance in balances:
                response_data.append({
                    "account_id": balance['account_id'],
                    "account_name": balance['account_name'],
                    "root_id": balance['root_id'],
                    "date": balance['date'],
                    "balance": balance['balance']
                })

                # Add the balance to the total balance
                total_balance += balance['balance']

            # Return the response data as JSON along with the total balance
            return JsonResponse({
                "status": "success",
                "response": response_data,
                "total_balance": total_balance
            })

        # Handle exceptions if authentication or API calls fail
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

