# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/3/2 20:21
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from meiduo_mall import settings
from itsdangerous import BadData, BadSignature,SignatureExpired
# 加密
def generic_openid(openid):
    s = Serializer(settings.SECRET_KEY, expires_in=3600)
    access_token = s.dumps({'openid': openid})
    # 将bytes数据类型转换为str
    return access_token.decode()


# 解密
def check_access_token(access_token):
    s = Serializer(settings.SECRET_KEY, expires_in=3600)
    try:
        result = s.loads(access_token)
    except Exception:
        return None
    else:
        return result.get('openid')