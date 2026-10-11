# 一、先说明原理和限制

在高版本iPhone IOS系统中除了使用GPS，还会通过附近的WiFi和基站向Apple网络定位服务查询当前位置。只靠爱思助手改定位就拉不起需要定位的Wi-Fi calling了

WLOC模块会通过Shadowrocket拦截Apple网络定位服务的响应，并将其中的坐标替换为用户设置的位置。

简单理解：


iPhone请求网络定位→→→Apple返回当前位置→→→Shadowrocket模块拦截响应→→→将坐标替换为目标位置→→→系统读取修改后的坐标→→→正确符合运营商要求

↓

成功拉起WI-FI calling

---

需要注意：

- 本项目修改的是Apple的网络定位（WiFi/基站定位）；
- 它不是直接修改GPS硬件数据；
- 在室内、GPS信号较弱、主要依赖WiFi定位时效果最好；
- 在室外GPS信号很强时，系统或部分App可能重新使用真实GPS坐标；
- 不保证所有App都能长期稳定使用修改后的坐标；
- iOS高版本存在较强的定位缓存，切换坐标后可能需要重启设备。



# 二、准备工作

- 一台iPhone；
- 已安装Shadowrocket（小火箭）；
- 可以正常联网；
- Shadowrocket中存在一条可用英国代理；
- 系统已允许Shadowrocket创建VPN连接。

# 三、修改定位


## 苹果IOS26以下修改定位视频教程:[点击直达（科网）](https://www.youtube.com/watch?v=9kNXvGxVsQc)

## 苹果IOS27以上修改定位视频教程:[点击直达（科网）](https://www.youtube.com/watch?v=iFh-o3to7Rk)

## 如果模块失效用这个：[点击进入](https://cyberhandyman-ioslocspo.cyberhandyman.workers.dev/)

设置坐标后，打开苹果地图观察当前位置。

如果没有立即改变，可以先尝试：

- 关闭地图App；
- 在后台任务列表中彻底划掉地图；
- 关闭再打开系统定位服务；
- 重新打开地图；
- 等待系统再次触发网络定位请求。

# 四、拉取WIFICall

### iOS 15～18

iOS 15～18通常不需要重启，重新触发定位后即可生效。
（如果只是拉Wi-Fi calling甚至都不需要你改定位 关闭手机定位后重启即可）

如果仍然显示真实位置，可以：

- 关闭定位服务；
- 确认Shadowrocket已经连接；
- 确认模块和HTTPS解密已经开启；
- 重新打开定位服务；
- 打开地图验证。

### iOS 26+

根据项目说明，Apple从iOS 26开始加强了locationd的定位缓存。

即使WLOC脚本已经成功修改服务器响应，系统仍可能继续读取内存中缓存的旧坐标。

这种情况下，单独开关飞行模式或定位服务可能不足以清除缓存，建议直接重启设备。

#### 高版本推荐流程一

text

先通过快捷指令或选点页面设置目标位置
打开飞行模式
关闭系统定位服务
重启iPhone
开机后关闭飞行模式
暂时保持WiFi关闭，使用蜂窝网络联网
打开Shadowrocket并确认VPN已经连接
打开系统定位服务
打开苹果地图验证
系统定位服务入口：

text
设置 → 隐私与安全性 → 定位服务

#### 高版本推荐流程二
text

关闭系统定位服务
保持Shadowrocket代理、模块及HTTPS解密开启
设置并储存目标位置
重新打开系统定位服务
出现位置权限提示时，选择“下次询问或在我共享时”
打开苹果地图验证
如果方法二过一段时间后恢复真实位置，通常是系统重新使用了GPS结果或定位缓存。可以改用方法一，并在GPS信号较弱的室内环境测试。


# 五、总结

测试手机：iphone Xr

<img width="828" height="499" alt="Image" src="https://github.com/user-attachments/assets/082be66d-47e8-4dc3-8f10-a4db2b2f23a7" />

1. WLOC改定位到英国；

<img width="599" height="801" alt="Image" src="https://github.com/user-attachments/assets/9d865281-531e-42c5-bcf6-46dc9fdab4f8" />

2. 开启飞行模式，开启局域网通话，重启手机（隔空投送，蓝牙最好关掉）

<img width="1105" height="822" alt="Image" src="https://github.com/user-attachments/assets/6c979d30-2a9b-4e62-b947-32f5b02a42c9" />

3. 开机后，保持飞行模式，自动连接节点，检查地图，IP和时间是否都在英国

<img width="828" height="1280" alt="Image" src="https://github.com/user-attachments/assets/b7c251f1-9ef0-4165-b82e-435c713cdcb6" />

4. 数分钟内，查看手机状态栏，出现WiFiCall就成功（有人反馈等分长时间才可以，多重启几次）

<img width="600" height="833" alt="Image" src="https://github.com/user-attachments/assets/8af9e73b-0981-4f19-9b74-e75af4132d0d" />

