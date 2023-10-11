from django.urls import path
from .view import GetBalanceSumView
from .template_views import BalanceSumTemplateView

urlpatterns = [
    # ... other URL patterns ...
    path('test', BalanceSumTemplateView.as_view(), name='balance_sum_template'),
    path('api/get-balance-sum/', GetBalanceSumView.as_view(), name='get_balance_sum'),
]
