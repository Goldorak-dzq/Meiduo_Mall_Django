# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/3/27 17:11
# python manage.py generate_homepage

# from django.template.loader import render_to_string
# from meiduo_mall import settings
# import os
# from datetime import datetime
from django.core.management.base import BaseCommand
from utils.goods import get_categories
from apps.contents.models import ContentCategory
import time
class Command(BaseCommand):
    help = '每分钟生成首页静态文件'

    def handle(self, *args, ** options):

        print('----------%s-------------' % time.ctime())
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