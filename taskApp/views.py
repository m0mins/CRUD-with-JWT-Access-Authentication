from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .models import UserRole,TodoItem
from taskApp.models import User,Document
#from .serializers import UserRoleSerializer,DocumentSerializer,UserSerializer,MyTokenObtainPairSerializer
from .serializers import UserRoleSerializer,TodoItemSerializer,TodoItemDetailsSerializer,UserSerializer,UserDetailsSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from .permissions import IsSuperOrAdminOrStaff,IsSuperUser
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
#from todoApp.custom_pagination import CustomPagination
# Create your views here.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .pagination import MyPageNumberPagination
paginator = MyPageNumberPagination()

from rest_framework_simplejwt.tokens import RefreshToken



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    access['email'] = user.email
    return {
        #'refresh': str(refresh),
        'access': str(access),
    }


#class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#    @classmethod
#    def get_token(cls, user):
#        print(f"#####################3faffa   {user}")
#        token = super().get_token(user)
#
#        token['role'] = user.role
#        token['email'] = user.email
#        print(f"##########***************###################***********{token}")
#
#        return token
#
#
#class MyTokenObtainPairView(TokenObtainPairView):
#    serializer_class = MyTokenObtainPairSerializer


class UserRegistrationAPIView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        role = data.get('role','is_user')


        try:
            user_role = UserRole.objects.get(role=role)
            user = User.objects._create_user(email=email, password=password, role=user_role)

            user.save()
            refresh=get_tokens_for_user(user)
            print(f"refresh token : {refresh}")
            #refresh = str(RefreshToken.for_user(user))
            return Response({'message': 'User registered successfully'})
        except UserRole.DoesNotExist:
            return Response(data={'error': 'Role does not exist'}, status=400)


        except Exception as e:
            return Response(data={'error': e.args}, status=500)
        
class UserLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        print(f"#############654656############## {request}")

        if user is not None:
            login(request, user)
            access = get_tokens_for_user(user)
            #refresh = RefreshToken.for_user(user)

            #access_token = str(refresh.access_token)
            return Response({
                'message': 'Login successful',
                'access token': access,
                })
           
        
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    

#using Generic -----Start----------------APIVIEW---------------------------Start---------------------------------------------

class TodoItemListCreate(generics.ListCreateAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = [IsAuthenticated,IsSuperOrAdminOrStaff]

    #pagination_class=CustomPagination

    #for filter
    #filter_backends=[SearchFilter]
    #search_fields=['title']

    def perform_create(self, serializer):
        token = self.request.auth
        email=token['email']
        obj = User.objects.filter(email=email).last()
        user_role=obj.role_id

        # Pass request to serializer's context
        serializer.save(created_by=obj)
#Retrive update and Delete
class TodoItemRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = [IsSuperOrAdminOrStaff]
#using Generic -----End----------------APIVIEW---------------------------End---------------------------------------------





#using APIVIEW -----Start----------------APIVIEW---------------------------Start---------------------------------------------
class TodoItemDetail(APIView):
    permission_classes = [IsAuthenticated, IsSuperOrAdminOrStaff]

    def post(self, request):
        data=request.data
        serializer = TodoItemSerializer(data=data)
        if serializer.is_valid():
            token = request.auth
            email = token['email']
            obj = User.objects.filter(email=email).last()
            serializer.save(created_by=obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def get(self, request):
        id=request.GET.get("id" or None)
        page=request.GET.get("page" or None)
        limit=request.GET.get("limit" or None)
        #query=TodoItem.objects.filter(id=id).last()
        if id:
            try:
                query = TodoItem.objects.get(id=id)
                #serializer = TodoItemSerializer(todo_item)
                serializer = TodoItemDetailsSerializer(query)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except TodoItem.DoesNotExist:
                #return Response({'Error':'status=status.HTTP_404_NOT_FOUND})
                    return JsonResponse({"status":status.HTTP_404_NOT_FOUND,"success":False,"message":"Data not found!", "results":{}})
        else:
            queryset = TodoItem.objects.all()
            count=len(queryset)
            result_page = paginator.paginate_queryset(queryset,request)
            if result_page is not None:
                serializer = TodoItemDetailsSerializer(result_page, many=True)
                #serializer = TodoItemSerializer(result_page, many=True)

                result = {
                    "status":status.HTTP_200_OK,
                    "success": True,
                    "message": "Visit record fetched successfully!",
                    "results": serializer.data,
                    "count": count,
                    "page":page,
                    "limit":limit,
                }
            
                return Response(result)

            else:
            
                return JsonResponse({"status":status.HTTP_404_NOT_FOUND,"success":False,"message":"Data not found!", "results":{}})
    def put(self, request, id=None):
        token = request.auth
        email = token['email']
        updated_by = User.objects.filter(email=email).last()
        try:
            query = TodoItem.objects.filter(pk=id).last()
        except TodoItem.DoesNotExist:
            return Response({'error': 'Todo item not found'}, status=status.HTTP_404_NOT_FOUND)                
        serializer = TodoItemDetailsSerializer(query, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=updated_by)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        id=request.GET.get("id" or None)
        try:
            query = TodoItem.objects.get(pk=id)
        except TodoItem.DoesNotExist:
            return Response({'error': 'Todo item not found'}, status=status.HTTP_404_NOT_FOUND)        
        query.delete()
        return Response({'message': 'Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
#using APIVIEW -----End----------------APIVIEW---------------------------End---------------------------------------------


class UserRoleUpdate(APIView):
    permission_classes = [IsAuthenticated, IsSuperUser]


    def put(self, request, id=None):
        token = request.auth
        email = token['email']
        updated_by = User.objects.filter(email=email).last()
        try:
            query = User.objects.filter(pk=id).last()

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)        

        serializer = UserDetailsSerializer(query, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=updated_by)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
