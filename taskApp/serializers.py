from rest_framework import serializers
from .models import TodoItem,UserRole,User

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        #read_only_fields = ['email']

    def to_representation(self, instance):

        try:
            get_user=instance.role
            print(f"###################Role *********************88 {get_user}")

            serializer = UserRoleSerializer(get_user)
            user_info = serializer.data
            role=user_info['role']
        except:
            role={}
        role_info = {
            "id": instance.id,
            "email": instance.email,
            "role": role,

        }
        return role_info



class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = '__all__'
        read_only_fields = ['created_by']
class TodoItemDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = '__all__'


    def to_representation(self, instance):

        try:
            get_user=instance.created_by
            serializer = UserSerializer(get_user)
            user_info = serializer.data
            created_by=user_info['email']
        except:
            created_by={}
        try:
            get_user=instance.updated_by
            serializer = UserSerializer(get_user)
            user_info = serializer.data
            updated_by=user_info['email']
        except:
            updated_by={}
        #try:

        #    get_business = '{product_base_url}ekkbaz/business_details/{b_id}'.format(product_base_url=product_base_url,b_id=str(instance.business))
        #    headers_value =self.context["headers_value"]
        #    header = {"authorization":headers_value}
        #    response = requests.get(get_business , headers=header)
#
        #    response_data= response.json()
#
        #    if response_data["success"] == True:
        #        business = response_data["results"]
        #    else:
        #        business = {}
        #except:
        #    business ={}
        #try:
        #    area_serializer = AreaSerializer(instance.area)
        #    area = area_serializer.data
        #except:
        #    area={}        
        #try:
        #    region_serializer = RegionSerializer(instance.region)
        #    region = region_serializer.data
        #except:
        #    region={}
        todos_info = {
            "id": instance.id,
            "title": instance.title,
            "description": instance.description,
            #"uploaded_file": instance.uploaded_file,
            "created_by": created_by,
            "updated_by": updated_by,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
            "delivery_date":instance.delivery_date,


        }
        return todos_info