# # -*-coding:utf-8-*-
# # @Author: DZQ
# # @Time:2025/3/7 14:28
# from fdfs_client.client import Fdfs_client  # 或者使用py3Fdfs的API
# import os
#
# # 配置FastDFS客户端
# client_conf = 'utils/fastdfs/client.conf'  # 根据实际路径修改
# storage_http_url = 'http://www.meiduo.site:8000/'  # Storage的HTTP访问地址
#
# # 初始化客户端
# client = Fdfs_client(client_conf)
#
# # 本地图片目录
# image_dir = '/var/fdfs/storage/data/'
#
# # 遍历目录并上传所有图片
# for filename in os.listdir(image_dir):
#     if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
#         file_path = os.path.join(image_dir, filename)
#         try:
#             # 上传图片到FastDFS
#             ret = client.upload_by_filename(file_path)
#             if ret['Status'] == 'Upload successed.':
#                 file_id = ret['Remote file_id']
#                 # 生成完整URL
#                 image_url = f"{storage_http_url}{file_id}"
#                 print(f"上传成功: {image_url}")
#                 # 可将image_url存入数据库或在网页中使用
#             else:
#                 print(f"上传失败: {filename}, 错误: {ret}")
#         except Exception as e:
#             print(f"上传异常: {filename}, 错误: {str(e)}")