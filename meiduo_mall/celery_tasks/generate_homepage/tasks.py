# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/3/27 17:48
from celery_tasks.main import app
from celery_tasks.generate_homepage.generate_static import generate_homepage  # 导入生成静态文件的具体函数

@app.task
def generate_homepage_static():
    try:
        result = generate_homepage()  # 调用生成函数
        return {"status": "success", "message": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}