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
    url = 'http://13.49.59.166:8069'
    db = 'KMNSS'
    username = 'sugam.pandey@gmail.com'
    password = 'sugam@kmnss!23#'
    uid, models = authenticate_odoo()  # Define models in this scope

    if uid is not None and models is not None:
        try:
            # Call the 'search_read' method on the 'account.account' model to retrieve account IDs
            account_ids = models.execute_kw(
                db,
                uid,
                password,
                'account.account',  # Replace with the actual module name
                'get_all_accounts',
                [],
            )

            if isinstance(account_ids, list):
                # Process each account ID
                for account_id in account_ids:
                    # Do something with the account ID, e.g., print it
                    print("Account ID:", account_id)

                # Return the account IDs as a JSON response
                return JsonResponse({'account_ids': account_ids})
            else:
                return JsonResponse({"error": "Invalid response from Odoo."}, status=500)

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"}, status=500)
    else:
        return JsonResponse({"error": "Authentication failed."}, status=500)    
