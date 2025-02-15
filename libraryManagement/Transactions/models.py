from django.db import models
from django.contrib.auth.models import User
from Users.models import CustomerAccount
from Books.models import Book
# Create your models here.

class DepositTransaction(models.Model):
    user = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE,related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)

    def __str__(self):
        return f"{self.user.user.username}"
    
class BorrowingTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    borrow_date = models.DateTimeField(auto_now_add=True)
    balance_after_borrow = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
