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