[toc]

## Windows 日志

### Windows 日志路径

```powershell
系统日志：%SystemRoot%\System32\Winevt\Logs\System.evtx
安全日志：%SystemRoot%\System32\Winevt\Logs\Security.evtx
应用程序日志：%SystemRoot%\System32\Winevt\Logs\Application.evtx

日志在注册表的键：HKEY_LOCAL_MACHINE\system\CurrentControlSet\Services\Eventlog
```

### Windows 日志清除方式

1. **最简单粗暴的方式**

开始→运行,输入 `eventvwr` 进入事件查看器，右边栏选择清除日志。

2. **命令行一键清除Windows事件日志**

```powershell
PowerShell -Command "& {Clear-Eventlog -Log Application,System,Security}"

Get-WinEvent -ListLog Application,Setup,Security -Force | % {Wevtutil.exe cl $_.Logname}
```

3. **利用脚本停止日志的记录**

通过该脚本遍历事件日志服务进程（专用svchost.exe）的线程堆栈，并标识事件日志线程以杀死事件日志服务线程。

因此，系统将无法收集日志，同时事件日志服务似乎正在运行。

> https://github.com/hlldz/Invoke-Phant0m

4. **Windows单条日志清除**

该工具主要用于从Windows事件日志中删除指定的记录。

> https://github.com/QAX-A-Team/EventCleaner

5. **Windows日志伪造**

使用eventcreate这个[命令行工具](https://cloud.tencent.com/product/cli?from=10680)来伪造日志或者使用自定义的大量垃圾信息覆盖现有日志。

```powershell
eventcreate -l system -so administrator -t warning -d "this is a test" -id 500
```

## IIS日志

### IIS默认日志路径

```powershell
%SystemDrive%\inetpub\logs\LogFiles\W3SVC1\
```

### 清除WWW日志

```powershell
停止服务：net stop w3svc
删除日志目录下所有文件：del *.*
启用服务：net start w3svc
```

## 文件删除

### Shift+Delete

直接删除文件，还是能在回收站找到的，使用Shift+Delete快捷键可以直接永久删除了。但是用数据恢复软件，删除的文件尽快恢复，否则新的文件存入覆盖了原来的文件痕迹就很难恢复了。

### Cipher 命令多次覆写

在删除文件后，可以利用Cipher 命令通过 /W 参数可反复写入其他数据覆盖已删除文件的硬盘空间，彻底删除数据防止被恢复。

比如，删除`D:\tools`目录下的文件，然后执行这条命令：

```powershell
cipher /w:D:\tools
```

这样一来，D 盘上未使用空间就会被覆盖三次：一次 0x00、一次 0xFF，一次随机数，所有被删除的文件就都不可能被恢复了。

### Format命令覆盖格式化

Format 命令加上 /P 参数后，就会把每个扇区先清零，再用随机数覆盖。而且可以覆盖多次。比如：

```powershell
format D: /P:8
```

这条命令表示把 D 盘用随机数覆盖 8 次。

## 清除远程桌面连接记录

当通过本机远程连接其他客户端或服务器后，会在本机存留远程桌面连接记录。代码保存为`clear.bat`文件，双击运行即可自动化清除远程桌面连接记录。

```powershell
@echo off
reg delete "HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Default" /va /f
reg delete "HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Servers" /f
reg add "HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Servers"
cd %userprofile%\documents\
attrib Default.rdp -s -h
del Default.rdp
```

## Metasploit 痕迹清除

### 查看事件日志

```powershell
meterpreter > run event_manager  -i   
[*] Retriving Event Log Configuration

Event Logs on System
====================

 Name                    Retention  Maximum Size  Records
 ----                    ---------  ------------  -------
 Application             Disabled   20971520K     2149
 HardwareEvents          Disabled   20971520K     0
 Internet Explorer       Disabled   K             0
 Key Management Service  Disabled   20971520K     0
 Security                Disabled   20971520K     1726
 System                  Disabled   20971520K     3555
 Windows PowerShell      Disabled   15728640K     138
```

### 清除事件日志

> 包括六种日志类型

```powershell
meterpreter > run event_manager  -c
```

### clearv命令

> 清除目标系统的事件日志，仅包含三种日志类型

```powershell
meterpreter > clearev 
[*] Wiping 4 records from Application...
[*] Wiping 8 records from System...
[*] Wiping 7 records from Security...
```

