from django.shortcuts import render
from django.http import HttpResponse
import xmlrpc.client

def create_bills(request):
    # Odoo server URL and database name
    url = 'http://127.0.0.1:9069'
    db = 'testkmnss'
    username = 'sameerz09@hotmail.com'
    password = 'Test@111'
    bill_date = request.GET.get('bill_date', '2023-10-01')
    bill_date_due = request.GET.get('bill_date_due', '2023-10-01')
    selected_account_id = request.GET.get('selected_account_id', '1')
    selected_partner_id = request.GET.get('selected_partner_id', '7')
    selected_analytic_id = request.GET.get('selected_analytic_id', '1')

    price_unit = request.GET.get('move_amount')

  

    # Connect to the Odoo server using the XML-RPC API
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})

    if uid:
        # Create a new instance for the Odoo model
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

        # Define the bill data (as a list of dictionaries)
        bill_data = [
            {
                'bill_number': 'INV020',
                'bill_date': bill_date,
                'bill_date_due': bill_date_due,
                'supplier_id': selected_partner_id,  # Replace with the actual supplier ID
                'amount1': 6040.00,
                'amount2': 20.00,
                'price_unit': price_unit,
                'account_id': selected_account_id,
                'selected_analytic_id': selected_analytic_id,
                # Add more fields as needed
            },
            # Add more bill data as necessary
        ]

        try:
            # Call the create_bills API on the Odoo server
            response = models.execute_kw(
                db, uid, password,
                'account.account',  # Updated to use 'account.account' as the Odoo model
                'create_bills',  # Name of the API method
                [bill_data]  # Pass the bill data as an argument
            )

            return HttpResponse(f"Response from Odoo API: {response}")

        except xmlrpc.client.Fault as err:
            return HttpResponse(f"XML-RPC Fault: {err}")

        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")

    else:
        return HttpResponse("Login failed. Check your credentials or server URL.")
