from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import DepositTransaction, BorrowingTransaction,Book
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import DepositForm
from django.shortcuts import get_object_or_404, redirect
from Users.models import CustomerAccount
import uuid 
from django.views import View

class DepositCreateView(LoginRequiredMixin, CreateView):
    model = DepositTransaction
    form_class = DepositForm
    template_name = 'deposit.html'
    success_url = reverse_lazy('deposit')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user.account
        })
        return kwargs
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        user_account  = self.request.user.account
        user_account.balance += amount
        user_account.save(
            update_fields=[
                'balance'
            ]
        )
        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )

        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['balance'] = self.request.user.account.balance  # Pass balance to the template
        return context
    

class BorrowBookView(LoginRequiredMixin, CreateView):
    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        user = request.user
        account, created = CustomerAccount.objects.get_or_create(user=user)
        
        if account.balance < book.price:
            messages.error(request, "Insufficient balance to borrow this book.")
            return redirect('book_details', pk=book.pk)
        
        account.balance -= book.price
        account.save(update_fields=['balance'])

        BorrowingTransaction.objects.create(
            user=request.user,
            book=book,
            transaction_id=str(uuid.uuid4()),
            balance_after_borrow=account.balance,
        )

        messages.success(request, f"You successfully borrowed '{book.title}'!")
        return redirect('profile')
    

class ReturnBookView(View):
    def post(self, request, pk):
        transaction = get_object_or_404(BorrowingTransaction, id=pk, user=request.user, returned=False)
        account = CustomerAccount.objects.get(user=request.user)
        account.balance += transaction.book.price
        account.save()
        transaction.returned = True
        transaction.save()
        messages.success(request, f"You have successfully returned '{transaction.book.title}'. ${transaction.book.price} has been added back to your balance.")
        return redirect('profile')