# Create your views here.

####################上传图片########################
# from fdfs_client.client import Fdfs_client
# # 1.创建客户端
# # 修改加载配置文件的路径
# client = Fdfs_client('utils/fastdfs/client.conf')
# # 2.上传图片
# client.upload_by_filename('apps/goods/123.png')
# # 3.获取file_id upload_by_filename 上传成功会返回字典数据

from django.views import View
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
