import xmlrpc.client
from django.http import JsonResponse

def authenticate_odoo():
    # Replace these with your Odoo server details
    url = 'http://127.0.0.1:9069'
    db = 'testkmnss'
    username = 'sameerz09@hotmail.com'
    password = 'Test@111'

    # Create XML-RPC server proxies for common and models with allow_none=True
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', allow_none=True)
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', allow_none=True)

    try:
        # Authenticate and get user ID
        uid = common.authenticate(db, username, password, {})
        return uid, models

    except xmlrpc.client.Fault as err:
        return None, None

def get_partner_ids(request):
    uid, models = authenticate_odoo()
    db = 'testkmnss'
    username = 'sameerz09@hotmail.com'
    password = 'Test@111'

    if uid is not None and models is not None:
        try:
            # Call the custom 'get_all_accounts' method on the 'account.account' model
            partner_data = models.execute_kw(
                db,
                uid,
                password,
                'account.account',  # Replace with the actual module name
                'get_all_partners',
                [],
            )

            if isinstance(partner_data, list):
                # Process each partner object
                for partner in partner_data:
                    # Do something with the account data
                    print("Partner ID:", partner['id'], "Partner Name:", partner['name'])

                # Return the partner data as a JSON response
                return JsonResponse({'partner_data': partner_data})
            else:
                return JsonResponse({"error": "Invalid response from Odoo."}, status=500)

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"}, status=500)
    else:
        return JsonResponse({"error": "Authentication failed."}, status=500)