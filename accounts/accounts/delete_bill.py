import xmlrpc.client
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def delete_bill(request):
    if request.method == 'POST':
        try:
            # Connect to your Odoo instance using XML-RPC
            url = 'http://127.0.0.1:9069/xmlrpc/2/common'
            db = 'testkmnss'
            username = 'sameerz09@hotmail.com'
            password = 'Test@111'

            common = xmlrpc.client.ServerProxy(url)
            uid = common.authenticate(db, username, password, {})

            if uid:
                # Now, call the delete_bill method on your Odoo model
                models = xmlrpc.client.ServerProxy('http://127.0.0.1:9069/xmlrpc/2/object')
                bill_id = int(request.POST.get('bill_id'))
                result = models.execute_kw(db, uid, password, 'account.account', 'delete_bill', [bill_id])

                # Process the result from the Odoo server
                if isinstance(result, str):
                    return JsonResponse({'message': result})
                else:
                    return JsonResponse({'message': 'Bill deleted successfully.'})
            else:
                return JsonResponse({'message': 'Authentication failed.'})

        except Exception as e:
            return JsonResponse({'message': f'An error occurred: {str(e)}'})

    else:
        return JsonResponse({'message': 'Invalid request method. Use POST.'})
