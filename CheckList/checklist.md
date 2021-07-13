[TOC]

# **Check list - 功能点**

## 登录

- SQL注入

- XSS

```php
 <?php 
 echo "<input name='username' value=".$username.">";
 ?>
```

- 验证码绕过

- 弱口令

- dos

## 注册

- 任意注册，示例 [222.197.165.168-任意注册管理员用户](http://yulinsec.com:28120/pages/viewpage.action?pageId=6292154)


## 修改密码

- 验证码绕过
- 任意密码重置
- 密码重置连接未过期
- 密码重置无速率限制
- 输入长密码时拒绝服务
- 通过密码重置页面进行用户枚举
- host 头攻击
- referer泄漏密码重置令牌
- 弱凭证问题
- 凭证泄露（referer头）
- 使用电子邮件参数重置密码
- 替换返回包中的信息

> 参考：[国外众测之密码找回漏洞 - 先知社区 (aliyun.com)](https://xz.aliyun.com/t/9719)   

## 搜索框

- SQL注入
- XSS

## 输入框

- XSS

## 文件上传

- 任意文件上传
- sql注入

## API

- API泄露
- 信息泄露
- 水平越权
- 垂直越权

# Check list - 测试过程

> 参考：`https://github.com/e11i0t4lders0n/Web-Application-Pentest-Checklist/blob/main/Web_Application_Penetration_Testing_Checklist_by_Tushar_Verma.pdf`

## 信息收集

* 侦察阶段 
* 识别网络服务器、技术和数据库 
* 子公司和收购清单 
* 反向查找 
* ASN & IP 空间枚举和服务枚举 
* 谷歌多金 
* Github 侦察
* 目录枚举 
* IP 范围枚举 
* JS文件分析 
* 子域枚举和暴力破解 
* 子域接管 
* 参数模糊测试 
* 端口扫描 
* 基于模板的扫描（核） 
* 回溯历史 
* 断链劫持 
* 互联网搜索引擎发现 
* 配置错误的云存储 

## 注册测试

- 检查重复注册/覆盖现有用户 

- 检查弱密码策略 

- 检查重用现有用户名 

- 检查电子邮件验证过程是否不足 

- 弱注册实施 - 允许一次性电子邮件地址

- 弱注册实现 - Over HTTP 

- 通过特制的用户名注册覆盖默认的 Web 应用程序页面。

- 注册后，您的个人资料链接是否就像这样： `www.username.com/username?`

    1. 如果是，请枚举 Web 应用程序的默认文件夹，例如 /images、/contact、/portfolio 

    2. 使用用户名（例如图片、联系人、作品集）进行注册 

    3. 检查这些默认文件夹是否已被您的个人资料链接覆盖。

## Session管理测试

* 从应用程序中的批量 cookie 中识别实际的会话 cookie 
* 使用一些标准的解码算法（如 Base64、hex、URL 等）对 cookie 进行解码 
* 按 1 位/字节修改 cookie.session 令牌值。 然后重新提交并对所有令牌执行相同操作。 减少您需要执行的工作量，以识别令牌的哪一部分实际正在使用，哪些没有。
* 如果可以自行注册并且您可以选择您的用户名，请使用一系列相似的用户名登录，其中包含它们之间的细微差异，例如 A、AA、AAA、AAAA、AAAB、AAAC、AABA 等。 如果在登录时提交其他用户特定数据或存储在用户配置文件中（例如电子邮件地址） 
* 检查会话 cookie 和 cookie 到期日期/时间 
* 确定 cookie 域范围
* 检查 cookie 中的 HttpOnly 标志
* 检查应用程序是否通过 SSL 检查 cookie 中的安全标志
* 检查会话固定，即身份验证前后会话 cookie 的值 
* 从不同的有效IP地址或系统重放会话cookie以检查服务器是否维护机器状态 
* 检查通过不同机器/IP 的并发登录 
* 检查是否有任何用户相关信息存储在 cookie 值中 如果是，则篡改其他用户的数据 
* 未能使会话无效（电子邮件更改，2FA 激活） 

## 认证测试

* 用户名枚举
* 在用户名和密码字段上使用各种 SQL 注入绕过身份验证 
* 缺少密码确认
    * 更改电子邮件地址
    * 更改密码 
    * 管理 2FA 
* 是否可以在没有身份验证的情况下使用资源？ 访问冲突 
* 检查用户凭据是否通过 SSL 传输 
* 弱登录功能 HTTP 和 HTTPS 都可用 
* 在蛮力攻击中测试用户帐户锁定机制
    变化：如果服务器阻止即时用户请求，则尝试使用来自入侵者的时间限制选项并再次重复该过程。 
    * 通过将用户代理篡改到移动用户代理来绕过速率限制 
    * 通过将用户代理篡改到匿名用户代理来绕过速率限制 
    * 使用空字节绕过速率限制 
* 使用 cewl 命令创建密码词表，[cewl工具介绍](https://www.freebuf.com/articles/network/190128.html)
* 测试Oauth登陆功能
    * OAuth 角色（以Twitter为例？)
        * Resource Owner → User
        * Resource Server → Twitter
        * Client Application → Twitterdeck.com
        * Authorization Server → Twitter
        * client_id → Twitterdeck ID  (This is a public, non-secret unique identifier_)
        * client_secret → Twitter 和 Twitterdeck 已知的用于生成 access_tokens 的秘密令牌 
        * response_type → 定义令牌类型  e.g (code, token, etc.)
        * scope → Twitterdeck 要求的访问级别 
        * redirect_uri → 授权完成后重定向到的URL用户 
        * state → OAuth 中的主要 CSRF 保护可以在被定向到 授权服务器并再次返回 
        * grant_type → 定义 grant_type 和返回的令牌类型 
        * code → 推特生成的授权码，会像 `?code=` , 该代码与 client_id 和 client_secret 一起使用以获取 access_token 
        * access_token → twitterdeck 用于代表用户发出 API 请求的令牌 
        * refresh_token → 允许应用程序在不提示用户的情况下获取新的 access_token 
    * 代码缺陷 
        * 重用代码 
        * 代码预测/蛮力和速率限制 
        * 应用程序 X 的代码对应用程序 Y 是否有效？ 
    * Redirect_uri 缺陷 
        * URL 根本没有经过验证：`?redirect_uri=https://attacker.com`
        * 允许子域（子域接管或在这些子域上打开重定向）:  `?redirect_uri=https://sub.twitterdeck.com`
        * 主机验证，路径不是（链开放重定向）: `?redirect_uri=https://twitterdeck.com/callback?redirectUrl=https://evil.com`
        * 主机验证，路径不是（Referer泄露）:  在 HTML 页面上包含外部内容并通过 Referer 泄漏代码 
        * 弱正则表达式 
        * 在主机之后暴力破解 URL 编码的字符：`redirect_uri=https://twitterdeck.com§FUZZ§ `
        * 在主机之后（或在任何白名单打开重定向过滤器上）强制执行关键字白名单： `?redirect_uri=https://§FUZZ§.com `
        * URI 验证就位：使用典型的开放重定向有效负载 
    * 状态缺陷
        * 缺少状态参数？(CSRF)
        * 可预测状态参数？ 
        * 是否正在验证状态参数？
    * 杂项
        * client_secret 是否经过验证？
        * Pre ATO 使用 Facebook 电话号码注册
        * ATO前没有电子邮件验证 
* 测试 2FA 配置错误 
    * 响应操作
    * 状态码
    * ManipulationWeb 应用程序渗透测试清单 4
    * 响应中的 2FA 代码泄漏
    * 2FA 代码可重用性
    * 缺乏蛮力保护
    * 缺少 2FA 代码完整性验证
    * 带有 null 或 000000

## 我的账户（登录后）测试 

* 查找使用活动帐户用户 ID 的参数。 尝试篡改它以更改其他帐户的详细信息
* 创建仅与用户帐户相关的功能列表。 更改电子邮件 更改密码 - 更改帐户详细信息（姓名、号码、地址等）。 尝试 CSRF 
* 登录后更改电子邮件 ID 并使用任何现有电子邮件 ID 进行更新。 检查它是否在服务器端得到验证。 应用程序是否向新用户发送任何新的电子邮件确认链接？ 如果用户在某个时间范围内没有确认链接怎么办？ 
* 在新选项卡中打开个人资料图片并检查 URL。 查找电子邮件 ID/用户 ID 信息。 EXIF 地理位置数据未从上传的图像中剥离。 
* 如果应用程序提供，请检查帐户删除选项并通过忘记密码功能确认
* 更改email id、account id、user id参数并尝试暴力破解其他用户的密码
* 检查应用程序是否重新进行身份验证以执行身份验证后功能的敏感操作 

## 忘记密码测试

* 注销和密码重置时会话无效
* 检查是否忘记密码重置链接/代码唯一性
* 如果用户在一段时间内未使用重置链接，请检查重置链接是否会过期
* 查找用户帐号识别参数并篡改Id或参数值以更改其他用户的密码
* 检查弱密码策略
* 弱密码重置实现Token使用后不失效 
* 如果重置链接有另一个参数，例如日期和时间，则。 更改日期和时间值以建立有效且有效的重置链接 
* 检查是否询问安全问题？ 允许多少猜测？ ⟶ 停工政策是否维持？
* 仅在新密码和确认密码中添加空格。 然后回车看看结果
* 完成忘记密码手续后是否在同一页面显示旧密码？
* 要求提供两个密码重置链接并使用用户电子邮件中的旧链接
* 检查活动会话是否在更改密码时被破坏？
* 弱密码重置实现 通过 HTTP 发送的密码重置令牌
* 发送连续忘记密码请求，以便它可以发送顺序令牌 

## “请联系我们”测试

* 验证码是否在联系我们表单上实施以限制电子邮件泛滥攻击？
* 它允许在服务器上上传文件吗？
* 盲XSS 

## 产品采购测试 

* 立即购买
    * 篡改产品ID以低价购买其他高价值产品
    * 篡改产品数据以增加同奖产品数量 
* 礼品券
    * 篡改请求中的礼物/代金券计数（如果有）以增加/减少要使用的代金券/礼物数量 
    * 篡改礼品/代金券价值以增加/减少代金券的货币价值。 （例如，100 美元作为代金券，篡改价值以增加、减少金钱） 
    * 通过在参数篡改中使用旧礼物值来重用礼物/凭证
    * 检查礼物/优惠券参数的唯一性并尝试猜测其他礼物/优惠券代码 
    * 在 BurpSuite 请求中使用 & 再次添加相同的参数名称和值，使用参数污染技术两次添加相同的凭证 
* 从购物车中添加/删除产品 
    * 篡改用户 ID 以从其他用户的购物车中删除产品
    * 篡改购物车 ID 以添加/删除其他用户购物车中的产品
    * 为购物车功能识别购物车 ID/用户 ID，以查看其他用户帐户中添加的商品 
* 地址
    * 篡改 BurpSuite 请求将其他用户的送货地址更改为您的地址
    * 通过在送货地址上添加 XSS 向量来尝试存储的 XSS 
    * 使用参数污染技术添加两个送货地址，而不是尝试操纵应用程序在两个送货地址上发送相同的项目 
* 下订单 
    * 篡改付款选项参数以更改付款方式。 例如。 考虑到某些商品不能以货到付款方式订购，但是将借记/信用卡/PayPal/网上银行选项中的请求参数篡改到货到付款可能允许您为该特定商品下订单 
    * 在每个主和子请求和响应中篡改支付操作的金额值
    * 检查 CVV 是否以明文形式运行 
    * 检查应用程序本身是否会处理您的卡详细信息然后执行交易，或者它会调用任何第三方支付处理公司来执行交易 
* 跟踪订单 
    * 通过猜测订单跟踪号来跟踪其他用户的订单
    * 暴力追踪号码前缀或后缀以追踪其他用户的批量订单
* 愿望清单页面测试
    * 检查用户A是否可以在其他用户B的账户的Wishlist中添加/远程产品
    * 检查用户 A 是否可以从他/她（用户 A）的愿望清单部分将产品添加到用户 B 的购物车中。
* 产品购买后测试
    * 检查用户A是否可以取消用户B购买的订单
    * 检查用户 A 是否可以查看/检查用户 B 已经下的订单
    * 检查用户A是否可以修改用户B下订单的送货地址
* 带外测试
    * 用户可以订购缺货的产品吗？ 

## 银行应用测试 

* 结算活动 
    * 检查用户“A”是否可以查看用户“B”的对帐单
    * 检查用户“A”是否可以查看用户“B”的交易报告
    * 检查用户“A”是否可以查看用户“B”的摘要报告
    * 检查用户“A”是否可以代表用户“B”通过电子邮件注册每月/每周的帐户对帐单 
    * 检查用户 'A' 是否可以更新用户 'B' 的现有电子邮件 ID 以检索每月/每周帐户摘要 
* 存款/贷款/关联/外部账户检查 
    * 检查用户'A'是否可以查看用户'B'的存款账户摘要
    * 检查存款账户的账户余额篡改 
* 扣税查询测试 
    * 检查用户 'A' 的客户 ID 'a' 是否可以通过篡改他/她的客户 ID 'b' 来查看用户 'B' 的税收减免详情 
    * 检查参数篡改增减利率、利息金额、退税
    * 检查用户'A'是否可以下载用户'B'的TDS详细信息 
* 检查用户“A”是否可以代表用户“B”请求支票簿。 
* 定期存款账户测试 
    * 检查用户'A'是否可以代表用户'B'开设FD账户
    * 检查用户是否可以开设比当前账户余额更多的 FD 账户
* 根据支票/日期范围停止付款
    * 用户“A”可以通过支票号码停止向用户“B”付款吗
    * 用户“A”是否可以根据用户“B”的日期范围停止付款
* 状态查询测试
    * 用户“A”能否查看用户“B”的状态查询
    * 用户'A'可以修改用户'B'的状态查询吗
    * 用户“A”能否代表用户“B”从自己的账户发帖和查询 
* 资金转移测试 
    * 是否可以将资金从用户“A”转移到用户“C”而不是用户“B”，后者旨在从用户“A”转移到用户“B” 
    * 转账金额可以被操纵吗？
    * 用户'A'可以使用自己的账户通过参数操作修改用户'B'的收款人列表吗
    * 是否可以在用户 'A' 自己的帐户或用户 'B' 的帐户中添加收款人而无需任何适当的验证 
* 安排转移测试
    * 用户“A”能否查看用户“B”的调度传输
    * 用户“A”是否可以更改用户“B”的计划转移的详细信息
* 通过 NEFT 测试资金转移
    * 通过 NEFT 转账进行金额操作
    * 检查用户'A'是否可以查看用户'B'的NEFT转账详情
* 账单支付测试
    * 检查用户是否可以在没有任何检查员批准的情况下注册收款人
    * 检查用户“A”是否可以查看用户“B”的待付款
    * 检查用户“A”是否可以查看用户“B”的付款详情 

## 开放重定向测试 

* 常用注射参数 

    ```
    /{payload}
    ?next={payload}
    ?url={payload}
    ?target={payload}
    ?rurl={payload}
    ?dest={payload}
    ?destination={payload}
    ?redir={payload}
    ?redirect_uri={payload}
    ?redirect_url={payload}
    ?redirect={payload}
    /redirect/{payload}
    /cgi-bin/redirect.cgi?{payload}
    /out/{payload}
    /out?{payload}
    ?view={payload}
    /login?to={payload}
    ?image_url={payload}
    ?go={payload}
    ?return={payload}
    ?returnTo={payload}
    ?return_to={payload}
    ?checkout_url={payload}
    ?continue={payload}
    ?return_path={payload}
    ```

* 使用 burp 'find' 选项来查找参数，例如 URL、red、redirect、redir、origin、redirect_uri、target 等
* 检查这些可能包含 URL 的参数的值
* 将 URL 值更改为 www.tushar.com 并检查是否被重定向
* 尝试单斜线和 url 编码
* 使用列入白名单的域或关键字
* 使用 // 绕过 http 黑名单关键字
* 使用 https: 绕过 // 列入黑名单的关键字
* 使用 \\ 绕过 // 列入黑名单的关键字
* 使用 \/\/ 绕过 // 列入黑名单的关键字
* 使用空字节 %00 绕过黑名单过滤器
* 使用°符号绕过 

## HOST头注入

* 提供任意 Host 标头
* 检查有缺陷的验证
* 发送不明确的请求
    * 注入重复的主机标头
    * 提供绝对 URL
    * 添加换行
* 注入主机覆盖标头 

## SQL注入

* 入口点检测

    * 简单字符
    * 多重编码
    * 合并字符
    * 逻辑测试
    * 奇怪的字符

* 使用SQLmap识别漏洞参数

    * 在浏览器GUI中填写表单正常提交
    * 转到 burpsuite 中的历史记录选项卡并找到相关请求
    * 右键单击并选择“复制到文件”选项
    * 将文件另存为 anyname.txtWeb 应用程序渗透测试清单 8
    * 要运行的 SQLmap 命令
    * `python sqlmap.py r ~/Desktop/textsqli.txt proxy=http://127.0.0.1:8080`

* 对所有请求运行 SQL 注入扫描程序

* 绕过WAF

    * 在 SQL 查询之前使用空字节
    * 使用 SQL 内联注释序列
    * 网址编码
    * 更改大小写（大写/小写）
    * 使用 SQLMAP 篡改脚本 

* 时间延迟

    ```
    Oracle 			dbms_pipe.receive_message(('a'),10)
    Microsoft 		WAITFOR DELAY '0:0:10'
    PostgreSQL 		SELECT pg_sleep(10)
    MySQL 			SELECT sleep(10)
    ```

* 条件延迟

    ```
    Oracle 			SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN 									'a'||dbms_pipe.receive_message(('a'),10) ELSE NULL END FROM du
    Microsoft 		IF (YOUR-CONDITION-HERE) WAITFOR DELAY '0:0:10'
    PostgreSQL 		SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN pg_sleep(10) ELSE 					pg_sleep(0) END
    MySQL 			SELECT IF(YOUR-CONDITION-HERE,sleep(10),'a')
    ```

## XSS测试

* 使用 infosecguy 的 QuickXSS 工具尝试 XSS
* 使用` '"><img src=x onerror=alert(document.domain)>.txt` 上传文件
* 如果脚本标签被禁止，使用 `<h1> `和其他 HTML 标签
* 如果输出作为任何变量的值反映在 JavaScript 内部，只需使用 `alert(1)`
* 如果` "` 被过滤，则使用此有效负载 `/><img src=d onerror=confirm(/tushar/);>`
* 使用图像文件上传 JavaScript
* 执行 JS 负载的不寻常方法是将方法从 POST 更改为 GET。 它有时会绕过过滤器 
* 标签属性值 

    * 输入登陆 `<input type="text" name="state" value="INPUT_FROM_USER">`
    * 要插入的有效负载-`" onfocus="alert(document.cookie)"`
* 语法编码有效负载`%3cscript%3ealert(document.cookie)%3c/script%3e`
* XSS 过滤器绕过

    * < 和 > 可以替换为 html 实体 `&lt; `和` &gt;` 
* 你可以试试 XSS 多语言。比如：`-javascript:/→</title></style></textarea></script></xmp><svg/onload='+/"/+/onmouseover=1/+/[/[]/+alert(1)//'>`
* XSS防火墙绕过
    * 检查防火墙是否只阻止小写
    * 尝试用新行打破防火墙正则表达式(\r\n)
    * 尝试双重编码 
    * 测试递归过滤器
    * 注入没有空格的锚标记
    * 尝试使用 Bullet 绕过空格
    * 尝试更改请求方法 

## CSRF测试

* CSRF 令牌的验证取决于请求方法
* CSRF 令牌的验证取决于是否存在令牌
* CSRF 令牌不绑定到用户会话
* CSRF 令牌绑定到非会话 cookie
* Referer 的验证取决于是否存在标头 

## SAML 漏洞 

* 签名包装 (XSW) 攻击
* SAML 消息完整性滥用
* 缺少/无效签名
* SAML 消息重放
* 代币接收者的困惑 

## XML注入测试

* 将内容类型更改为 text/xml 然后插入下面的代码。 通过中继器检查 

    ```
    <?xml version="1.0" encoding="ISO 8859 1"?>
    <!DOCTYPE tushar [
    <!ELEMENT tushar ANY
    <!ENTITY xxe SYSTEM "file:///etc/passwd" >]><tushar>&xxe;</
    <!ENTITY xxe SYSTEM "file:///etc/hosts" >]><tushar>&xxe;</
    <!ENTITY xxe SYSTEM "file:///proc/self/cmdline" >]><tushar>&xxe;</
    <!ENTITY xxe SYSTEM "file:///proc/version" >]><tushar>&xxe;</
    ```

* 带外交互的盲 XXE 

## 跨域资源共享（CORS）

* 解析 Origin 标头时出错
* 白名单空原值

## 服务器端请求伪造（SSRF）

* 常用注射参数 

    ```
    "access=",
    "admin=",
    "dbg=",
    "debug=",
    "edit=",
    "grant=",
    "test=",
    "alter=",
    "clone=",
    "create=",
    "delete=",
    "disable=",
    "enable=",
    "exec=",
    "execute=",
    "load=",
    "make=",
    "modify=",
    "rename=",
    "reset=",
    "shell=",
    "toggle=",
    "adm=",
    "root=",
    "cfg=",
    "dest=",
    "redirect=",
    "uri=",
    "path=",
    "continue=",
    "url=",
    "window=",
    "next=",
    "data=",
    "reference=",
    "site=",
    "html=",
    "val=",
    "validate=",
    "domain=",
    "callback=",
    "return=",
    "page=",
    "feed=",
    "host=",
    "port=",
    "to=",
    "out=",
    "view=",
    "dir=",
    "show=",
    "navigation=",
    "open=",
    "file=",
    "document=",
    "folder=",
    "pg=",
    "php_path=",
    "style=",
    "doc=",
    "img=",
    "filename="
    ```

* 尝试基本的本地主机负载

* 绕过过滤器

    * 使用 HTTPS 绕过
    * 用 [::] 绕过
    * 通过域重定向绕过
    * 使用十进制 IP 位置绕过
    * 使用 IPv6/IPv4 地址嵌入绕过
    * 使用格式错误的网址绕过
    * 使用稀有地址绕过（通过删除零的短手 IP 地址）
    * 使用封闭的字母数字绕过 

* 云实例 

    * AWS

        ```
        http://instance-data
        http://169.254.169.254
        http://169.254.169.254/latest/user-data
        http://169.254.169.254/latest/user-data/iam/security-credentials/[ROLE NAME]
        http://169.254.169.254/latest/meta-data/
        http://169.254.169.254/latest/meta-data/iam/security-credentials/[ROLE NAME]
        http://169.254.169.254/latest/meta-data/iam/security-credentials/PhotonInstance
        http://169.254.169.254/latest/meta-data/ami-id
        http://169.254.169.254/latest/meta-data/reservation-id
        http://169.254.169.254/latest/meta-data/hostname
        http://169.254.169.254/latest/meta-data/public-keys/
        http://169.254.169.254/latest/meta-data/public-keys/0/openssh-key
        http://169.254.169.254/latest/meta-data/public-keys/[ID]/openssh-key
        http://169.254.169.254/latest/meta-data/iam/security-credentials/dummy
        http://169.254.169.254/latest/meta-data/iam/security-credentials/s3access
        http://169.254.169.254/latest/dynamic/instance-identity/document
        ```

    * Google Cloud

        ```
        http://169.254.169.254/computeMetadata/v1/
        http://metadata.google.internal/computeMetadata/v1/
        http://metadata/computeMetadata/v1/
        http://metadata.google.internal/computeMetadata/v1/instance/hostname
        http://metadata.google.internal/computeMetadata/v1/instance/id
        http://metadata.google.internal/computeMetadata/v1/project/project-id
        ```

    * Digital Ocean

        ```
        curl http://169.254.169.254/metadata/v1/id
        http://169.254.169.254/metadata/v1.json
        http://169.254.169.254/metadata/v1/
        http://169.254.169.254/metadata/v1/id
        http://169.254.169.254/metadata/v1/user-data
        http://169.254.169.254/metadata/v1/hostname
        http://169.254.169.254/metadata/v1/region
        http://169.254.169.254/metadata/v1/interfaces/public/0/ipv6/address
        ```

    * Azure

        ```
        http://169.254.169.254/metadata/v1/maintenance
        http://169.254.169.254/metadata/instance?api-version=2017-04-02
        http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2017-04-02&format=text
        ```

* 通过开放重定向绕过 

## 文件上传测试

* 将恶意文件上传到存档上传功能并观察应用程序如何响应
* 上传文件并更改其路径以覆盖现有系统文件
* 大文件拒绝服务
* 元数据泄露
* ImageMagick 库攻击
* 像素洪水攻击
* 绕过 
    * 空字节 （%00） 绕过
    * 内容类型绕过
    * 魔术字节绕过
    * 客户端验证绕过
    * 黑名单扩展绕过
    * 同形异义字符绕过 

## 验证码测试 

* 缺少验证码字段完整性检查
* HTTP 动词操作
* 内容类型转换
* 可重复使用的验证码
* 检查验证码是否可以使用绝对路径检索，例如 `www.tushar.com/internal/captcha/images/24.png`
* 检查服务器端验证的 CAPTCHA.Remove captcha 块从 GUI 使用 firebug 插件并向服务器提交请求 
* 检查图像识别是否可以使用OCR工具进行？ 

## JWT Token测试

* 暴力破解秘钥
* 使用“none”算法签署新令牌
* 更改令牌的签名算法（用于模糊测试）
* 将非对称签名的令牌签名为其对称算法匹配（当您拥有原始公钥时） 

## Websockets测试 

* 拦截和修改 WebSocket 消息
* Websockets MITM 尝试
* 测试秘密头 websocket
* websockets中的内容窃取
* websockets中的令牌认证测试 

## GraphQL 漏洞测试

* 不一致的授权检查
* 缺少自定义标量的验证
* 未能适当地限制速率
* 自省查询启用/禁用

## WordPress 常见漏洞

* WordPress 中的 XSPA
* wp-login.php 中的暴力破解
* 信息公开 wordpress 用户名
* 备份文件 wp-config 暴露
* 日志文件暴露
* 通过 load-styles.php 拒绝服务
* 通过 load-scripts.php 拒绝服务
* 使用 xmlrpc.php 的 DDOS

## 拒绝服务

* 饼干炸弹
* 像素泛滥，使用具有巨大像素的图像
* 帧泛滥，使用带有巨大帧的 GIF
* ReDoS（正则表达式 DoS）
* CPDoS（缓存中毒拒绝服务） 

## 其他测试用例（所有类别） 

* 检查安全标头，至少检查下面这些
    * X 框架选项
    * X-XSS 标头
    * HSTS 标头
    * CSP 标头
    * 推荐人政策
    * 缓存控制
    * 公钥引脚
*  角色授权测试 
    * 检查普通用户是否可以访问高权限用户的资源？ 
    * 强制浏览
    * 不安全的直接对象引用
    * 参数篡改将用户账号切换为高权限用户 
* 盲操作系统命令注入
    * 使用时间延迟
    * 通过重定向输出
    * 带外交互
    * 带外数据泄露
* CSV 导出命令注入（上传/下载）
* CSV Excel 宏注入
* 如果您发现 phpinfo.php 文件，请检查配置泄漏并尝试利用任何网络漏洞。
* 参数污染社交媒体分享按钮
* 破译密码术
    * 密码学实现缺陷
    * 加密信息泄露
    * 用于加密的弱密码
* 网络服务测试
    * 测试目录遍历
    * Web 服务文档披露服务、数据类型、输入类型边界和限制的枚举 



# Check List - 特性

## 中间件&组件

- shiro
- fastjson
- jackson
- xstream
- weblogic
- ueditor
- ...

## 框架

- 致远OA
    - Rce **需要具体给出cve 以及对应poc/文章介绍**
- 通达OA
- Thinkphp
- druid  [druid未授权访问](http://www.yulinsec.com:28120/pages/viewpage.action?pageId=2097306)
- 安全设备**（需要具体列举）**
- 泛微
- ...

## 服务

- 数据库
    - mysql
    - redis
    - mssql
    - 
    - ...
- rdp
- vnc
- ssh

## 服务端

- iis 
    - 畸形解析（iis < 8.0）
    - 短文件名猜解
- apache
    - 畸形解析
- nginx
    - 



# 从OSWAP搬运：

参考：`https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/02-Fingerprint_Web_Server`

对目前测试学校站点曾经出现过的漏洞类型标成黑体

## 信息收集

搜索引擎

服务器指纹识别

网站的元信息

WA枚举

**html文件信息泄露**

应用程序的入口点 （请求方法，端点，参数，报头）

路径映射

框架指纹识别

后端服务器架构（WAF，反代，服务器，数据库）

## 配置和部署管理测试

**服务器的错误配置（默认配置），服务器管理工具（服务器版本管理等等），服务器的CVE**

**应用平台配置（服务器默认存在的文件，debug信息泄露，日志文件泄露）**

测试服务器如何处理敏感信息的拓展名，*.tar，*.zip文件下载，*.phTml畸形绕过

弃用文件检测 asp.old，*.bak

隐藏的管理员接口枚举  /admin/* ，cookie中修改admin=1

测试允许的HTTP请求（有危害的比如PUT，TRACE），权限控制绕过，HTTP请求方法覆写（X-HTTP-Method）

HTTPS有效性

跨域策略设置

测试文件权限（服务器端设置的rwx权限）

DNS接管

云存储的访问配置

## 身份管理测试

身份定义测试，如尝试区分身份、测试身份的权限、切换身份

**测试注册过程**

测试账号配置过程，如管理员添加用户

测试账号枚举和账户猜测

测试弱用户名策略，比如用户名只能为1，2，3等等，容易枚举和猜测

### 测试身份鉴定（authentication）

测试是否交换不加密的凭据

**测试弱凭据，新用户的默认密码**

**测试弱锁定机制（抗暴力破解能力）**

绕过身份验证（sql万能密码，session预测等等）

容易受到攻击的记住密码测试

浏览器缓存弱点测试

余下参考原链接

### 测试授权（Authorization）

测试文件包含导致的目录遍历

**测试平行越权或者垂直越权**

权限提升测试

**测试不安全的直接对象引用（通过改变id遍历数据或者文件，感觉包含在越权里面）**

### 会话管理测试

cookie收集、会话分析、cookie逆向工程、cookie爆破

cookie属性测试

会话固定测试

测试暴露的会话变量

CSRF测试

测试注销功能

测试会话超时

Session fuzzing

会话劫持测试

### 输入验证测试

**SQL注入**

**XSS注入**

余下参考原链接

### 错误处理测试

余下参考原链接

### 弱加密测试

余下参考原链接

### 逻辑漏洞测试

余下参考原链接

### 客户端测试

余下参考原链接