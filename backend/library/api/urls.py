from django.urls import path
from .views import BookListView, PurchaseBookView, ReturnBookView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),  # Endpoint for the list of available books
    path('purchase/', PurchaseBookView.as_view(), name='purchase-book'),  # Endpoint to purchase a book
    path('return/', ReturnBookView.as_view(), name='return-book'),  # Endpoint to return a book
]