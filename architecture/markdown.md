# 校园二手交易平台
## 1、系统架构概述
```
graph TD;
    subgraph 本地开发环境
        A1[前端 Vue+ Pinia + Axios + Vue Router]
        A2[后端 Django]
        A3[(MySQL 数据库)]
    end

    A1 --> |HTTP API 请求| A2
    A2 --> |读写数据| A3

```

## 2、技术栈选择
| 组件 | 技术 | 选择原因 |
| --- | --- | --- |
| 前端 | Vue 3 | 轻量、易学、生态完善，支持 Vue Router 进行前端路由管理|
| 状态管理|Pinia| 代替 Vuex，API 简洁，性能优越|
| 前端路由| Vue Router |处理单页面应用（SPA）的导航|
| HTTP 请求 | Axios | 简单、功能强大，支持拦截器 |
| 后端| Django |Python Web 框架，自带 ORM，开发快速|
| 数据库 | MySQL | 关系型数据库，稳定可靠，支持事务 |

## 3、架构说明

### 1.前端（Vue + Pinia + Axios + Vue Router）
 - 运行方式：npm run dev
 - 通过 Axios 调用后端 API 获取数据
 - 运行在 Vite 提供的开发服务器（通常是 localhost:5173 或 localhost:3000）
 
### 2.后端（Django）
 - 运行方式：python manage.py runserver
 - 提供 RESTful API 供前端调用
 - 运行在 localhost:8000
 
### 3.数据库（MySQL）
 - Django 通过 models.py 访问 MySQL
 - 处理用户数据、商品信息、订单等
 
## 4、关键架构设计
```
sequenceDiagram
    participant 用户
    participant Vue前端
    participant Django后端
    participant MySQL数据库

    用户->>Vue前端: 访问网站
    Vue前端->>Django后端: 发送 API 请求 (Axios)
    Django后端->>MySQL数据库: 查询/写入数据
    MySQL数据库-->>Django后端: 返回查询结果
    Django后端-->>Vue前端: 返回 JSON 数据
    Vue前端-->>用户: 渲染页面
```

