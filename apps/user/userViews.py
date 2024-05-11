
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .tokens import account_activation_token

# Create your views here.

# 管理员后台登录
class SuperAdminLoginView(APIView):
    def post(self, request, *args, **kwargs):
         # 直接从请求中获取数据
         username = request.data.get('username')
         password = request.data.get('password')

         # 验证用户名和密码
         user = SuperAdmin.objects.filter(username=username).first()
         if user and user.check_password(password):
             # 登录成功，生成并返回自定义令牌
             user.custom_auth_token = user.generate_custom_auth_token()
             user.save()
             return Response({'custom_auth_token': user.custom_auth_token})
         else:
             return Response({'error': 'Incorrect credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.conf import settings



from ..paper.serializers import *
class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            if user:
                # 生成自定义认证令牌
                token = user.generate_custom_auth_token()
                return Response({'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import render

def activate_account(request, uidb64, token):
    try:
        uid = smart_str(urlsafe_base64_decode(uidb64))
        user = PaperUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, PaperUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'success.html')
    else:
        return render(request, 'failure.html')

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


    def post(self, request, *args, **kwargs):

        username = request.data.get('username')
        password = request.data.get('password')
        user = PaperUser.objects.filter(username=username).first()
        if user is not None:
            if user.is_active:
                    # 用户验证成功，可以生成令牌
                token = user.generate_custom_auth_token()
                serializer = UserSerializer(user)
                return Response({'data':serializer.data,'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User account is disabled.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':"User is not lunched"})

