"""MitdtermProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from MidtermApp import views

from rest_framework.routers import DefaultRouter

from MidtermApp.ViewSets import TransactionViewSet

from MidtermApp.views import CustomerListCreate, AddressListCreate, AccountListCreate
from MidtermApp.views import CustomerViewUpdate, AddressViewUpdate, AccountViewUpdate

router = DefaultRouter()
router.register('transaction_viewset', TransactionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.details, name='home'),
    url(r'^home/$', views.details, name='home'),
    re_path(r'^createCustomer/$', views.CreateCustomerView.as_view(), name='create'),
    path('editCustomer/<int:id>/',  views.EditCustomerView.as_view(), name='edit'),
    path('createAddress/<int:fk>/', views.createAddress, name='create_address'),
    path('editAddress/<int:id>/<int:fk>/', views.editAddress, name='edit_address'),
    path('createAccount/<int:fk>/', views.createAccount, name='create_account'),
    path('editAccount/<int:id>/<int:fk>/', views.editAccount, name='edit_account'),
    path('addTransaction/<int:fk>/',  views.AddTransactionView.as_view(), name='transaction'),
    url(r'^listCustomerREST/$', CustomerListCreate.as_view(), name='list_customer_REST'),
    url(r'^listAddressREST/$', AddressListCreate.as_view(), name='list_address_REST'),
    url(r'^listAccountREST/$', AccountListCreate.as_view(), name='list_account_REST'),
    path('updateCustomerREST/<int:pk>/', CustomerViewUpdate.as_view(), name='update_customer_REST'),
    path('updateAddressREST/<int:pk>/', AddressViewUpdate.as_view(), name='update_address_REST'),
    path('updateAccountREST/<int:pk>/', AccountViewUpdate.as_view(), name='update_account_REST')
]

# login urls
urlpatterns += [
    url(r'^login/$', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'password_reset_done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^password_change/$', auth_views.PasswordChangeView.as_view(), name='password_change')
]
urlpatterns += router.urls
