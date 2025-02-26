# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/2/26 12:12

from django.urls import converters
class UsernameConverter:
    regex = '[a-zA-Z0-9_-]{5,20}'
    def to_python(self, value):
        return str(value)