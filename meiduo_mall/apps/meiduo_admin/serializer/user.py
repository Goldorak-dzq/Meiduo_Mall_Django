# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/6 21:46
from rest_framework import serializers
from apps.users.models import User
class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'  # 偷懒
        fields = ['id', 'username', 'email', 'mobile', 'password']

        extra_kwargs = {
            'username': {
                'max_length': 20,
                'min_length': 5
            },
            'password': {
                'max_length': 20,
                'min_length': 8,
                'write_only': True

            },
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)