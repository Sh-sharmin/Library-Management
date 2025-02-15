from django.urls import path
from .views import BookDetailView ,AddReviewView
from Transactions.views import BorrowBookView 

urlpatterns = [
    path('details/<int:id>/',BookDetailView.as_view(),name='book_details'),
    path('borrow/<int:book_id>/', BorrowBookView.as_view(), name='borrow_book'),
    path('review/<int:book_id>/', AddReviewView.as_view(), name='add_review'),
]
