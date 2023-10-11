from django.urls import path
from .view import GetBalanceSumView
from .template_views import BalanceSumTemplateView

urlpatterns = [
    # Other URL patterns can be placed here if you have any.
    
    # Define the URL pattern for the GetBalanceSumView
    path('test', BalanceSumTemplateView.as_view(), name='balance_sum_template'),
    path('api/get-balance-sum/', GetBalanceSumView.as_view(), name='get_balance_sum'),
]
