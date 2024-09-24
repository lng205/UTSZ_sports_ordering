# 开发信息

体育中心貌似只能用微信公众号订，微信生态的细节不明且似乎较为复杂~~张小龙啊啊啊啊啊~~，但本质仍然是web交互，可以抓包分析。

~~之前用Charles爬过集市，但试用会一直弹窗有点麻烦。看了看Fiddle也需要付费。决定试试Whistle，目前体验良好，赞美开源。~~

通过Whistle提取curl请求再转为python requests代码，可以爬到场次查询结果：`response.json`。

场次信息为json格式，只返回被订的场次。`listVenue`绑定了场号和id（注意是`id`不是`venueTypeID`），`listWeixinVenueStatus`存储了所有被订的场次。

如果脚本能在场次发布时立即订场，应当可以不用解析场次信息，直接订场。

故问题转为如何模拟订单和支付请求。

跟踪支付请求，发现关键为两次post请求，第一次创建订单，第二次支付订单。

---

尝试去除无关内容，发现服务器不检查header，仅检查cookies。

同时，cookies中，除了用于防止XSS的XSRF-TOKEN，其余内容在多个请求中均是不变的，表明这些cookies决定了微信大学城身份认证信息。

故抓包微信HTTPS流量得到cookies，并去除XSRF-TOKEN后，可以稳定地模拟一名大学城用户的请求。

---

实测发现中间的大量请求都不影响订场请求。~~真是规范的RESTful API~~

成功模拟了订单和支付请求后，剩下的任务是定时执行脚本。

---

超过订场日期会返回：

```py
{'result': None, 'targetUrl': None, 'success': False, 'error': {'code': 0, 'message': '已超过可订场日期', 'details': None, 'validationErrors': None}, 'unAuthorizedRequest': False, '__abp': True}
```

未到22:00会返回：

```py
{'result': None, 'targetUrl': None, 'success': False, 'error': {'code': 0, 'message': '未到放场时间22:00', 'details': None, 'validationErrors': None}, 'unAuthorizedRequest': False, '__abp': True}
```

~~居然没有漏洞~~