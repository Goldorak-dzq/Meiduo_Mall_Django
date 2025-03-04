# Create your views here.

"""
判断用户名是否重复的功能
前端: 当用户输入用户名之后，失去焦点，发生一个axios(ajax)请求
后端: 
    请求: 接受用户名
    业务逻辑:  根据用户名查询数据库,result=0 没有注册，result=0 有注册
    响应: JSON
    路由:GET  /usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/
    步骤:1.接受用户名
    2.根据用户名查询数据库
    3.返回响应
"""
import re
import json

from django.views import View
from apps.users.models import User
from django.http import JsonResponse

class UsernameCountView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})

"""
注册
步骤:1. 接受请求
    2. 获取数据
    3. 验证数据
        3.1 用户名，密码，确认密码，手机号，是否同意协议 都要有
        3.2 用户名满足规则，用户名不能重复
        3.3 密码满足规则
        3.4 确认密码与密码一致
        3.5 手机号满足规则，同时不能重复
        3.6 需要同意协议
    4. 数据入库
    5. 返回响应
"""
class RegisterView(View):
    def post(self, request):
        #     1. 接受请求
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)
        #     2. 获取数据
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        allow = body_dict.get('allow')
        # sms_code = body_dict.get('sms_code')
        allow = body_dict.get('allow')
        #     3. 验证数据
        #         3.1 用户名，密码，确认密码，手机号，是否同意协议 都要有
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        #         3.2 用户名满足规则，用户名不能重复
        if not re.match('[a-zA-Z0-9_-]{5,20}', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名不满足规则'})
        #         3.3 密码满足规则
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': 'password格式有误!'})
        #         3.4 确认密码与密码一致
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次输入不对!'})
        #         3.5 手机号满足规则，同时不能重复
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': 'mobile格式有误!'})
        #         3.6 需要同意协议
        if allow != True:
            return JsonResponse({'code': 400, 'errmsg': 'allow格式有误!'})
        #     4. 数据入库
        # user = User(username=username, password=password, mobile=mobile, sms_code=sms_code)
        # user.save()
        # User.objects.create(username=username, password=password, mobile=mobile) # 不加密
        # 密码加密
        # user = User.objects.create_user(username=username, password=password, mobile=mobile)
        from django.contrib.auth import login
        try:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            mobile=mobile)
        except Exception:
            return JsonResponse({'code': 400, 'errmsg': '注册失败!'})
        login(request, user)
        #     5. 返回响应
        return JsonResponse({'code': 0, 'errmsg': '注册成功'})

"""
如果需求是注册成功后即表示用户认证通过，那么此时可以在注册成功后实现状态保持 (注册成功即已登录)
如果需求是注册成功后不表示用户认证通过，那么此时不用在注册成功后实现状态保持 (注册成功，单独登录)
实现状态保持主要有两种方式:
    客户端存储信息用Cookie
    服务器存储信息用Session
"""

"""  
登录

前端:
    当用户名把用户名和密码输入完成之后，点击登录按钮，这时候前端应该发送一个axios请求
后端:
    请求:   接受数据，验证数据
    业务逻辑: 验证用户名和密码是否正确 session
    响应: 返回JSON数据 0 成功 400 失败
步骤:
    1.接受数据
    2.验证数据
    3.验证用户名和密码是否正确
    4.session
    5.判断是否记住登录
    6.返回响应
"""

class LoginView(View):
    def post(self, request):
        # 1.接受数据
        # body_bytes = request.body
        # body_str = body_bytes.decode()
        # body_dict = json.loads(body_str)
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered')
        # 2.验证数据
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        # 确定根据手机号查询还是根据用户名查询
        if re.match('^1[3-9]\d{9}$', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'

        # 3.验证用户名和密码是否正确
        # User.objects.get(username=username)
        from django.contrib.auth import authenticate, login
        # authenticate传递用户名和密码
        # 如果正确，则返回User信息
        # 如果不正确，则返回None
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})
        # 4.session
        login(request, user)
        # 5.判断是否记住登录
        if remembered:
            # 记住登录 2周
            request.session.set_expiry(None)
        else:
            # 不记住密码，浏览器关闭session过期
            request.session.set_expiry(0)

        # 6.返回响应
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        # 首页显示用户信息，添加cookie信息
        response.set_cookie('username', user.username)
        return response

"""
退出登录

前端:
    当用户名点击退出按钮之后，前端应该发送一个axios delete请求
后端:
    请求:   接受数据，验证数据
    业务逻辑: 退出
    响应: 返回JSON数据 

"""
from django.contrib.auth import logout
class LogoutView(View):
    def delete(self, request):
        logout(request)
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        # 删除cookie信息
        response.delete_cookie('username')
        return response

