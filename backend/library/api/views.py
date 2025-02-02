from library.models import Book, Purchase ,Province
from .serializers import BookSerializers, PurchaseSerializer
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError




class BookListView(generics.ListAPIView):
    queryset = Book.objects.filter(available=True)  
    serializer_class = BookSerializers
    permission_classes = [permissions.IsAuthenticated]


class PurchaseBookView(generics.CreateAPIView):
    queryset = Purchase.objects.all()  
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        user = self.request.user

        if user.loction:
            user_point = user.location
            province = Province.objects.first()
            if not province.boundary.contains(user_point):
                     raise ValidationError("User is not within Tehran boundary.")

        if user.credit < book.price:
            raise serializer.ValidationError("Insufficient credit.")

        user.credit -= book.price
        user.save()

        book.available = False
        book.save()

        serializer.save(user=user)


class ReturnBookView(generics.DestroyAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        user = instance.user
        book = instance.book

        user.credit += book.price
        user.save()

        book.available = True
        book.save()

        instance.delete()
