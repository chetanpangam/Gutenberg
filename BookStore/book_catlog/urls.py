from django.urls import path
from . import views


app_name = "book_catlog"
urlpatterns = [
    path('books', views.BookCatalogView.as_view(), name='books')
]