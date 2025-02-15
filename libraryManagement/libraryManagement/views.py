from django.shortcuts import render
from Categories.models import Category
from Books.models import Book

def home(request):
    categories = Category.objects.all() 
    Category_filter = request.GET.get('cat')
    if Category_filter:
        books = Book.objects.filter(category__name=Category_filter)  
    else:
        books = Book.objects.all()
    return render(request, 'home.html', {'books': books, 'categories': categories})
