# Create your views here.
# from django.contrib.admin.templatetags.admin_list import pagination
####################上传图片########################
# from fdfs_client.client import Fdfs_client
# # 1.创建客户端
# # 修改加载配置文件的路径
# client = Fdfs_client('utils/fastdfs/client.conf')
# # 2.上传图片
# client.upload_by_filename('apps/goods/123.png')
# # 3.获取file_id upload_by_filename 上传成功会返回字典数据

from django.views import View
from unicodedata import category

from utils.goods import get_categories
from apps.contents.models import ContentCategory
from django.shortcuts import render
class IndexView(View):
    def get(self, request):
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
        return render(request, 'index.html', context)

"""
 需求:
        根据点击的分类，获取分类数据（排序、分页）
 前端:
        前端发送一个axios请求 分类id 在路由中
        分页的页码（第几页数据）
 后端:
    请求:   接受参数
    业务逻辑:  根据需求查询数据，将对象数据转换为字典数据                        
    响应:     返回JSON
    
    路由 GET  /list/category_id/skus/
    
    步骤: 
        1.接受参数
        2.获取category_id
        3.根据分类idj进行分类数据的查询验证
        4.获取面包屑数据
        5.查询分类对应的sku数据，排序分页
        6.返回响应
"""



from django.http import JsonResponse
from utils.goods import get_breadcrumb
from apps.goods.models import SKU, GoodsCategory
class ListView(View):
    def get(self, request, category_id):
        # 1.接受参数
        # 排序字段
        ordering = request.GET.get('ordering')
        # 每页多少数据
        page_size = request.GET.get('page_size')
        # 要第几页数据
        page = request.GET.get('page')
        # 2.获取category_id
        # 3.根据分类idj进行分类数据的查询验证
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '参数缺失'})
        # 4.获取面包屑数据
        breadcrumb = get_breadcrumb(category)
        # 5.查询分类对应的sku数据，排序分页
        skus = SKU.objects.filter(category=category, is_launched=True).order_by(ordering)
        # 分页
        from django.core.paginator import Paginator
        # object_list 列表数据
        # per_page 每页多少数据
        paginator = Paginator(skus, per_page=page_size)
        # 获取指定页码的数据
        page_skus = paginator.page(page)
        sku_list = []
        # 将对象转换为字典
        for sku in page_skus.object_list:
            sku_list.append({
                'id':sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url':sku.default_image.url,

            })
        # 获取总页码
        total_num = paginator.num_pages
        # 6.返回响应
        return JsonResponse({'code': 0,
                             'errmsg': 'ok',
                            'list': sku_list,
                            'count': total_num,
                            'breadcrumb': breadcrumb,
                            })


# 商品热销排行
class HotGoodsView(View):
    """商品热销排行"""

    def get(self, request, category_id):
        """提供商品热销排行JSON数据"""
        # 根据销量倒序
        skus = SKU.objects.filter(category_id=category_id, is_launched=True).order_by('-sales')[:2]

        # 序列化
        hot_skus = []
        for sku in skus:
            hot_skus.append({
                'id':sku.id,
                'default_image_url':sku.default_image.url,
                'name':sku.name,
                'price':sku.price
            })

        return JsonResponse({'code':0, 'errmsg':'OK', 'hot_skus':hot_skus})

# Elasticsearch