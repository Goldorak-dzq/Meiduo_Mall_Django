# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/3/27 18:45
from django.core.management.base import BaseCommand
from utils.goods import get_categories
from apps.contents.models import ContentCategory
import time

# def generate_homepage():
#     print('----------%s-------------' % time.ctime())
#     # 商品分类数据
#     categories = get_categories()
#     # 广告数据
#     contents = {}
#     content_categories = ContentCategory.objects.all()
#     for cat in content_categories:
#         contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')
#     # 渲染模板的上下文
#     context = {
#         'categories': categories,
#         'contents': contents,
#     }
#     import os
#     # 1.加载渲染模板
#     from django.template import loader
#     index_template = loader.get_template('index.html')
#     # 2.把数据给模板
#     index_html = index_template.render(context)
#     # 3.把渲染好的HTML写入指定文件
#     from meiduo_mall import settings
#     file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'front_end_pc/index.html')
#     with open(file_path, 'w', encoding='utf-8') as f:
#         f.write(index_html)

import logging
import time
import os
from django.template import loader
from meiduo_mall import settings

# 获取日志器（需在settings.py中配置LOGGING）
logger = logging.getLogger("crontab")  # 建议在settings中配置名为"crontab"的日志器

def generate_homepage():
    try:
        logger.info(f"开始生成静态首页，当前时间：{time.ctime()}")

        # 商品分类数据
        categories = get_categories()
        logger.info("成功获取商品分类数据")

        # 广告数据
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')
        logger.info("广告数据查询完成")

        # 渲染模板的上下文
        context = {
            'categories': categories,
            'contents': contents,
        }

        # 加载模板
        index_template = loader.get_template('index.html')
        index_html = index_template.render(context)
        logger.info("模板渲染完成")

        # 写入文件
        file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'front_end_pc/index.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(index_html)
        logger.info(f"静态文件已写入路径：{file_path}")

    except Exception as e:
        logger.error("生成静态首页时发生异常", exc_info=True)  # 记录异常堆栈信息
        raise  # 抛出异常以便Celery捕获