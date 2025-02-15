from django.contrib import admin
from .models import DepositTransaction,BorrowingTransaction
# Register your models here.
admin.site.register(DepositTransaction)
admin.site.register(BorrowingTransaction)