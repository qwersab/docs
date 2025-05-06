# 校园二手交易平台 API 文档

## 基本信息
- 版本: 1.0.0
- 描述: 校园二手交易平台API接口文档

## 目录
1. [用户相关接口](#用户相关接口)
2. [商品相关接口](#商品相关接口)
3. [订单相关接口](#订单相关接口)
4. [评论相关接口](#评论相关接口)
5. [互动相关接口](#互动相关接口)
6. [消息相关接口](#消息相关接口)

## 用户相关接口

### 查询用户信息
- **接口**: GET `/user/{id}`
- **描述**: 查询用户信息接口
- **参数**:
  - `id` (path): 用户id (integer)
  - `Authorization` (header): 认证信息 (string, 可选)
- **响应**:
  ```json
  {
    "user_id": 73,
    "username": "福若汐",
    "email": "irescp.gxn5@foxmail.com",
    "password": "DxUg8h0DgoE1kHR",
    "profile_picture": "https://loremflickr.com/400/400?lock=6684522664261550",
    "created_at": "2025-03-19 13:18:41",
    "login_at": "2025-03-19 13:18:41"
  }
  ```

### 用户注册
- **接口**: POST `/api/user/register`
- **描述**: 用户注册接口
- **请求体**:
  ```json
  {
    "username": "JohnDoe",
    "password": "password123",
    "profile_picture": "https://example.com/avatar.jpg"
  }
  ```
- **响应**:
  ```json
  {
    "id": 1,
    "username": "JohnDoe",
    "email": "john@example.com",
    "profile_picture": "https://example.com/avatar.jpg",
    "created_at": "2025-03-25T10:00:00",
    "login_at": null
  }
  ```

### 用户登录
- **接口**: POST `/api/user/login`
- **描述**: 用户登录接口
- **请求体**:
  ```json
  {
    "username": "john",
    "password": "password123"
  }
  ```
- **响应**:
  ```json
  {
    "code": 200,
    "message": "登录成功",
    "token": "abcdef123456",
    "user": {
      "id": 1,
      "username": "test_user",
      "email": "test@example.com",
      "profile_picture": "https://example.com/avatar.jpg",
      "created_at": "2025-03-25T12:00:00",
      "login_at": "2025-03-25T14:00:00"
    }
  }
  ```

### 更新用户信息
- **接口**: PUT `/api/user/update`
- **描述**: 更新用户信息接口
- **参数**:
  - `username` (query): 用户名 (string, 可选)
  - `email` (query): 邮箱 (string, 可选)
  - `profile_picture` (query): 头像 (string, 可选)
  - `Authorization` (header): 认证信息 (string, 可选)
- **响应**:
  ```json
  {
    "code": 200,
    "message": "更新成功"
  }
  ```

### 修改密码
- **接口**: PUT `/users/{id}/password`
- **描述**: 修改密码接口
- **参数**:
  - `id` (path): 用户ID (string)
- **请求体**:
  ```json
  {
    "old_password": "password123",
    "new_password": "newpass456"
  }
  ```
- **响应**:
  ```json
  {
    "code": 200,
    "message": "密码重置成功"
  }
  ```

## 商品相关接口

### 发布商品
- **接口**: POST `/api/product/add`
- **描述**: 发布商品接口
- **请求体**:
  ```json
  {
    "name": "二手笔记本电脑",
    "detail": "i7 8代，16G 内存，512G SSD",
    "cover_list": "https://example.com/image1.jpg,https://example.com/image2.jpg",
    "old_level": 9,
    "category_id": 1,
    "user_id": 1001,
    "inventory": 5,
    "price": 2500.5,
    "is_bargain": true
  }
  ```
- **响应**:
  ```json
  {
    "code": 200,
    "message": "商品发布成功",
    "product_id": 1
  }
  ```

### 获取商品详情
- **接口**: GET `/api/product/{id}`
- **描述**: 获取指定商品详情接口
- **参数**:
  - `id` (path): 商品ID (string)
- **响应**:
  ```json
  {
    "code": 200,
    "product": {
      "id": 1,
      "name": "二手笔记本电脑",
      "detail": "i7 8代，16G 内存，512G SSD",
      "cover_list": "https://example.com/image1.jpg,https://example.com/image2.jpg",
      "old_level": 9,
      "category_id": 1,
      "user_id": 1001,
      "inventory": 5,
      "price": 2500.5,
      "is_bargain": true,
      "create_at": "2025-03-25T12:00:00"
    }
  }
  ```

### 获取商品列表
- **接口**: GET `/api/product/list`
- **描述**: 获取商品列表
- **参数**:
  - `page` (query): 页码 (integer, 可选)
  - `size` (query): 每页数量 (string, 可选)
  - `category_id` (query): 分类ID (integer, 可选)
  - `min_price` (query): 最低价格 (string, 可选)
  - `max_price` (query): 最高价格 (string, 可选)
- **响应**:
  ```json
  {
    "code": 200,
    "products": [
      {
        "id": 1,
        "name": "二手笔记本电脑",
        "detail": "i7 8代，16G 内存，512G SSD",
        "cover_list": "https://example.com/image1.jpg,https://example.com/image2.jpg",
        "old_level": 9,
        "category_id": 1,
        "user_id": 1001,
        "inventory": 5,
        "price": 2500.5,
        "is_bargain": true,
        "create_at": "2025-03-25T12:00:00"
      }
    ],
    "total": 2
  }
  ```

### 更新商品信息
- **接口**: PUT `/api/product/update/{id}`
- **描述**: 更新商品信息接口
- **参数**:
  - `id` (path): 商品ID (string)
- **请求体**:
  ```json
  {
    "price": "2400.0",
    "inventory": "10"
  }
  ```
- **响应**:
  ```json
  {
    "code": 200,
    "message": "更新成功"
  }
  ```

### 删除商品
- **接口**: DELETE `/api/product/delete/{id}`
- **描述**: 删除商品接口
- **参数**:
  - `id` (path): 商品ID (string)
- **响应**:
  ```json
  {
    "code": 200,
    "message": "商品删除成功"
  }
  ```

### 获取用户发布的商品
- **接口**: GET `/api/product/user/{user_id}`
- **描述**: 获取用户发布的商品
- **参数**:
  - `user_id` (path): 用户ID (integer)
- **响应**:
  ```json
  {
    "code": 200,
    "products": [
      {
        "id": 1,
        "name": "二手笔记本电脑",
        "detail": "i7 8代，16G 内存，512G SSD",
        "cover_list": "https://example.com/image1.jpg,https://example.com/image2.jpg",
        "old_level": 9,
        "category_id": 1,
        "inventory": 5,
        "price": 2500.5,
        "is_bargain": true,
        "create_at": "2025-03-25T12:00:00"
      }
    ]
  }
  ```

## 订单相关接口

### 获取订单列表
- **接口**: GET `/orders`
- **描述**: 获取订单列表
- **参数**:
  - `pages` (query): 页码 (integer, 可选)
  - `size` (query): 每页数量 (integer, 可选)
  - `trade_status` (query): 交易状态筛选 (string, 可选)
- **响应**:
  ```json
  {
    "total": 10,
    "page": 1,
    "size": 10,
    "orders": [
      {
        "id": 1,
        "code": "ORD12345",
        "detail": "备注信息",
        "product_id": 101,
        "buy_price": 199.99,
        "trade_status": 0,
        "trade_time": "2025-03-25T14:30:00",
        "create_time": "2025-03-25T14:30:00"
      }
    ]
  }
  ```

### 创建订单
- **接口**: POST `/orders`
- **描述**: 创建订单
- **请求体**:
  ```json
  {
    "code": "ORD12346",
    "detail": "备注信息",
    "product_id": 102,
    "buy_price": 199.99,
    "trade_status": 0,
    "trade_time": "2025-03-25T14:30:00",
    "create_time": "2025-03-25T14:30:00"
  }
  ```
- **响应**:
  ```json
  {
    "id": 1,
    "code": "ORD12346",
    "detail": "备注信息",
    "product_id": 102,
    "buy_price": 199.99,
    "trade_status": 0,
    "trade_time": "2025-03-25T14:30:00",
    "create_time": "2025-03-25T14:30:00"
  }
  ```

### 获取订单详情
- **接口**: GET `/orders/{id}`
- **描述**: 根据订单 ID 获取订单详情接口
- **参数**:
  - `id` (path): 订单ID (integer)
- **响应**:
  ```json
  {
    "id": 1,
    "code": "ORD12345",
    "detail": "备注信息",
    "product_id": 101,
    "buy_price": 199.99,
    "trade_status": 0,
    "trade_time": "2025-03-25T14:30:00",
    "create_time": "2025-03-25T14:30:00"
  }
  ```

### 更新订单
- **接口**: PUT `/orders/{id}`
- **描述**: 更新订单
- **参数**:
  - `id` (path): 订单ID (string)
- **请求体**:
  ```json
  {
    "code": "ORD12347",
    "detail": "更新备注",
    "product_id": 103,
    "buy_price": 249.99,
    "trade_status": 1,
    "trade_time": "2025-03-25T15:00:00",
    "create_time": "2025-03-25T14:30:00"
  }
  ```
- **响应**:
  ```json
  {
    "id": 1,
    "code": "ORD12347",
    "detail": "更新备注",
    "product_id": 103,
    "buy_price": 249.99,
    "trade_status": 1,
    "trade_time": "2025-03-25T15:00:00",
    "create_time": "2025-03-25T14:30:00"
  }
  ```

### 删除订单
- **接口**: DELETE `/orders/{id}`
- **描述**: 删除订单
- **参数**:
  - `id` (path): 订单ID (string)
- **响应**:
  ```json
  {
    "message": "删除成功"
  }
  ```

## 评论相关接口

### 获取评论列表
- **接口**: GET `/comments`
- **描述**: 获取评论列表
- **参数**:
  - `product_id` (query): 商品ID (integer, 可选)
  - `page` (query): 页码 (integer, 可选)
  - `size` (query): 每页数量 (integer, 可选)
- **响应**:
  ```json
  {
    "total": 50,
    "page": 1,
    "size": 10,
    "comments": [
      {
        "id": 1,
        "user_id": "user123",
        "product_id": "product101",
        "content": "这款商品质量很好，非常满意。",
        "created_at": "2025-03-25T14:00:00"
      }
    ]
  }
  ```

### 发布评论
- **接口**: POST `/comments`
- **描述**: 发布评论
- **请求体**:
  ```json
  {
    "user_id": 123,
    "product_id": 101,
    "content": "商品非常好，值得购买！",
    "created_at": "2025-03-25T14:00:00"
  }
  ```
- **响应**:
  ```json
  {
    "id": 1,
    "user_id": 123,
    "product_id": 101,
    "content": "商品非常好，值得购买！",
    "created_at": "2025-03-25T14:00:00"
  }
  ```

### 获取评论详情
- **接口**: GET `/comments/{id}`
- **描述**: 获取单个评论详情
- **参数**:
  - `id` (path): 评论ID (string)
- **响应**:
  ```json
  {
    "id": 1,
    "user_id": "user123",
    "product_id": "product101",
    "content": "这款商品质量很好，非常满意。",
    "created_at": "2025-03-25T14:00:00"
  }
  ```

## 互动相关接口

### 获取用户互动行为列表
- **接口**: GET `/interactions`
- **描述**: 获取用户互动行为列表
- **参数**:
  - `user_id` (query): 用户ID (integer, 可选)
  - `type` (query): 行为类型 (integer, 可选) - 1：浏览，2：收藏，3：想要
- **响应**:
  ```json
  {
    "total": 3,
    "page": 1,
    "size": 10,
    "interactions": [
      {
        "id": 1,
        "user_id": 1001,
        "product_id": 2001,
        "type": 1,
        "create_time": "2025-03-25T14:00:00"
      }
    ]
  }
  ```

### 添加互动行为
- **接口**: POST `/interactions`
- **描述**: 添加互动行为（用户对商品进行互动，如收藏2、浏览1或标记"想要"3）
- **请求体**:
  ```json
  {
    "user_id": 1001,
    "product_id": 2001,
    "type": 1,
    "create_time": "2025-03-25T14:15:00"
  }
  ```
- **响应**:
  ```json
  {
    "id": 1,
    "user_id": 1001,
    "product_id": 2001,
    "type": 1,
    "create_time": "2025-03-25T14:15:00"
  }
  ```

### 获取用户某个商品的互动行为
- **接口**: GET `/interactions/{user_id}/{product_id}`
- **描述**: 获取用户某个商品的互动行为
- **参数**:
  - `user_id` (path): 用户ID (string)
  - `product_id` (path): 商品ID (string)
- **响应**:
  ```json
  {
    "id": 1,
    "user_id": 1001,
    "product_id": 2001,
    "type": 1,
    "create_time": "2025-03-25T14:00:00"
  }
  ```

### 删除互动行为
- **接口**: DELETE `/interactions/{id}`
- **描述**: 删除互动行为
- **参数**:
  - `id` (path): 行为ID (integer)
- **响应**:
  ```json
  {
    "message": "互动行为删除成功"
  }
  ```

## 消息相关接口

### 获取用户消息列表
- **接口**: GET `/messages`
- **描述**: 获取用户消息列表
- **参数**:
  - `user_id` (query): 用户ID (integer, 可选)
  - `is_read` (query): 是否已读 (boolean, 可选)
  - `page` (query): 页码 (integer, 可选)
  - `size` (query): 每页数量 (integer, 可选)
- **响应**:
  ```json
  {
    "total": 10,
    "page": 1,
    "size": 10,
    "messages": [
      {
        "id": 1,
        "user_id": 1001,
        "content": "您的订单已取消。",
        "is_read": false,
        "create_time": "2025-03-25T14:15:00"
      }
    ]
  }
  ```

### 发送消息
- **接口**: POST `/messages`
- **描述**: 发送消息
- **请求体**:
  ```json
  {
    "user_id": 1001,
    "content": "您的订单已取消。",
    "is_read": false,
    "create_time": "2025-03-25T14:15:00"
  }
  ```
- **响应**:
  ```json
  {
    "id": 1,
    "user_id": 1001,
    "content": "您的订单已取消。",
    "is_read": false,
    "create_time": "2025-03-25T14:15:00"
  }
  ```

### 获取消息详情
- **接口**: GET `/messages/{id}`
- **描述**: 获取单条消息详情
- **参数**:
  - `id` (path): 消息ID (integer)
- **响应**:
  ```json
  {
    "id": 1,
    "user_id": 1001,
    "content": "您的订单已取消。",
    "is_read": false,
    "create_time": "2025-03-25T14:15:00"
  }
  ```

### 删除消息
- **接口**: DELETE `/messages/{id}`
- **描述**: 删除某条消息
- **参数**:
  - `id` (path): 消息ID (string)
- **响应**:
  ```json
  {
    "message": "删除成功"
  }
  ```

### 标记消息为已读
- **接口**: PUT `/messages/{id}/read`
- **描述**: 标记消息为已读
- **参数**:
  - `id` (path): 消息ID (integer)
- **响应**:
  ```json
  {
    "message": "标记成功"
  }
  ``` 