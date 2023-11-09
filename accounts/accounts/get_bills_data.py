import xmlrpc.client
from django.http import JsonResponse
from django.views import View

class GetBillsView(View):
    def get(self, request):
        # Replace with your Odoo server details
        url = 'http://127.0.0.1:9069'
        db = 'testkmnss'
        username = 'sameerz09@hotmail.com'
        password = 'Test@111'

        # Define your search criteria variables
        start_date = request.GET.get('start_date', '2023-01-01')
        end_date = request.GET.get('end_date', '2023-10-01')
        selected_account_id = request.GET.get('selected_account_id', '7')
        selected_partner_id = request.GET.get('selected_partner_id', '7')
        selected_analytic_id = request.GET.get('selected_analytic_id', '1')
            # start_date = '2000-10-01'
        # end_date = '2100-10-31'

        try:
            # Connect to the Odoo server using the XML-RPC API
            common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
            uid = common.authenticate(db, username, password, {})

            if uid:
                # Create a new instance for the Odoo model
                models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

                # Define the search criteria to retrieve bill data
                # search_criteria = [
                #     ['date', '>=', start_date],
                #     ['date', '<=', end_date],
                # ]

                # Call the get_bills API on the Odoo server to retrieve bill data
                response = models.execute_kw(
                    db, uid, password,
                    'account.account',  # Replace with the actual Odoo model name
                    'get_bills',  # Name of the API method for retrieving bills
                    [start_date, end_date, selected_account_id, selected_partner_id, selected_analytic_id],
                {}  # Pass the search criteria as an argument
                )

                # Check if 'bill_info' exists in the response dictionary
                if 'bill_info' in response:
                    bill_info = response['bill_info']

                    # Initialize the total amount variable
                    total_amount = 0.0

                    # Iterate through bill information
                    for bill in bill_info:
                        print(f"Bill ID: {bill['id']}")
                        print(f"Bill Date: {bill['bill_date']}")
                        # print(f"Bill Date: {bill['selected_accounr_id']}")
                        print(f"Amount Total: {bill['amount']}")
                        # Add more bill details here as needed
                        print("")

                        # Add the amount to the total amount
                        total_amount += bill['amount']

                    # Print the total amount
                    print(f"Total Amount: {total_amount}")

                    # Return the bill information as JSON response
                    return JsonResponse({'bill_info': bill_info})

                else:
                    return JsonResponse({'error': 'No bill information found.'})

            else:
                return JsonResponse({'error': 'Login failed. Check your credentials or server URL.'})

        except xmlrpc.client.Fault as err:
            return JsonResponse({'error': f'XML-RPC Fault: {err}'})
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {e}'})