"""
判断用户是否登录
用户中心也必须是登录用户
LoginRequiredMixin 未登录的用户 会返回重定向 重定向并不是JSON数据
需要返回JSON数据
"""
from utils.views import LoginRequiredJsonMixin
class CenterView(LoginRequiredJsonMixin, View):
    def get(self, request):
        # request.user 已经登录的用户信息
        # request.user 来源于中间件
        # 系统会判断，如果是登录用户，可以获取登录用户对应的模型实例数据
        # 如果不是登录用户，request.user = AnonymousUser() 匿名用户
        info_data = {
            'username': request.user.username,
            'email': request.user.email,
            'mobile': request.user.mobile,
            'email_active': request.user.email_active,
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'info_data': info_data})


"""
1.保存邮件地址 2.发送一封激活邮件 3.用户激活邮件

前端:
    当用户名输入邮箱之后，前端应该发送一个axios请求
后端:
    请求:   接受数据，获取数据
    业务逻辑: 保存邮件地址，发送一封激活邮件
    响应: 返回JSON数据
    路由: PUT
    步骤:
        1.接受请求
        2.保存数据
        3.保存邮箱地址
        4.发送一封激活邮件
        5.返回响应

"""

class EmailView(LoginRequiredJsonMixin, View):
    def put(self, request):
        # 1.接受请求
        data = json.loads(request.body.decode())
        # 2.保存数据
        email = data.get('email')
        # 验证数据
        if not email:
            return JsonResponse({'code': 400, 'errmsg': '缺少email参数'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({'code': 400, 'errmsg': 'email格式不正确'})

        # 3.保存邮箱地址
        user = request.user
        user.email = email
        user.save()

        # 4.发送一封激活邮件
        # from django.core.mail import send_mail
        subject = '美多商城激活邮件'  # 主题
        message = ""      # 邮件内容
        from_email = '美多商城<dzq1780315381@163.com>'       # 发件人
        recipient_list = ['1780315381@qq.com', 'dzq1780315381@163.com']  # 收件人列表
        # 邮件的内容如果是html 使用html_message
        # 4.1 对a标签的内容进行加密处理
        from apps.users.utils import generic_email_verify_token
        token = generic_email_verify_token(request.user.id)
        # 4.2 组织我们的激活邮件
        # html_message = "点击按钮激活<a href='http://www.baidu.com/?token=%s'>激活</a>"%token
        # send_mail(
        #     subject=subject,
        #     message=message,
        #     from_email=from_email,
        #     recipient_list=recipient_list,
        #     html_message=html_message,
        # )
        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=%s' % token
        html_message = '<p>尊敬的用户您好！</p>' \
                       '<p>感谢您使用美多商城。</p>' \
                       '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                       '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)
        # celery异步
        from celery_tasks.email.tasks import celery_send_email
        celery_send_email.delay(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
        )
        # 5.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})

"""
激活用户邮件

前端:
    当用户名点击激活链接，激活链接携带了token
后端:
    请求:   接受请求，获取参数，验证参数
    业务逻辑: user_id 根据用id查询数据，修改数据
    响应: 返回响应JSON
    路由: PUT emails/verifications/ token没有在body
    步骤:
        1.接受请求
        2.获取参数
        3.验证参数
        4.获取user_id
        5.根据用id查询数据
        6.修改数据
        7.返回响应JSON

"""
class EmailVerifyView(View):
    def put(self, request):
        # 1.接受请求
        params = request.GET
        # 2.获取参数
        token = params.get('token')
        print(f"Token: {token}")
        # 3.验证参数
        if token is None:
            return JsonResponse({'code': 400, 'errmsg': '参数缺失'})
        # 4.获取user_id
        from apps.users.utils import check_verify_token
        user_id = check_verify_token(token)
        if user_id is None:
            return JsonResponse({'code': 400, 'errmsg': '参数缺失'})
        # 5.根据用户id查询数据
        user = User.objects.get(id=user_id)
        # 6.修改数据
        user.email_active = True
        user.save()
        # 7.返回响应JSON
        return JsonResponse({'code': 0, 'errmsg': 'ok'})

"""
新增地址

前端:
    当用户完成地址信息之后，前端应该发送一个axios请求 携带相关信息
后端:
    请求:   接受请求，获取参数，验证参数
    业务逻辑: 数据入库
    响应: 返回响应JSON
    路由: POST /addresses/create/
    步骤:
        1.接受请求
        2.获取参数，验证参数
        3.数据入库
        4.返回响应JSON

"""

from apps.users.models import Address
class AddressCreateView(LoginRequiredJsonMixin, View):
    def post(self, request):
        # 1.接受请求
        data = json.loads(request.body.decode())
        # 2.获取参数，验证参数
        receiver = data.get('receiver')
        province_id = data.get('province_id')
        city_id = data.get('city_id')
        district_id = data.get('district_id')
        place = data.get('place')
        mobile = data.get('mobile')
        tel = data.get('tel')
        email = data.get('email')
        user = request.user
        # 数据检验
        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '参数mobile有误'})
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return JsonResponse({'code': 400, 'errmsg': '参数tel有误'})
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return JsonResponse({'code': 400, 'errmsg': '参数email有误'})
        # 3.数据入库
        address = Address.objects.create(
            user=user,
            title=receiver,
            receiver=receiver,
            province_id=province_id,
            city_id=city_id,
            district_id=district_id,
            place=place,
            mobile=mobile,
            tel=tel,
            email=email,
        )
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email,
        }
        # 4.返回响应JSON
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'address': address_dict})


