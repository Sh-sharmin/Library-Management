from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book,Review
from Transactions.models import BorrowingTransaction
from .forms import ReviewForm
from django.views import View

# Create your views here

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_details.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        user_has_borrowed = False
        if self.request.user.is_authenticated:
            user_has_borrowed = BorrowingTransaction.objects.filter(
                user=self.request.user, book=book
            ).exists()

        context['user_has_borrowed'] = user_has_borrowed
        context['form'] = ReviewForm()
        return context


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        user = request.user

        if not BorrowingTransaction.objects.filter(user=user, book=book).exists():
            messages.error(request, "You must borrow this book before leaving a review.")
            return redirect('book_details', id=book.id)

        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(user=user, book=book, review=form.cleaned_data['review'])
            messages.success(request, "Your review has been submitted successfully!")

        return redirect('book_details', id=book.id)
