# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/2/28 21:28
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
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