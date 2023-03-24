from django.urls import path

from .views import C2BValidationView, C2BConfirmationView

urlpatterns = [
    path('c2b_validation', C2BValidationView.as_view(), name="c2b_validation"),
    path('c2b_confirmation', C2BConfirmationView.as_view(), name="c2b_validation")
]