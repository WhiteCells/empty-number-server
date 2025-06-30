### 文档

- 协议: HTTP
- 请求格式: application/json
- 返回格式: application/json
- 本地测试地址: http://127.0.0.1:8000

#### 推送分机账号

- 请求地址：/api/account
- 请求方法：POST
- 请求头：
  - Content-Type: application/json

请求体参数：

| 参数名             | 类型       | 是否必填 | 描述             |
| --------------- | -------- | ---- | -------------- |
| account         | `array`  | 是    | 分机账号列表         |
| account\[].host | `string` | 是    | SIP 服务器地址（含端口） |
| account\[].name | `string` | 是    | 分机账号用户名        |
| account\[].pwd  | `string` | 是    | 分机账号密码         |

请求示例：

```curl
curl --location 'http://127.0.0.1:8000/api/account' \
--header 'Content-Type: application/json' \
--data '{
    "account": [
        {
            "host": "192.168.10.51:5060",
            "name": "1004",
            "pwd": "1004"
        },
        {
            "host": "192.168.10.51:5060",
            "name": "1001",
            "pwd": "1001"
        },
        {
            "host": "192.168.10.51:5060",
            "name": "1002",
            "pwd": "1002"
        }
    ]
}'
```

响应示例：

```json
{
    "code": 200,
    "data": {
        "accounts": [
            {
                "host": "192.168.10.51:5060",
                "name": "1003",
                "pwd": "1003"
            },
            {
                "host": "192.168.10.51:5060",
                "name": "1005",
                "pwd": "1005"
            },
            {
                "host": "192.168.10.51:5060",
                "name": "1006",
                "pwd": "1006"
            }
        ]
    },
    "msg": null
}
```


#### 推送拨号号码

- 请求方法：/api/dialplan
- 请求方式：POST
- 请求头：
  - Content-Type: application/json

请求体参数：

| 参数名         | 类型         | 是否必填 | 描述           |
| ----------- | ---------- | ---- | ------------ |
| phone       | `string[]` | 是    | 需要拨打的电话号码数组  |
| return\_url | `string`   | 是    | 回调通知地址（POST） |

请求示例：

```curl
curl --location 'http://127.0.0.1:8000/api/dialplan' \
--header 'Content-Type: application/json' \
--data '{
    "phone": [
        "818871357213"
    ],
    "return_url": "http://127.0.0.1:5001"
}'
```

响应示例：

```json
{
    "code": 200,
    "data": {
        "task_id": 255,
        "dialplans": [
            {
                "id": 501,
                "phone": "818871357213",
                "client_id": null,
                "status": "free",
                "result": null,
                "created_at": "2025-06-30T10:11:12.251774",
                "updated_at": "2025-06-30T10:11:12.251777",
                "task_id": 255
            }
        ],
        "return_url": "http://127.0.0.1:5001"
    },
    "msg": null
}
```


#### 获取所有任务

- 请求方法：/api/tasks
- 请求方式：GET
- 请求头：
  - Content-Type: application/json

请求示例：

```curl
curl --location 'http://127.0.0.1:8000/api/tasks?page=1&size=10'
--header 'Content-Type: application/json'
```

响应示例：

```json
{
    "code": 200,
    "data": [
        {
            "id": 255,
            "status": "finish",
            "return_url": "http://127.0.0.1:5001",
            "created_at": "2025-06-30T10:11:12",
            "updated_at": "2025-06-30T10:11:17"
        }
    ],
    "msg": "success"
}
```


#### 获取指定任务

- 请求方法：/api/tasks/{task_id}
- 请求方式：GET
- 请求头：
  - Content-Type: application/json

请求示例：

```curl
curl --location 'http://127.0.0.1:8000/api/task/255'
```

响应示例：

```json
{
    "code": 200,
    "data": {
        "id": 255,
        "status": "finish",
        "return_url": "http://127.0.0.1:5001",
        "created_at": "2025-06-30T10:11:12",
        "updated_at": "2025-06-30T10:11:17",
        "dialplans": [
            {
                "id": 501,
                "phone": "818871357225",
                "client_id": null,
                "status": "finish",
                "result": null,
                "created_at": "2025-06-30T10:11:12",
                "updated_at": "2025-06-30T10:11:33",
                "task_id": 255
            }
        ]
    },
    "msg": null
}
```