# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/3/6 01:15
from django.urls import path
from apps.goods.views import IndexView, ListView, HotGoodsView, SKUSearchView, DetailView, CategoryVisitCountView

urlpatterns = [
    path('index/', IndexView.as_view()),
    path('list/<int:category_id>/skus/', ListView.as_view()),
    path('hot/<int:category_id>/', HotGoodsView.as_view()),
    path('search/', SKUSearchView()),
    path('detail/<sku_id>/', DetailView.as_view()),
    path('detail/visit/<category_id>/', CategoryVisitCountView.as_view()),

]