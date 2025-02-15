from django.db import models
from Categories.models import Category 
from django.contrib.auth.models import User
from django.urls import reverse


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='books')

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'book_id': self.id})
    
    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'