from django.urls import path
from django.contrib import admin
from django.urls import path, include
from .view import GetBalanceSumView
from .template_views import BalanceSumTemplateView
# from .template_login import LoginView
from . import login
from .accounts_id_views import get_account_ids
from django.contrib.auth import views as auth_views
# from .general_ledger_view import GeneralLedgerView
from .fetch_general_ledger_data import Reports
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # ... other URL patterns ...

    # Add the URL pattern for the admin panel

    path('admin/', admin.site.urls),
    path('login/', login.custom_login, name='custom_login'),
    path('api/get-account-ids/', login_required(get_account_ids), name='get_account_ids'),
    path('test/', BalanceSumTemplateView.as_view(), name='balance_sum_template'),
    path('logout/', login_required(auth_views.LogoutView.as_view(next_page='/login/')), name='logout'),
    path('api/get-balance-sum/', GetBalanceSumView.as_view(), name='get_balance_sum'),
    path('general_ledger/<int:account_number>/', Reports.as_view(), name='general_ledger'),
    # path('ledger/', GeneralView.as_view(), name='ledger'),
]
