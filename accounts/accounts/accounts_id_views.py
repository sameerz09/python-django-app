import xmlrpc.client
from django.http import JsonResponse

def authenticate_odoo():
    # Replace these with your Odoo server details
    url = 'http://13.49.59.166:8069'
    db = 'KMNSS'
    username = 'sugam.pandey@gmail.com'
    password = 'sugam@kmnss!23#'

    # Create XML-RPC server proxies for common and models with allow_none=True
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', allow_none=True)
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', allow_none=True)

    try:
        # Authenticate and get user ID
        uid = common.authenticate(db, username, password, {})
        return uid, models

    except xmlrpc.client.Fault as err:
        return None, None

def get_account_ids(request):
    uid, models = authenticate_odoo()
    db = 'KMNSS'
    username = 'sugam.pandey@gmail.com'
    password = 'sugam@kmnss!23#'

    if uid is not None and models is not None:
        try:
            # Call the custom 'get_all_accounts' method on the 'account.account' model
            account_data = models.execute_kw(
                db,
                uid,
                password,
                'account.account',  # Replace with the actual module name
                'get_all_accounts',
                [],
            )

            if isinstance(account_data, list):
                # Process each account object
                for account in account_data:
                    # Do something with the account data
                    print("Account ID:", account['id'], "Account Name:", account['name'])

                # Return the account data as a JSON response
                return JsonResponse({'account_data': account_data})
            else:
                return JsonResponse({"error": "Invalid response from Odoo."}, status=500)

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"}, status=500)
    else:
        return JsonResponse({"error": "Authentication failed."}, status=500)
