from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .models import UserRole,TodoItem
from taskApp.models import User,Document
#from .serializers import UserRoleSerializer,DocumentSerializer,UserSerializer,MyTokenObtainPairSerializer
from .serializers import UserRoleSerializer,TodoItemSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from .permissions import IsAdminOrStaff
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
#from todoApp.custom_pagination import CustomPagination
# Create your views here.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

#class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#    @classmethod
#    def get_token(cls, user):
#        token = super().get_token(user)
#
#        # Add custom claims
#        token['email'] = user.email
#
#        return token
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    #refresh.access_token['email']=user.email
    access = refresh.access_token
    access['email'] = user.email
    #access['role'] = user.role
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
            #user_role, created = UserRole.objects.get_or_create(role=role)
            user = User.objects._create_user(email=email, password=password, role=user_role)

            #user = User.objects._create_user(email=email, password=password,role=user_role)
            user.save()
            refresh=get_tokens_for_user(user)
            print(f"refresh token : {refresh}")
            #refresh = str(RefreshToken.for_user(user))
            return Response({'message': 'User registered successfully'})
        #except UserRole.DoesNotExist:
            #return Response(data={'error': 'Role does not exist'}, status=400)

            #if created:
            #    return Response({'message': 'User registered successfully with a new role'})
            #else:
            #    return Response({'message': 'User registered successfully with existing role'})

        #except Exception as e:
        except Exception as e:
            return Response(data={'error': e.args}, status=500)

#Login


#class UserLoginAPIView(APIView):
#    def post(self, request):
#        email = request.data.get('email')
#        password = request.data.get('password')
#        user = authenticate(request, email=email, password=password)
#
#        if user is not None:
#            login(request, user)
#            refresh = RefreshToken.for_user(user)
#            # Here you're returning the access token as a string
#            # If you want to include the role and email, you can return the token itself
#            access_token = MyTokenObtainPairSerializer.get_token(user)
#            return Response({
#                'message': 'Login successful',
#                'access': str(access_token),  # No need to convert to string
#            })
#        else:
#            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

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
    

#Create and List 
#class DocumentListCreate(generics.ListCreateAPIView):
#    queryset = Document.objects.all()
#    serializer_class = DocumentSerializer
#    permission_classes = [IsAuthenticated,IsAdminOrStaff]
#
#    #pagination_class=CustomPagination
#
#    #for filter
#    #filter_backends=[SearchFilter]
#    #search_fields=['title']
#
#    def perform_create(self, serializer):
#        current_user = self.request
#        print(f"#############{current_user}****************")
#        user_role = User.objects.get(user=current_user)
#        print("#############################")
#        print(user_role)
#        print("#############################")
#
#        # Pass request to serializer's context
#        serializer.save(user=user_role)
#
#
#
#class UserRegistrationAPIView(APIView):
#    def post(self, request):
#        data = request.data
#        email = data.get('email')
#        password = data.get('password')
#        role = data.get('role','is_user')
#
#
#        try:
#            user_role = UserRole.objects.get(role=role)
#            user = User.objects._create_user(email=email, password=password, role=user_role)
#
#            user.save()
#            refresh = str(RefreshToken.for_user(user))
#            return Response({'message': 'User registered successfully'})
#
#
#        except Exception as e:
#            return Response(data={'error': e.args}, status=500)

#Create and List 
class TodoItemListCreate(generics.ListCreateAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = [IsAuthenticated,IsAdminOrStaff]

    #pagination_class=CustomPagination

    #for filter
    #filter_backends=[SearchFilter]
    #search_fields=['title']

    def perform_create(self, serializer):
        token = self.request.auth
        email=token['email']
        obj = User.objects.filter(email=email).last()
        user_role=obj.role_id
        print(obj)
        print(f"#############9999999999999999999999999999999999999999999999################ {user_role}")



        # Pass request to serializer's context
        serializer.save(created_by=obj)
#Retrive update and Delete
class TodoItemRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = [IsAdminOrStaff]
    