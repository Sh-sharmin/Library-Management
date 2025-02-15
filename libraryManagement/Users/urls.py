from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', views.UserSignUpView.as_view(), name='signup'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(next_page = '/'), name='logout'),

    
]