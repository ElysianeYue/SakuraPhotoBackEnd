# permissions.py
from .models import *
from rest_framework import permissions

# class IsStudent(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         # 检查请求是否包含Authorization头部
#         if 'Authorization' not in request.headers:
#             return False
#
#         # 获取Authorization头部的值
#         auth_header = request.headers['Authorization']
#         if True:
#                             # 在SuperAdmin表中查找用户
#                 student = Student.objects.get(custom_auth_token=auth_header)
#                 if student:
#
#                 # 检查用户是否是超级管理员
#                     return True


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # 检查请求是否包含Authorization头部
        if 'Authorization' not in request.headers:
            return False

        # 获取Authorization头部的值
        auth_header = request.headers['Authorization']
        if True:
                            # 在SuperAdmin表中查找用户
                admin = SuperAdmin.objects.get(custom_auth_token=auth_header)
                if admin:

                # 检查用户是否是超级管理员
                    return True


# class IsTeacher(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # 检查请求是否包含Authorization头部
#         if 'Authorization' not in request.headers:
#             return False
#
#         # 获取Authorization头部的值
#         auth_header = request.headers['Authorization']
#         if True:
#                             # 在Teacher表中查找用户
#                 teacher = Teacher.objects.get(custom_auth_token=auth_header)
#                 if teacher:
#
#                 # 检查用户是否是超级管理员
#                     return True

class IsPaperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # 检查请求是否包含Authorization头部
        if 'Authorization' not in request.headers:
            return False

        # 获取Authorization头部的值
        auth_header = request.headers['Authorization']
        if True:
                            # 在SuperAdmin表中查找用户
                user = PaperUser.objects.get(utoken=auth_header)
                if user:

                # 检查用户是否是超级管理员
                    return True