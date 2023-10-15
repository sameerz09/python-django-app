from django.http import JsonResponse
from django.views import View
import xmlrpc.client

def odoo_api(url, db, username, password, method, *args):
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    return models.execute_kw(db, uid, password, method, *args, {})

def fetch_balance213213123(account_id, url, db, username, password):
    try:
        # Set your Odoo server details

        # Get the account name
        account_data = odoo_api(url, db, username, password, 'account.account', 'read', [account_id, ['name']])
        account_name = account_data[0]['name']

        # Call the 'getbalance' method to fetch the general ledger data
        balances = odoo_api(url, db, username, password, 'account.account', 'general_ledger', ['2023-10-01', '2025-10-31', account_id])

        ledger_entries = []

        if isinstance(balances, list) and balances:
            for balance in balances:
                debit = balance['balance'] if balance['balance'] >= 0 else 0
                credit = abs(balance['balance']) if balance['balance'] < 0 else 0
                entry = {
                    "Account Name": account_name,  # Include the account name
                    "Date": balance['date'],
                    "Debit": debit,
                    "Credit": credit,
                    "Balance": balance['balance']
                }
                ledger_entries.append(entry)

        return ledger_entries

    except xmlrpc.client.Fault as err:
        return []  # Return an empty list for this account due to an XML-RPC fault
    except Exception as e:
        return []  # Return an empty list for this account due to other errors

class GeneralLedgerView23123(View):
    def get(self, request, account_number):
        # Define the account_id to fetch data for account number 6
        account_id = 6  # Modify this value to the desired account number

        # Set your Odoo server details
        url = 'http://127.0.0.1:9069'
        db = 'testkmnss'
        username = 'sameerz09@hotmail.com'
        password = 'Test@111'

        # Fetch the general ledger data
        ledger_entries = fetch_balance(account_id, url, db, username, password)

        # Return the general ledger data as a JSON response
        return JsonResponse({'general_ledger': ledger_entries})
