from rest_framework.permissions import BasePermission
from .utils import verify_token  # ou depuis le bon fichier

class IsUserAuthenticated(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith("Bearer "):
            return False

        token = auth_header.split(" ")[1]
        result = verify_token(token)
        return result["authenticated"]

