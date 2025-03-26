# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/3/8 15:28


"""
1.我们需要在模型对应的子应用中创建search_indexes.py文件方便haystack检索文件
2.索引必须继承自indexes.SearchIndex, indexes.Indexable
3. 必须定义一个字段document=True
    字段名起什么都可以 text为惯例
use_template=True 允许我们来单独设置文件来指定哪些字段进行检索
该文件应创建在模板文件下/search/indexes/子应用名目录/模型类名小写_text.txt

运作：
    我们应该让haystack将数据获取到给es生成索引
    在虚拟环境运行python manage.py rebuild_index
"""
from apps.goods.models import SKU
from haystack import indexes

class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)


    def get_model(self):
        """返回建立索引的模型类"""
        return SKU

    def index_queryset(self, using=None):
        # return SKU.objects.all()
        return self.get_model().objects.all()

