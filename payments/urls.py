from django.urls import path

from .views import (
    C2BValidationView,
    C2BConfirmationView, 
    RegisterMpesaCallBackUrlsView, 
    SimulateC2BTransactionView, 
    StkPushApiView,
    StkPushWebHookView
)

urlpatterns = [
    path('c2b_validation', C2BValidationView.as_view(), name="c2b_validation"),
    path('c2b_confirmation', C2BConfirmationView.as_view(), name="c2b_validation"),
    path('register_mpesa_callbackurls', RegisterMpesaCallBackUrlsView.as_view(), name="c2b_validation"),
    path('simulate_c2b_transaction', SimulateC2BTransactionView.as_view(), name="c2b_transaction_simulate"),
    path('stk_push', StkPushApiView.as_view(), name="stk_push_process"),
    path('stk_push_webhook', StkPushWebHookView.as_view(), name="stk_push_process"),


]