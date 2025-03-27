# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/3/27 22:52
#!/usr/bin/env python

import sys
sys.path.insert(0, '../')  # base_dir

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings")

import django
django.setup()


from utils.goods import get_categories
from utils.goods import get_goods_specs
from utils.goods import get_breadcrumb
from apps.goods.models import SKU
def generic_detail_html(sku):
    # 查询商品频道分类
    categories = get_categories()
    # 查询面包屑导航
    breadcrumb = get_breadcrumb(sku.category)
    goods_specs = get_goods_specs(sku)
    # 渲染页面
    context = {
        'categories': categories,
        'breadcrumb': breadcrumb,
        'sku': sku,
        'specs': goods_specs
    }

    # 1.加载模板
    from django.template import loader
    detail_template = loader.get_template('detail.html')
    # 2.模板渲染
    detail_html_data = detail_template.render(context)
    # 3.写入到指定文件
    import os
    from meiduo_mall import settings
    file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'front_end_pc/goods/%s.html' % sku.id)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(detail_html_data)

    print(sku.id)

skus = SKU.objects.all()
for sku in skus:
    generic_detail_html(sku)