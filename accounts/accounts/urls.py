from django.urls import path
from .view import GetBalanceSumView
from .template_views import BalanceSumTemplateView
from .accounts_id_views import get_account_ids

urlpatterns = [
    # ... other URL patterns ...
    path('api/get-account-ids/', get_account_ids, name='get_account_ids'),
    path('test', BalanceSumTemplateView.as_view(), name='balance_sum_template'),
    path('api/get-balance-sum/', GetBalanceSumView.as_view(), name='get_balance_sum'),
]
