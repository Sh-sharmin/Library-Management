from django.urls import path
from .views import DepositCreateView ,ReturnBookView

urlpatterns = [
    path('deposit/', DepositCreateView.as_view(), name='deposit'),
    path('return/<int:pk>/', ReturnBookView.as_view(), name='return_book'),
]
