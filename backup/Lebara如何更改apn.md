Lebara UK 使用 Vodafone 网络。

如果手机无法上网，可以在 APN 设置中检查或切换以下配置：

- Vodafone（夯）
- Talkmobile（NPC）
- Lebara（拉完了）

> 首选配置应使用 Vodafone 官方 APN。
> Talkmobile 和 Lebara 配置只建议作为排障备用，不保证每张 Lebara SIM 都能使用。

---

## 一、进入 APN 设置

Android 手机常见路径：

```text
设置
→ 移动网络
→ 选择 Lebara SIM 卡
→ 接入点名称（APN）
```

部分手机的路径可能是：

```text
设置
→ 连接
→ 移动网络
→ 接入点名称
```

进入 APN 页面后，点击“添加”或“新建 APN”。

---

## 二、Vodafone APN 配置

| 设置项目 | 内容 |
|---|---|
| 名称 | `Vodafone UK` |
| APN | `wap.vodafone.co.uk` |
| 用户名 | `wap` |
| 密码 | `wap` |
| APN 类型 | `default,supl,mms` |
| 身份验证类型 | `无 / None` |

| 设置项目 | 内容 |
|---|---|
| 名称 | `Vodafone ` |
| APN | `live.vodafone.com` |
| 用户名 | `wap` |
| 密码 | `wap` |
| APN 类型 | `default,supl` |
| 身份验证类型 | `无 / None` |

## 三、Talkmobile APN 配置

| 设置项目 | 内容 |
|---|---|
| 名称 | `Talkmobile PAYG` |
| APN | `payg.talkmobile.co.uk` |
| 用户名 | `wap` |
| 密码 | `wap` |
| APN 类型 | `default,supl,mms` |
| 身份验证类型 | `无 / None` |

## 四、Lebara APN 配置

| 设置项目 | 内容 |
|---|---|
| 名称 | `Lebara Internet` |
| APN | `uk.lebara.mobi` |
| 用户名 | `wap` |
| 密码 | `wap` |
| MCC | `234` |
| MNC | `15` |
| 身份验证类型 | `无 / None` |
| APN 类型 | `default,supl,mms` |
| 代理 | 留空 |
| 端口 | 留空 |

---

保存后，选择对应的APN，重启手机。

---