# 展示地址
class AddressView(LoginRequiredJsonMixin, View):
    def get(self, request):
        # 1.查询指定数据
        user = request.user
        # addresses = user.address
        addresses = Address.objects.filter(user=user, is_deleted=False)
        # 2.将对象数据转换为字典数据
        address_list = []
        for address in addresses:
            address_list.append({
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            })

        # 3.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'addresses': address_list})

# 修改地址
class UpdateDestroyAddressView(LoginRequiredJsonMixin, View):
    """修改和删除地址"""

    def put(self, request, address_id):
        """修改地址"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})


        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '参数mobile有误'})

        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return JsonResponse({'code': 400, 'errmsg': '参数tel有误'})
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return JsonResponse({'code': 400, 'errmsg': '参数email有误'})

        # 判断地址是否存在,并更新地址信息
        try:
            Address.objects.filter(id=address_id).update(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )
        except Exception:
            return JsonResponse({'code': 400, 'errmsg': '更新地址失败'})

        # 构造响应数据
        address = Address.objects.get(id=address_id)
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        # 响应更新地址结果
        return JsonResponse({'code': 0, 'errmsg': '更新地址成功', 'address': address_dict})

    # 删除地址
    def delete(self, request, address_id):
        """删除地址"""
        try:
            # 查询要删除的地址
            address = Address.objects.get(id=address_id)

            # 将地址逻辑删除设置为True
            address.is_deleted = True
            address.save()
        except Exception:
            return JsonResponse({'code': 400, 'errmsg': '删除地址失败'})

        # 响应删除地址结果
        return JsonResponse({'code': 0, 'errmsg': '删除地址成功'})

# 设置默认地址
class DefaultAddressView(LoginRequiredJsonMixin, View):
    """设置默认地址"""

    def put(self, request, address_id):
        """设置默认地址"""
        try:
            # 接收参数,查询地址
            address = Address.objects.get(id=address_id)

            # 设置地址为默认地址
            request.user.default_address = address
            request.user.save()
        except Exception:
            return JsonResponse({'code': 400, 'errmsg': '设置默认地址失败'})

        # 响应设置默认地址结果
        return JsonResponse({'code': 0, 'errmsg': '设置默认地址成功'})


# 修改地址标题
class UpdateTitleAddressView(LoginRequiredJsonMixin, View):
    """设置地址标题"""

    def put(self, request, address_id):
        """设置地址标题"""
        # 接收参数：地址标题
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')

        try:
            # 查询地址
            address = Address.objects.get(id=address_id)

            # 设置新的地址标题
            address.title = title
            address.save()
        except Exception:
            return JsonResponse({'code': 400, 'errmsg': '设置地址标题失败'})

        # 4.响应删除地址结果
        return JsonResponse({'code': 0, 'errmsg': '设置地址标题成功'})

# 修改密码
class ChangePasswordView(LoginRequiredJsonMixin, View):
    """修改密码"""

    def put(self, request):
        """实现修改密码逻辑"""
        # 接收参数
        dict = json.loads(request.body.decode())
        old_password = dict.get('old_password')
        new_password = dict.get('new_password')
        new_password2 = dict.get('new_password2')

        # 校验参数
        if not all([old_password, new_password, new_password2]):
           return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})


        result = request.user.check_password(old_password)
        if not result:
            return JsonResponse({'code': 400, 'errmsg': '原始密码不正确'})

        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_password):
            return JsonResponse({'code': 400, 'errmsg': '密码最少8位,最长20位'})

        if new_password != new_password2:
            return JsonResponse({'code': 400, 'errmsg': '两次输入密码不一致'})

        # 修改密码
        try:
            request.user.set_password(new_password)
            request.user.save()
        except Exception:

            return JsonResponse({'code': 400, 'errmsg': '修改密码失败'})

        # 清理状态保持信息
        logout(request)

        response = JsonResponse({'code': 0, 'errmsg': 'ok'})

        response.delete_cookie('username')

        # # 响应密码修改结果：重定向到登录界面
        return response