# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/2/28 16:27
# 配置信息 key = value
# 指定redis为我们的broker
broker_url = 'redis://192.168.88.111:6379/15'

from celery import Celery
from celery.schedules import crontab

app = Celery(
    'static_generator',
    broker='redis://node1:6379/0',  # Redis作为消息代理
    backend='redis://node1:6379/1'  # Redis存储结果
)

# 设置时区（避免UTC问题）
app.conf.timezone = 'Asia/Shanghai'
app.conf.enable_utc = False

# 定时任务配置（每分钟执行一次）
app.conf.beat_schedule = {
    'generate-homepage-every-minute': {
        'task': 'tasks.generate_homepage_static',
        'schedule': crontab(minute='*/1'),  # 每分钟触发[1,3,6](@ref)
        'args': ()  # 可传递参数，如文件路径
    }
}