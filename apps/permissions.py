from rest_framework.permissions import DjangoModelPermissions


class CustomPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

  

    # def has_permission(self, request, view):
    #     user = request.user
    #     print(user.get_all_permissions())
    #     if user.is_staff:
    #         if user.has_perm('apps.view_product'):
    #             return True
    #         if user.has_perm('apps.change_product'):
    #             return True
    #         if user.has_perm('apps.delete_product'):
    #             return True
    #         if user.has_perm('apps.add_product'):
    #             return True
    #     else:
    #         return False                    
   
