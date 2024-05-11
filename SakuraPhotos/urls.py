"""
URL configuration for SakuraPhotos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# SakuraPhotos/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.paper import paperViews
from apps.user import userViews

# 创建一个DefaultRouter实例
router = DefaultRouter(trailing_slash=False)

# 注册路由




urlpatterns = [
    path('', include(router.urls)),  # 包含router的URLs
    path('api/paper/push_image', paperViews.PushImagesView.as_view(), name='pushImage'),
    # 获取图片40个
    path('api/paper/get_image', paperViews.GetImagesView.as_view(), name='getImage'),
    # 提升图片权重
    path('api/paper/up_weight', paperViews.UpWeightView.as_view(), name='up_weight'),
    # 获取热门图片
    path('api/paper/get_hots', paperViews.GetHotsView.as_view(), name='get_hots'),
    # 新建类型分类
    path('api/paper/up_sortInfo', paperViews.GetHotsView.as_view(), name='up_softInfo'),
    # 获取分类信息
    path('api/paper/get_sortInfo', paperViews.GetSortInfoView.as_view(), name='get_softInfo'),
    # 删除分类信息
    path('api/paper/delete_sortInfo', paperViews.DeleteSortInfo.as_view(), name='delete_softInfo'),
    #图片搜索
    path('api/paper/searching', paperViews.SearchingPaperView.as_view(), name='searching'),

    # 用户注册
    path('api/user/register/', userViews.RegisterView.as_view(), name='register'),

    path('api/user/login/',userViews.LoginView.as_view(),name='login'),
    # 邮箱激活
    path('sakura/activate/<uidb64>/<token>/', userViews.activate_account, name='activate'),

]
