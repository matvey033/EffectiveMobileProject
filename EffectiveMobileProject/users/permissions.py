from rest_framework.permissions import BasePermission
from .models import AccessRoleRule, BusinessElement


class RolePermission(BasePermission):
    def has_permission(self, request, view):
        element_name = getattr(view, "business_element", None)
        if not element_name:
            return False

        element = BusinessElement.objects.filter(name=element_name).first()
        if not element:
            return False

        user_role = request.user.role
        if not user_role:
            return False

        rule = AccessRoleRule.objects.filter(role=user_role, element=element).first()
        if not rule:
            return False

        return getattr(rule, "read_permission", False)
