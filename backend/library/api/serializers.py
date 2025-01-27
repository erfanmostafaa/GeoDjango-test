from rest_framework import serializers
from library.models import Book ,Purchase

class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        feilds = ['title' , 'price' , ' author' , 'available']



class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'user', 'book', 'purchased_at']