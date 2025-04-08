# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/5 21:53

from django.urls import path
# from rest_framework_jwt.views import obtain_jwt_token
from apps.meiduo_admin.utils import meiduo_token
from apps.meiduo_admin.views import home, user, images, sku, permissions

urlpatterns = [
    path('authorizations/', meiduo_token),
    # 日活统计
    path('statistical/day_active/', home.DailyActiveAPIView.as_view()),
    # 日下单量统计
    path('statistical/day_orders/', home.DailyOrderCountAPIView.as_view()),
    # 月增用户统计
    path('statistical/month_increment/', home.MonthCountAPIView.as_view()),

    path('users/', user.UserAPIView.as_view()),
    # 获取新增中的sku展示
    path('skus/simple/', images.ImageSKUAPIView.as_view()),

    path('skus/categories/', sku.GoodsCategoryAPIView.as_view()),
    # sku获取spu数据
    path('goods/simple/', sku.SPUListAPIView.as_view()),
    # sku获取spu规格和规格选项
    path('goods/<spu_id>/specs/', sku.SPUSpecAPIView.as_view()),
    # 权限中获取ContentType 的数据
    path('permission/content_types/', permissions.ContentTypeListAPIView.as_view()),
    # 组中获取权限列表数据
    path('permission/simple/', permissions.GroupPermissionListAPIView.as_view()),

]

from rest_framework.routers import DefaultRouter
# 1.创建router实例
router = DefaultRouter()
# 2.设置路由
router.register(r'skus/images', images.ImageModelViewSet, basename='images')
# 3.添加到urlpatterns
urlpatterns += router.urls

#####################SKU#######################
router.register(r'skus', sku.SKUModelViewSet, basename='skus')
####################权限#########################
#注册路由
router.register(r'permission/perms', permissions.PermissionModelViewSet, basename='perms')
#################### 组 #########################
router.register(r'permission/groups', permissions.GroupModelViewSet, basename='groups')
#################### 普通管理员 #########################
router.register(r'permission/admins', permissions.AdminUserModelViewSet, basename='admins')
# 将router生成的路由追加到urlpatterns中
urlpatterns += router.urls
