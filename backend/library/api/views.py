from library.models import Book, Purchase ,Province
from .serializers import BookSerializers, PurchaseSerializer
from rest_framework.permissions import  IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView ,ListAPIView ,DestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status


class BookListView(ListAPIView):
    queryset = Book.objects.filter(available=True)  
    serializer_class = BookSerializers
    permission_classes = [IsAuthenticated]

    
class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class PurchaseBookView(CreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book = serializer.validated_data['book']
        user = self.request.user

        if user.location:
            user_point = user.location
            if user_point.srid != 4326:
                user_point.transform(4326)
            
            if not Province.objects.filter(
                ostn_name='تهران',
                geom__contains=user_point
            ).exists():
                raise ValidationError("User is not within Tehran boundary.")

        if user.credit < book.price:
            raise ValidationError("Insufficient credit.")

        user.credit -= book.price
        user.save()

        book.available = False
        book.save()

        serializer.save(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    
class ReturnBookView(DestroyAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        user = instance.user
        book = instance.book

        user.credit += book.price
        user.save()

        book.available = True
        book.save()

        instance.delete()
