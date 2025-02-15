from django.urls import path
from .views import BookListView, PurchaseBookView,BookCreateView, ReturnBookView ,GeoServerManagerView ,GeoServerDatastoreView ,GeoServerPublishLayerView  , GeoserverUploadRasterView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),  
    path('purchase/', PurchaseBookView.as_view(), name='purchase-book'),  
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('return/', ReturnBookView.as_view(), name='return-book'),
    path('geo-server/workspace/', GeoServerManagerView.as_view()),
    path('geo-server/datastore/', GeoServerDatastoreView.as_view(),),
    path('geo-server/publish-layer/', GeoServerPublishLayerView.as_view()),
    path('geo-server/upload-raster/', GeoserverUploadRasterView.as_view(), name='upload-raster'),  
]
