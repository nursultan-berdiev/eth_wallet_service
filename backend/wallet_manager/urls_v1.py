from django.urls import path
from . import views

urlpatterns = [
    path('wallets/', views.WalletView.as_view(), name='wallets_v1'),
    path('transaction/', views.WalletTransactionCreateView.as_view(), name='transaction_v1'),
]
