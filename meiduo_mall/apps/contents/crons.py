# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/3/27 00:38

"""
首页详细页面
先查询数据库的数据
后进行HTML页面的渲染
用户直接访问到应该数据查询 已经被渲染的HTML页面  （静态化）

"""
from utils.goods import get_categories
from apps.contents.models import ContentCategory
import time
# 渲染HTML页面， 然后将渲染的HTML写入指定文件
def generic_meiduo_index():
    print('----------%s-------------'%time.ctime())
    # 商品分类数据
    categories = get_categories()
    # 广告数据
    contents = {}
    content_categories = ContentCategory.objects.all()
    for cat in content_categories:
        contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

    # 渲染模板的上下文
    context = {
        'categories': categories,
        'contents': contents,
    }
    import os
    # 1.加载渲染模板
    from django.template import loader
    index_template = loader.get_template('index.html')
    # 2.把数据给模板
    index_html = index_template.render(context)
    # 3.把渲染好的HTML写入指定文件
    from meiduo_mall import settings
    file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'front_end_pc/index.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
