from rest_framework import permissions
from taskApp.models import UserRole,User

class IsAdminOrStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            token=request.auth
            email=token['email']

            obj = User.objects.filter(email=email).last()
            user_role=obj.role

        except UserRole.DoesNotExist:
            return False

        #if request.user.is_superuser or (user_role.role == 'admin'):
        if user_role.role == 'is_superuser':
           return True
        elif user_role.role == 'is_admin':
           return request.method in ['POST', 'PUT', 'PATCH'] or request.method in permissions.SAFE_METHODS 
        elif user_role.role == 'is_staff':
           return request.method in ['PUT', 'PATCH'] or request.method in permissions.SAFE_METHODS 
         #Others can only read
        return request.method in permissions.SAFE_METHODS