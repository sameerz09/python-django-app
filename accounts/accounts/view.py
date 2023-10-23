import xmlrpc.client
from django.http import JsonResponse
from rest_framework.views import APIView

class GetBalanceSumView(APIView):
    def get(self, request):
        # Replace these with your Odoo server details
        odoo_url = 'http://13.49.59.166:8069'
        odoo_db = 'KMNSS'
        odoo_username = 'sugam.pandey@gmail.com'
        odoo_password = 'sugam@kmnss!23#'

        # Replace these with your target date range
        # start_date = request.GET.get('start_date', '2023-01-01')
        end_date = request.GET.get('end_date', '2023-10-01')
        selected_account_id = request.GET.get('selected_account_id', '7')

        try:
            # Create an XML-RPC server proxy for common
            common = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/common')

            # Authenticate and get user ID
            uid = common.authenticate(odoo_db, odoo_username, odoo_password, {})

            # Create an XML-RPC server proxy for models
            models = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/object')

            # Call the general_ledger_report method with date range parameters and the selected account ID
            balances = models.execute_kw(
                odoo_db,
                uid,
                odoo_password,
                'account.account',  # Replace with your actual module name
                'get_balance',
                [int(selected_account_id), end_date],
                {}
            )

            # Initialize the total balance variable and response data list
            total_balance = 0.0
            response_data = []

            if not balances:
                return JsonResponse({"message": "No data available", "response": []})


            # Get the name from account_info
            # if 'balance_report' in balances:
            #     name = balances['balance_report']['name']

                

            for balance in balances['balance_info']:
                response_entry = {
                    "date": balance['date'],
                    "balance": balance['balance'],
             
                }

                response_data.append(response_entry)

                # Add the balance to the total balance
                total_balance += balance.get('balance', 0)

            # Return the response data as JSON along with the total balance
            return JsonResponse({
                "status": "success",
                "response": response_data,
                "total_balance": total_balance
            })

        # Handle exceptions if authentication or API calls fail
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
