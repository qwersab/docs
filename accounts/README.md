# 用户账户接口文档

本文档描述了Trading平台的用户账户相关API接口，包括用户注册、登录、查看和更新用户信息。

## 基本信息

- 基础URL: `http://localhost:8000/`
- 认证方式: Token认证
- 内容类型: `application/json`

## 接口列表

### 1. 用户注册

- **URL**: `/accounts/register/`
- **方法**: POST
- **描述**: 创建新用户账号
- **请求参数**:

```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}
```

- **成功响应** (201 Created):

```json
{
    "username": "testuser",
    "email": "test@example.com"
}
```

- **错误响应** (400 Bad Request):

```json
{
    "username": [
        "该用户名已经存在"
    ]
}
```

### 2. 用户登录

- **URL**: `/accounts/login/`
- **方法**: POST
- **描述**: 验证用户凭据并返回认证令牌
- **请求参数**:

```json
{
    "username": "testuser",
    "password": "password123"
}
```

- **成功响应** (200 OK):

```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "created_at": "2023-06-01T12:00:00Z",
        "login_at": "2023-06-01T14:30:00Z",
        "profile_picture": null
    }
}
```

- **错误响应** (400 Bad Request):

```json
{
    "non_field_errors": [
        "用户名或密码不正确"
    ]
}
```

### 3. 获取用户信息

- **URL**: `/accounts/user/`
- **方法**: GET
- **描述**: 获取当前登录用户的信息
- **请求头**:
  - `Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`

- **成功响应** (200 OK):

```json
{
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2023-06-01T12:00:00Z",
    "login_at": "2023-06-01T14:30:00Z",
    "profile_picture": null
}
```

- **错误响应** (401 Unauthorized):

```json
{
    "detail": "认证令牌无效"
}
```

### 4. 更新用户信息

- **URL**: `/accounts/user/update/`
- **方法**: PATCH
- **描述**: 更新当前登录用户的信息
- **请求头**:
  - `Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`
  - `Content-Type: application/json`

- **请求参数** (所有字段都是可选的):

```json
{
    "email": "updated@example.com",
    "profile_picture": null
}
```

- **成功响应** (200 OK):

```json
{
    "username": "testuser",
    "email": "updated@example.com",
    "profile_picture": null
}
```

- **错误响应** (400 Bad Request):

```json
{
    "email": [
        "输入一个有效的邮箱地址"
    ]
}
```

## Postman测试

项目包含了一个完整的Postman集合，可以用于测试所有API接口。

1. 导入 `accounts/postman_collection.json` 文件到Postman
2. 设置环境变量：
   - `base_url`: API的基础URL (例如 `http://localhost:8000`)
   - `auth_token`: 登录后获取的认证令牌

## 单元测试

运行单元测试以验证API功能：

```bash
python manage.py test accounts
```

单元测试包含以下测试用例：
- 用户注册测试
- 用户登录测试
- 获取用户信息测试
- 更新用户信息测试
- 无效凭据登录测试
- 重复用户名注册测试
- 未授权访问测试 