import hashlib
import string

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    img_name = models.CharField(max_length=100)
    img_size = models.CharField(max_length=20)
    img_down_link = models.URLField(max_length=200)
    weight = models.IntegerField(default=1)
    sort = models.IntegerField(default=0)
    uploader = models.IntegerField(default=10000)


    def __str__(self):
        return self.img_name

    class Meta:
        app_label = 'paper'
class Sort(models.Model):
    id = models.AutoField(primary_key=True)
    sortName = models.CharField(max_length=10)
    firstPaper = models.CharField(max_length=100)

    def __str__(self):
        return self.sortName

    class Meta:
        app_label = 'paper'


from rest_framework.authtoken.models import Token
class SuperAdmin(AbstractUser):

    role = models.IntegerField(default=0)
    utoken = models.CharField(max_length=200, blank=True, null=True)  # 使用不同的字段名
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='superadmin_groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='superadmin_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    def generate_custom_auth_token(self):
        # 生成一个简单的认证令牌
        token, created = Token.objects.get_or_create(user=self)
        return token.key
    def set_password(self, raw_password):
        # 使用一个简单的加密方法，例如MD5
        encrypted_password = hashlib.md5(raw_password.encode()).hexdigest()
        self.password = encrypted_password

    def check_password(self, raw_password):
        # 使用相同的加密方法来验证密码
        encrypted_password = hashlib.md5(raw_password.encode()).hexdigest()
        return self.password == encrypted_password

        # 重写save方法以在创建用户时生成并设置自定义令牌

        def save(self, *args, **kwargs):
            if not self.pk:
                self.set_password(self.password)  # 使用自定义散列函数
                self.custom_auth_token = self.generate_custom_auth_token()
            super().save(*args, **kwargs)

        # 生成自定义令牌的方法


class PaperUser(AbstractUser):
    introduction = models.CharField(max_length=50, default='还没有个人介绍呢，快让别人来认识你吧!')
    account = models.IntegerField()
    is_vip = models.IntegerField(default=0)
    background_url = models.CharField(max_length=100, default='https://pic.netbian.com/uploads/allimg/240320/231320-17109476001a93.jpg')
    imgIcon = models.CharField(max_length=100, default='http://q1.qlogo.cn/g?b=qq&nk=2109714162&s=100')  # 头像
    gold = models.IntegerField(default=0)
    utoken = models.CharField(max_length=200, blank=True, null=True)
    review = models.ManyToManyField('Reviews', related_name='paperuser_review', blank=True)
    groups = models.ManyToManyField(Group, related_name='paperuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='paperuser_set', blank=True)
    def generate_custom_auth_token(self):
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)

    def save(self, *args, **kwargs):
        # 如果 account 字段没有被设置，则生成一个九位数的账号
        if not self.account:
            self.account = self._generate_account()
        super().save(*args, **kwargs)  # 调用父类的 save 方法来保存用户
        self.utoken = self.generate_custom_auth_token()  # 确保在保存后生成令牌

    def _generate_account(self):
        import random
        # 生成一个九位数的账号
        return ''.join(random.choices(string.digits, k=9))


class Reviews(models.Model):
    content = models.CharField(max_length=300,default='SakuraPhoto',null=True)
    reviewer = models.ForeignKey(PaperUser,on_delete=models.CASCADE,related_name='reviews')