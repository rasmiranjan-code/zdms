# apps/accounts/urls.py  (updated)

from django.urls import path
from django.contrib.auth.views import LogoutView
from apps.accounts.views import RoleBasedLoginView, LandingPageView

app_name = 'accounts'

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing'),
    path('login/', RoleBasedLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]