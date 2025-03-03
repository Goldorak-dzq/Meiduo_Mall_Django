from django.db import models

# Create your models here.
from django.db import models
class Area(models.Model):
    """省市区"""
    name = models.CharField(max_length=20, verbose_name='名称')
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='subs',
        null=True, blank=True,
        verbose_name='上级行政区划'
    )
    # related_name 关联的模型名字，默认是关联模型类名小写_set  area_set
    # 可以通过related_name修改 ， 现在改为subs
    class Meta:
        db_table = 'tb_areas'
        verbose_name = '省市区'
        verbose_name_plural = '省市区'

    def __str__(self):
        return self.name

"""
1.查询省份信息
# select * from tb_areas where parent_id is NULL;
Area.objects.filter(parent=None) 
Area.objects.filter(parent__isnull=True)
2.查询市的信息
# select * from tb_areas where parent_id = 130000;
Area.objects.filter(parent_id=130000) # 省
Area.objects.filter(parent=130000) # 市

province = Area.objects.get(id=130000)
province.subs.all()
3.查询区县的信息
# select * from tb_areas where parent_id = 130600;
Area.objects.filter(parent_id=130600)
Area.objects.filter(parent=130600)
city = Area.objects.get(id=130600) # 市
city.subs.all() # 区县
"""