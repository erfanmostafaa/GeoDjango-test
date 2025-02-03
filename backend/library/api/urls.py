from django.urls import path
from .views import BookListView, PurchaseBookView,BookCreateView, ReturnBookView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),  
    path('purchase/', PurchaseBookView.as_view(), name='purchase-book'),  
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('return/', ReturnBookView.as_view(), name='return-book'),
]