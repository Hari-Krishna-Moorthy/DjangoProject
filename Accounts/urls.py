from django.urls import path

from Accounts.views import (
    loginView,
    logoutView,
    registerView,
    getUser,
)

urlpatterns = [
    path('login/', loginView, name='account-login'),
    path('logout/', logoutView, name='account-logout'),
    path('register/', registerView, name='account-register'),
    path('get-user/', getUser, name='get user')
]