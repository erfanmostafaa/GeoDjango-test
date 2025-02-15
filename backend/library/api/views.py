from library.models import Book, Purchase ,Province
from .serializers import BookSerializers, PurchaseSerializer
from rest_framework.permissions import  IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView ,ListAPIView ,DestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from utils import GeoServerManager
from rest_framework.views import APIView



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




class GeoServerManagerView(APIView):


    def post(self , request, *args, **kwargs):
        workspacename = request.data.get('workspace_name')

        if not workspacename:
            raise ValidationError("Workspace name is  required.")
        
        geo_manager = GeoServerManager()
        try:
            geo_manager.create_workspace(workspacename)
            return Response ({"message": f"Workspace '{workspacename}' created or already existes"} , status=status.HTTP_201_CREATED)
        except Exception as e :
            return Response({"error" : str(e) } , status=status.HTTP_400_BAD_REQUEST)
        
    

class GeoServerDatastoreView(APIView):

    def post(self , request , *args, **kwargs):
        workspace_name = request.data.get('workspace_name')
        datastore_name = request.data.get('datastore_name')
        db_config = request.data.get('db_config')


        if not workspace_name  or not datastore_name or not db_config:
            raise ValidationError ("Workspace name, datastore name, and db_config are required.")
        

        geo_manager = GeoServerManager()
        try:
            geo_manager.create_postgis_datastore(workspace_name, datastore_name, db_config)
            return Response({"message": f"PostGIS datastore '{datastore_name}' created in workspace '{workspace_name}'."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        



class GeoServerPublishLayerView(APIView):

    def post(self , request , *args, **kwargs):
        workspace_name = request.data.get('workspace_name')
        datastore_name = request.data.get('datastore_name')
        layer_name = request.data.get('layer_name')

        if not workspace_name or not datastore_name or not layer_name:
            raise ValidationError("Workspace name, datastore name, and layer name are required.")

        geo_manager = GeoServerManager()
        try:
            geo_manager.publish_layer(workspace_name, datastore_name, layer_name)
            return Response({"message": f"Layer '{layer_name}' published in datastore '{datastore_name}'."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




class GeoserverUploadRasterView(APIView):
    def post(self, request, *args, **kwargs):
        workspace_name = request.data.get('workspace_name')
        raster_name = request.data.get('raster_name')
        raster_file = request.data.get('raster_file')


        if not workspace_name or not raster_file or not raster_name : 
            raise ValidationError ("Workspace name , raster name and raster file not required.")
        


        geo_manager = GeoServerManager()
        try :
            raster_file_path = geo_manager.upload_raster(workspace_name , raster_file , raster_name)

            geo_manager.publish_layer(workspace_name , raster_name , raster_file_path )

            return Response ({"message" : f"Raster'{raster_name}' uploaded and published in workspace '{workspace_name}'." }, status=status.HTTP_201_CREATED),
        
        except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)