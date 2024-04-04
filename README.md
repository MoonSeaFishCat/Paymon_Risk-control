# paymon风控处理终端
前言：由于最近黑灰泛滥，为安全起见，决定添加消息风控系统!!!

## 本地开发
备注：本项目用时两天半，算是雏形，后期有兴趣在维护

下载源码后，运行
```
pip install -r requirements.txt
```
安装项目依赖，然后进行开发即可

## 接口信息

# 派蒙风控系统

Base URLs:

* <a href="http://dev-cn.your-api-server.com">开发环境: 127.0.0.1:5000</a>
# Authentication

# Default

## POST 插件信息提交

POST /submit_plugin

> Body 请求参数

```json
{
  "name": "Exampl",
  "author": "John Doe",
  "md5": "1d7c29228d8b1c3df3f9bc9f836c7e12",
  "server_ip": "192.168.1.100",
  "machine_code": "ABC123DEF456"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Content-Type|header|string| 否 |none|
|body|body|object| 否 |none|

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "message": "string",
  "plugin_id": 0
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» message|string|true|none||none|
|» plugin_id|integer|true|none||none|

## POST 信息审核

POST /check_risk_keywords

> Body 请求参数

```json
{
  "text": "我喜欢你。七七"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Content-Type|header|string| 否 |none|
|body|body|object| 否 |none|

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "message": "string"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» message|string|true|none||none|

## POST 插件审核查询

POST /info_search

> Body 请求参数

```json
{
  "name": "我喜欢你。七七"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Content-Type|header|string| 否 |none|
|body|body|object| 否 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

## POST 插件审核提交

POST /info_submit

> Body 请求参数

```json
{
  "name": "Exampl",
  "author": "John Doe",
  "qq": "1d7c29228d8b1c3df3f9bc9f836c7e12"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Content-Type|header|string| 否 |none|
|body|body|object| 否 |none|

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "message": "string"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» message|string|true|none||none|



