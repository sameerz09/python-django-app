# template_views.py
from django.shortcuts import render
from django.views import View
from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as drf_status
import requests

class BalanceSumTemplateView(View):
    # template_name = 'balance_sum_template.html'
    template_name = 'accounts/balance_sum_template.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # Handle the button click event (if needed)
        # You can call the GetBalanceSumView here if necessary
        # For example:
        # result = GetBalanceSumView.as_view()(request)
        # return result
        return render(request, self.template_name)
