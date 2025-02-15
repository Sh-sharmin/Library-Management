from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import SignupFrom
from Transactions.models import BorrowingTransaction
from Users.models import CustomerAccount

class UserSignUpView(FormView):
    form_class = SignupFrom
    template_name = 'signup.html'
    def get_success_url(self):
        return reverse_lazy('login')
    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Signup'
        return context
    
class UserLoginView(LoginView):
    template_name = 'signup.html'
    def get_success_url(self):
        return reverse_lazy('homepage')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context
    
class UserProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        account, created = CustomerAccount.objects.get_or_create(user=user)
        borrowed_books = BorrowingTransaction.objects.filter(user=user, returned=False)
        context['account'] = account
        context['borrowed_books'] = borrowed_books
        
        return context


