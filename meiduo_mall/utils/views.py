# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/2/28 21:28
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.http import JsonResponse
# 方法1
# class LoginRequiredJsonMixin(AccessMixin):
#     """Verify that the current user is authenticated."""
#
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return JsonResponse({'code': 400, 'errmsg': '没有登录'})
#         return super().dispatch(request, *args, **kwargs)
# 方法2
class LoginRequiredJsonMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        return JsonResponse({'code': 400, 'errmsg': '没有登录'})

# fdfs 上传文件到fdfs中
# from fdfs_client.client import Fdfs_client
# client = Fdfs_client('utils/fastdfs/client.conf')
# client.upload_by_filename('C:/Users/Lenovo/Desktop/123.png')
# http://192.168.88.111:8888/group1/M00/00/00/wKhYb2fKcgyAPVV2AACN6fGHbw4623.png