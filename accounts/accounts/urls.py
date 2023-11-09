from django.urls import path
from django.contrib import admin
from django.urls import path, include
from .view import GetBalanceSumView
from .template_views import BalanceSumTemplateView
# from .template_login import LoginView
from . import login
from .accounts_id_views import get_account_ids
from .partners_id_views import get_partner_ids
from .get_anylitic_accounts import get_analytic_account_ids
from django.contrib.auth import views as auth_views
# from .general_ledger_view import GeneralLedgerView
from .fetch_general_ledger_data import GetLedgerSumView
from django.contrib.auth.decorators import login_required
from .  import create_bills_accounts
from .  import delete_bills_accounts
from . import delete_bill
from .get_bills_data import GetBillsView


# urlpatterns = [
#     # ... other URL patterns ...

#     # Add the URL pattern for the admin panel

#     path('admin/', admin.site.urls),
#     path('login/', login.custom_login, name='custom_login'),
#     path('api/get-account-ids/', login_required(get_account_ids), name='get_account_ids'),

#     path('test/', BalanceSumTemplateView.as_view(), name='balance_sum_template'),
#     path('logout/', login_required(auth_views.LogoutView.as_view(next_page='/login/')), name='logout'),
#     path('api/get-balance-sum/', GetBalanceSumView.as_view(), name='get_balance_sum'),
#     path('general_ledger/<int:account_number>/', GetBalanceSumView.as_view(), name='general_ledger'),
#     # path('ledger/', GeneralView.as_view(), name='ledger'),
# ]


urlpatterns = [
    # ... other URL patterns ...

    # Add the URL pattern for the admin panel

    path('admin/', admin.site.urls),
    path('login/', login.custom_login, name='custom_login'),
    path('api/get-account-ids/', login_required(get_account_ids), name='get_account_ids'),
    path('api/get-partner-ids/', login_required(get_partner_ids), name='get-partner-ids'),
    path('api/get-anylitic-ids/', login_required(get_analytic_account_ids), name='get-anylitic-ids'),
    path('test/', login_required(BalanceSumTemplateView.as_view()), name='balance_sum_template'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('api/get-balance-sum/', login_required(GetBalanceSumView.as_view()), name='get_balance_sum'),
    path('api/get-ledger-sum/', login_required(GetLedgerSumView.as_view()), name='get_balance_sum'),
    path('general_ledger/<int:account_number>/', login_required(GetLedgerSumView.as_view()), name='general_ledger'),
    path('create_bills/', login_required(create_bills_accounts.create_bills), name='create_bills'),
    # path('create_bills/', login_required(create_bills_accounts.create_bills), name='create_bills'),
    path('delete_bills/', login_required(delete_bills_accounts.delete_bills), name='delete_bills'),
    path('delete_bill/', login_required(delete_bill.delete_bill), name='delete_bill'),
    path('get_bills/', login_required(GetBillsView.as_view()), name='get_bills'),
    # path('ledger/', GeneralView.as_view(), name='ledger'),
]