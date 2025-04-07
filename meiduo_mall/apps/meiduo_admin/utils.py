# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/6 18:33
def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'id': user.id,
        'username': user.username
    }

from rest_framework_jwt.serializers import JSONWebTokenSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class MeiduoTokenSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
                if not user.is_staff:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)

from rest_framework_jwt.views import JSONWebTokenAPIView
class MeiduoObtainJSONWebToken(JSONWebTokenAPIView):

    serializer_class = MeiduoTokenSerializer

meiduo_token = MeiduoObtainJSONWebToken.as_view()

# 分页

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
class PageNum(PageNumberPagination):
    # 开启分页 设置默认每页多少条记录
    page_size = 5
    # 每页多少条记录的key，可以通过传递的参数传递
    page_size_query_param = 'pagesize'
    # 一页中最多有多少条记录
    max_page_size = 20
    def get_paginated_response(self, data):
        # raise NotImplementedError('get_paginated_response() must be implemented.')
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('lists', data),  # 结果列表
            ('page', self.page.number),  # 第几页
            ('pages', self.page.paginator.num_pages),  # 总共几页
            ('pagesize', self.page.paginator.per_page),  # 动态  一页多少条记录
        ]))