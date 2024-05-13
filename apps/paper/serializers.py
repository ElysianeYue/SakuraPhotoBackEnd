from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail

from django.template.loader import render_to_string
from requests import Response

from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

class ImageSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'img_name', 'img_size', 'img_down_link', 'weight', 'sort', 'uploader', 'img_url']

    def get_img_url(self, obj):
        return obj.img_down_link   # 假设 img_down_link 已经是图片的 URL

class SortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sort
        fields = ['id', 'sortName', 'firstPaper']

class SuperAdminSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    def get_auth_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
              'refresh': str(refresh),
              'access': str(refresh.access_token),
         }

    class Meta:
        model = SuperAdmin
        fields = ['username', 'password', 'role', 'auth_token']

    def create(self, validated_data):
        # 在保存之前调用 set_password 方法来散列密码
         user = SuperAdmin.objects.create(**validated_data)
         user.set_password(validated_data['password'])
         user.save()
         return user

    def validate(self, attrs):
         # 这里可以添加额外的验证逻辑
         # 例如，确保用户名和密码匹配
         user = SuperAdmin.objects.filter(username=attrs['username']).first()
         if user and user.check_password(attrs['password']):
             return attrs
         raise serializers.ValidationError("Incorrect credentials.")

class PaperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperUser
        fields = ['id','username','introduction',  'is_vip', 'background_url', 'imgIcon', 'utoken']
        read_only_fields = ['id', 'utoken']  # utoken 字段在序列化时应该是只读的

    def create(self, validated_data):
        # 在创建用户时，您可以添加额外的逻辑，例如生成自定义令牌
        user = PaperUser.objects.create(**validated_data)
        user.set_password(user.password)  # 使用自定义散列函数
        user.utoken = user.generate_custom_auth_token()  # 生成自定义令牌
        user.save()
        return user

    def update(self, instance, validated_data):
        # 更新用户时，您可以添加额外的逻辑，例如更新自定义令牌
        instance.username = validated_data.get('username', instance.username)
        instance.introduction = validated_data.get('introduction', instance.introduction)
        instance.account = validated_data.get('account', instance.account)
        instance.is_vip = validated_data.get('is_vip', instance.is_vip)
        instance.background_url = validated_data.get('background_url', instance.background_url)
        instance.imgIcon = validated_data.get('imgIcon', instance.imgIcon)
        instance.set_password(instance.password)  # 使用自定义散列函数
        instance.utoken = instance.generate_custom_auth_token()  # 生成自定义令牌
        instance.save()
        return instance
from rest_framework import serializers
from django.utils.encoding import force_bytes
from django.utils.http import  urlsafe_base64_encode

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = PaperUser
        fields = ['email', 'password','username']



    def create(self, validated_data):
        from ..user.tokens import account_activation_token
        user = PaperUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username']
        )
        user.is_active = False

        user.save()

        # 生成激活令牌
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        # 发送激活邮件
        current_site = get_current_site(self.context.get('request'))
        subject = 'Activate Your Account'
        message = render_to_string('account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': uid,
            'token': token,
        })
        send_mail(
            subject,
            message,
            'SakuraTeam <3139282206@qq.com>',
            [user.email],
            fail_silently=False,
            html_message=message  # 如果你的邮件模板是 HTML 格式的，需要设置这个参数
        )

        return user


    # 3139282206@qq.com


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperUser
        fields = ['id','account','username', 'email', 'introduction', 'is_active','is_vip','gold','background_url','imgIcon']
