"""
Postman API测试用例

1. 用户注册接口测试
POST /api/register/
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}
预期响应:
200 OK
{
    "username": "testuser",
    "email": "test@example.com"
}

2. 用户登录接口测试
POST /api/login/
{
    "username": "testuser",
    "password": "password123"
}
预期响应:
200 OK
{
    "token": "生成的Token值",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "created_at": "创建时间",
        "login_at": "登录时间",
        "profile_picture": null
    }
}

3. 获取用户信息接口测试
GET /api/user/
Headers:
Authorization: Token 生成的Token值
预期响应:
200 OK
{
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "创建时间",
    "login_at": "登录时间",
    "profile_picture": null
}

4. 更新用户信息接口测试
PATCH /api/user/update/
Headers:
Authorization: Token 生成的Token值
{
    "email": "updated@example.com",
    "profile_picture": "上传的图片文件"
}
预期响应:
200 OK
{
    "username": "testuser",
    "email": "updated@example.com",
    "profile_picture": "图片URL"
}

5. 登录失败测试 - 错误密码
POST /api/login/
{
    "username": "testuser",
    "password": "wrongpassword"
}
预期响应:
400 Bad Request
{
    "non_field_errors": [
        "用户名或密码不正确"
    ]
}

6. 注册失败测试 - 已存在用户名
POST /api/register/
{
    "username": "testuser",
    "email": "another@example.com",
    "password": "password123"
}
预期响应:
400 Bad Request
{
    "username": [
        "该用户名已经存在"
    ]
}

7. 获取用户信息失败测试 - 无效Token
GET /api/user/
Headers:
Authorization: Token 无效Token值
预期响应:
401 Unauthorized
{
    "detail": "无效令牌"
}

8. 上传头像图片接口
POST /api/user/upload-avatar/
请求头:
Authorization: Token your_token_here
Content-Type: multipart/form-data
请求体:
profile_picture: 图片文件

9. 修改密码接口
URL: /api/user/change-password/
方法: POST
请求头:
Authorization: Token your_token_here
Content-Type: application/json
 {
       "old_password": "当前密码",
       "new_password": "新密码",
       "confirm_password": "确认新密码"
   }
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User

class AccountsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_info_url = reverse('user-info')
        self.user_update_url = reverse('user-update')
        
        # 创建测试用户数据
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }
        
    def test_user_registration(self):
        """测试用户注册功能"""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        
    def test_user_login(self):
        """测试用户登录功能"""
        # 先注册用户
        self.client.post(self.register_url, self.user_data, format='json')
        
        # 测试登录
        login_data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        self.assertTrue('user' in response.data)
        
    def test_get_user_info(self):
        """测试获取用户信息功能"""
        # 先注册用户
        self.client.post(self.register_url, self.user_data, format='json')
        
        # 登录获取token
        login_data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        token = response.data['token']
        
        # 使用token获取用户信息
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.get(self.user_info_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        
    def test_update_user_info(self):
        """测试更新用户信息功能"""
        # 先注册用户
        self.client.post(self.register_url, self.user_data, format='json')
        
        # 登录获取token
        login_data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        token = response.data['token']
        
        # 更新用户信息
        update_data = {
            'email': 'updated@example.com'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.patch(self.user_update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'updated@example.com')
        
    def test_login_invalid_credentials(self):
        """测试使用无效凭据登录"""
        # 先注册用户
        self.client.post(self.register_url, self.user_data, format='json')
        
        # 使用错误密码登录
        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_register_duplicate_username(self):
        """测试注册重复用户名"""
        # 先注册一个用户
        self.client.post(self.register_url, self.user_data, format='json')
        
        # 使用相同用户名再次注册
        duplicate_data = {
            'username': 'testuser',
            'email': 'another@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.register_url, duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_unauthorized_access(self):
        """测试未授权访问"""
        response = self.client.get(self.user_info_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
