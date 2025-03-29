# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/3/29 23:48

"""
需求:
    登录的时候将cookie数据合并到redis
前端:

后端:
    请求: 登录的时候 获取cookie数据
    业务逻辑: 合并到redis中
    响应:
    步骤:
        1.读取cookie数据
        2.初始化一个字典 用于保存 sku_id,count
            初始化一个列表 用于保存选中的商品id
            初始化一个列表 用于保存未选中的商品id
        3.遍历cookie数据
        4.将字典数据,列表数据分别添加到redis
        5.删除cookie数据

cookie和redis数据有相同商品id 以cookie数据为主
cookie有数据 redis没有数据 全部以cookie数据为主
redist有数据 cookie没有 不动
"""
import pickle
import base64
from django_redis import get_redis_connection

def merge_cookie_to_redis(request, response):
    # 1.读取cookie数据
    cookie_carts = request.COOKIES.get('carts')
    if cookie_carts is not None:
        carts = pickle.loads(base64.b64decode(cookie_carts))
        # 2.初始化一个字典 用于保存 sku_id,count
        cookie_dict = {}
        #     初始化一个列表 用于保存选中的商品id
        selected_ids = []
        #     初始化一个列表 用于保存未选中的商品id
        unselected_ids = []
        # 3.遍历cookie数据
        for sku_id, count_selected_dict in carts.items():
            cookie_dict[sku_id] = count_selected_dict['count']
            if count_selected_dict['selected']:
                selected_ids.append(sku_id)
            else:
                unselected_ids.append(sku_id)
        # 4.将字典数据,列表数据分别添加到redis
        user = request.user
        redis_cli = get_redis_connection('carts')
        pipline = redis_cli.pipeline()
        pipline.hmset('carts_%s' % user.id, cookie_dict)
        if len(selected_ids) > 0:
            # *selected_ids对列表数据进行解包
            pipline.sadd('selected_%s' % user.id, *selected_ids)
        if len(unselected_ids) > 0:
            pipline.srem('selected_%s' % user.id, *unselected_ids)
        pipline.execute()
        # 5.删除cookie数据
        response.delete_cookie('carts')
    return response
