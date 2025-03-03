# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/2/28 16:21
"""
生产者
    @app.task
    def celery_send_sms_code(mobile, code):
        CCP().send_template_sms(mobile, [code, 5], 1)

    app.autodiscover_tasks(['celery_tasks.sms'])
消费者
    celery -A proj worker -l info
    在虚拟环境下执行指令
    celery -A celery实例脚本路径 worker -l INFO (Linux)
    Windows不支持基于fork的多进程模式，需改用单进程池。启动Celery时添加--pool=solo参数：
    celery -A celery_tasks.main worker --pool=solo -l INFO (Windows)

队列 （中间人）
    # 2.设置broker
    app.config_from_object('celery_tasks.config')
    # 配置信息 key = value
    # 指定redis为我们的broker
    broker_url = 'redis://192.168.88.111:6379/15'

Celery
    # 1.设置django环境
    import os
    from celery import Celery

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings')
    # 1.创建celery实例
    # 参数1: main 设置脚本路径，脚本路径唯一
    app = Celery('celety_tasks')
"""
# 1.设置django环境
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings')
# 1.创建celery实例
# 参数1: main 设置脚本路径，脚本路径唯一
app = Celery('celety_tasks')

# 2.设置broker
app.config_from_object('celery_tasks.config')

# 3.让celery自动检测指定包的任务
# autodiscover_tasks参数为列表
# 列表中的元素是tasks的路径
app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])