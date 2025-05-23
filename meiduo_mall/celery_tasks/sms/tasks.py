# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/2/28 16:33
# 生产者--任务、函数
# 这个函数必须让celery的实例的task装饰器 装饰
# 需要celery自动检测指定包的任务
from libs.yuntongxun.sms import CCP
from celery_tasks.main import app

@app.task
def celery_send_sms_code(mobile, code):

    CCP().send_template_sms(mobile, [code, 5], 1)