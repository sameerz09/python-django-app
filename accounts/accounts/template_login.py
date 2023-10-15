from django.shortcuts import render
from django.views import View

class LoginView(View):
    # template_name = 'accounts/balance_sum_template.html'  # The other template
    login_template_name = 'accounts/accounts/login.html'  # New custom login template

    def get(self, request):
        # Use the custom login template for the login page
        return render(request, self.login_template_name)
