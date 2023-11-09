import xmlrpc.client
from django.http import JsonResponse
from rest_framework.views import APIView

class GetLedgerSumView(APIView):
    def get(self, request):
        # Replace these with your Odoo server details
        odoo_url = 'http://127.0.0.1:8069'
        odoo_db = 'testkmnss'
        odoo_username = 'sameerz09@hotmail.com'
        odoo_password = 'Test@111'

        # Replace these with your target date range
        start_date = request.GET.get('start_date', '2023-01-01')
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
                'general_ledger_report',
                [int(selected_account_id), start_date, end_date],
                {}
            )

            # Initialize the total balance variable and response data list
            total_balance = 0.0
            response_data = []

            if not balances:
                return JsonResponse({"message": "No data available", "response": []})

            # Get the name from account_info
            name = ''
            anlytic_name = ''
            anlytic_id = ''
            
            if 'account_info' in balances:
                name = balances['account_info']['name']

            # if 'analytic_account_info' in balances:
            #     anlytic_info = balances['analytic_account_info']
            #     anlytic_name = anlytic_info['name']
            #     anlytic_id = anlytic_info['id']

            for balance in balances['ledger_data']:
                response_entry = {
                    "account_root_id": balance['account_root_id'],

                    "debit": balance['debit'],
                    "credit": balance['credit'],
                    "date": balance['date'],
                    "analytic_account_amount": balance['analytic_account_amount'],
                    "analytic_account_name": balance['analytic_account_name'],
                    "partner_id": balance['partner_id'],
                    "partner_type": balance['partner_type'],
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
