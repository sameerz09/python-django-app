from django.http import JsonResponse
from django.views import View
import xmlrpc.client

def odoo_api(url, db, username, password, method, *args):
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    return models.execute_kw(db, uid, password, method, *args, {})

def fetch_balance(account_id, url, db, username, password, start_date, end_date):
    try:
        # Get the account name
        account_data = odoo_api(url, db, username, password, 'account.account', 'read', [account_id, ['name']])
        account_name = account_data[0]['name']

        # Call the 'getbalance' method to fetch the general ledger data
        balances = odoo_api(url, db, username, password, 'account.account', 'general_ledger', [start_date, end_date, account_id])

        ledger_entries = []

        if isinstance(balances, list) and balances:
            for balance in balances:
                debit = balance['balance'] if balance['balance'] >= 0 else 0
                credit = abs(balance['balance']) if balance['balance'] < 0 else 0
                entry = {
                    "Account Name": account_name,
                    "Date": balance['date'],
                    "Debit": debit,
                    "Credit": credit,
                    "Balance": balance['balance']
                }
                ledger_entries.append(entry)

        print(f'Account ID: {account_id}')
        print(f'Start Date: {start_date}')
        print(f'End Date: {end_date}')
        print("Ledger Entries:", ledger_entries)  # Print the ledger entries for debugging

        return ledger_entries

    except xmlrpc.client.Fault as err:
        return []  # Return an empty list for this account due to an XML-RPC fault
    except Exception as e:
        return []  # Return an empty list for this account due to other errors

class GeneralLedgerView(View):
    def get(self, request, account_id):
        # Set your Odoo server details
        url = 'http://127.0.0.1:9069'
        db = 'testkmnss'
        username = 'sameerz09@hotmail.com'
        password = 'Test@111'

        # Retrieve start_date and end_date from query parameters
        start_date = request.GET.get('start_date', '2020-10-01')
        end_date = request.GET.get('end_date', '2027-10-31')

        # Fetch the general ledger data
        ledger_entries = fetch_balance(account_id, url, db, username, password, start_date, end_date)

        # Return the general ledger data as a JSON response
        return JsonResponse({'general_ledger': ledger_entries})
