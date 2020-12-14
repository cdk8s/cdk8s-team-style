
# 安全思维



## 意识层面

## 产品层面

## 开发层面

#### 简单接入

- 平台分配给调用方一个 appKey（18位，字母全部为小写）、appSecret（32位，字母全部为小写）
- 请求头需要传下面几个参数：
    - appKey
    - nonce：随机数（最大长度 128 个字符）
    - epochMilli：当前 UTC 时间戳，到毫秒
    - shaString：对三个参数进行SHA1计算结果（字母全部为小写） SHA1(appSecret + nonce + epochMilli)




## 测试层面

## 运维层面


## 渗透测试

