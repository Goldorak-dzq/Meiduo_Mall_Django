# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/3/6 10:32

"""
您的自定义存储系统必须是 的子类 ：django.core.files.storage.Storage
Django 必须能够在没有任何参数的情况下实例化你的存储系统。 这意味着任何设置都应从 中获取：django.conf.settings
您的存储类必须实现 and 方法，以及适用于您的存储类的任何其他方法。看 有关这些方法的更多信息。
"""

from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from meiduo_mall import settings

@deconstructible
class MyStorage(Storage):
    # def __init__(self, fdfs_base_url=None):
    #     """
    #     构造方法，可以不带参数，也可以携带参数
    #     :param base_url: Storage的IP
    #     """
    #     self.fdfs_base_url = fdfs_base_url or settings.FDFS_BASE_URL

    def __init__(self, fdfs_base_url=None):
        self.fdfs_base_url = fdfs_base_url or settings.FDFS_BASE_URL

    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content):
        pass
    # def url(self, name):
    #     """
    #     返回name所指文件的绝对URL
    #     :param name: 要读取文件的引用:group1/M00/00/00/wKhnnlxw_gmAcoWmAAEXU5wmjPs35.jpeg
    #     :return: http://192.168.103.158:8888/group1/M00/00/00/wKhnnlxw_gmAcoWmAAEXU5wmjPs35.jpeg
    #     """
    #     # return 'http://192.168.103.158:8888/' + name
    #     # return 'http://image.meiduo.site:8888/' + name
    #     return self.fdfs_base_url + name
    # def exists(self, name):
    #     # 判断图片是否存在
    #     return False
    def url(self, name):
        # return f"{self.fdfs_base_url}{name}"
        return 'http://192.168.88.111:8888/' + name
        # return f"{settings.FDFS_BASE_URL}{name}"
