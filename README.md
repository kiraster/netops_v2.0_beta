## NetOps_v2.0_beta

一个使用`nornir`框架编写的跑脚本工具

`main`分支是在windows平台下运行的脚本

`ubuntu-branch`分支是在ubuntu server下运行的脚本（其他linux发行版，应该也可以）

两个分支主要区别是路径的斜杠符号

更多详细介绍，移步Blog：https://kiraster.github.io/posts/9571d5ee.html

## 功能

1. 批量备份配置
   - 根据加载的设备清单，读取ssh登陆信息登陆设备，执行display列中的display命令，将回显内容写入到`EXPORT\当天日期\export_conf`文件夹下，每个设备的回显内容分别记录在一个txt文件(格式：name + ip + 当前时间.txt)，运行结果记录在`EXPORT\当天日期\result_当前日期.log`文件
2. 批量修改配置
   - 根据加载的设备清单，读取ssh登陆信息登陆设备，执行config列中的config命令，将回显内容写入到`EXPORT\当天日期\modify_conf`文件夹下，每个设备的回显内容分别记录在一个txt文件(格式：name + ip + 当前时间.txt)，运行结果记录在`EXPORT\当天日期\result_当前日期.log`文件
3. 筛选-->执行
   - 选择该功能选项后，会在二级菜单显示主菜单中的1、2、6、7、8功能
   - 选择对应功能后进入筛选菜单
   - 筛选菜单：
     -  IP地址-筛选
     -  平台-筛选
     -  设备型号-筛选
     -  区域-筛选
     -  组合筛选（未编写）
4. 获取交换机 端口-MAC地址  
   - 该功能通过获取交换机MAC地址表和trunk接口信息，求差集获取到非trunk接口的MAC地址表，表格文件存储到`EXPORT\当天日期\generate_table`，格式为：`当天日期_MAC地址表.xlsx`
   - 强烈建议在代码`task.run`前进行filter过滤接入交换机的`nr对象`
   - 运行结果记录在`EXPORT\当天日期\result_当前日期.log`文件
5. 搜索MAC地址对应设备
   - 本功能依赖功能4中生成的MAC地址表，需要使用本功能先执行功能4
   - 输入的MAC地址格式任意，可以是全匹配如：4426-0f92-0d06，也可以是其中部分如：0d06 或 4426，或者任意字符（没有意义）
6. 批量ssh可达性测试
   - 根据加载的设备清单，读取ssh登陆信息登陆设备，以获取到设备的`prompt`作为依据判断ssh可达，运行结果记录在`EXPORT\当天日期\result_当前日期.log`文件
7. 批量ping可达性测试
   - 根据加载的设备清单，执行ping操作，以没有异常作为依据判断ping可达，运行结果记录在`EXPORT\当天日期\result_当前日期.log`文件
8. 批量保存配置
   - 根据加载的设备清单，执行`netmiko_save_config`操作，以没有异常作为依据判断保存成功，运行结果记录在`EXPORT\当天日期\result_当前日期.log`文件
9. 显示设备清单
   - 根据加载的设备清单，列出['name', 'ip', 'platform', 'model', 'device_type', 'area', 'location', 'version', 'sn']等内容


## 说明：

1. nornir 3.3.0

2. 属于重构之前的netops，原版代码主要使用netmiko进行功能编写

**重构原因**

1. 摒弃旧版本自己写的异步并发和文件写入，使用`nornir`自带的并发机制，专注于功能的实现
2. `nornir`具有与其他开源模块的联动功能，如`netbox`、`sql`、`scrapli`、`napalm`等，具有强扩展性
3. 原有代码结构臃肿、难维护、设计不合理、功能杂乱

## 20230407 功能结构

```
1、批量备份配置
2、批量修改配置
3、筛选-->执行
    1、备份配置
        1、IP地址-筛选（格式：192.168.1.1,192.168.1.0/24,192.168.1.1-192.168.1.254）
        2、平台-筛选（huawie、hp_comvare、...)
        3、设备型号-筛选(H3C S6850、...)
        4、区域-筛选（JCW、AFW、...)
        5、组合筛选（高级）
        0、返回上一级
    2、修改配置
    	同上
    3、ssh测试
    	同上
    4、ping测试
    	同上
    0、返回上一级
4、获取交换机 端口-MAC地址
5、搜索MAC地址对应设备
7、批量ssh可达性测试
8、批量ping可达性测试
9、批量保存配置
10、查看设备清单
0、退出
```

## 20230408 添加 tqdm 和 progress 进度条

1. 使用 on_failed=True, 代码减少过多的inventory初始化
2. 由于进程数设置过大，而模拟器设备达不到进程数，所以显示两行，把nornir.yaml 配置项中的num_workers 设为1或2观察效果
3. 由于task运行的任务耗时少，效果也会显得不明显，可添加time.sleep(5)观察效果


## 20230409 添加 raise Exception(e)
1. 不使用task任务而产生的异常，抛出异常在任务执行最后打印在控制台
2. 通过制造异常的方式把异常和制造的异常写入nornir.log

## 20230410 添加一层嵌套，实现一定安全性
1. inventory.xlsx添加打开密码

2. 原netops_start.py移动到func文件夹并改名为func_list.py


**一定安全性的实现说明：**

1. 嵌套最外层的启动文件，启动后判断不带打开密码的excel文件是否存在，如不存在则进行密码输入实现第二步的操作

2. 读取有打开密码的excel文件

3. 复制一份不带打开密码的excel文件在inventory文件夹下

4. 退出程序的时自动执行销毁不带打开密码的excel文件

5. 销毁的excel文件不能通过回收站找回

6. 能找到不带打开密码的文件，仅在生成该文件时，手动另存为


## 20230412 添加自定义textfsm模板
1. 在`venv\Lib\site-packages\ntc_templates\templates\index`文件里添加记录

2. 添加`venv\Lib\site-packages\ntc_templates\templates\hp_comware_display_port_trunk_local.textfsm` 模板文件


## 20230413 添加根据MAC地址搜索对应设备
1. 要求先获取设备MAC地址表，当天日期

2. 输入的MAC地址格式任意，可以是全匹配如：4426-0f92-0d06，也可以是其中部分如：0d06 或 4426，或者任意字符（没有意义）

## 20230417 添加打印设备清单

1. 安装prettytable

2. for循环`nr.inventory.hosts.items()`获取数据，最后打印

## 20230417 修改 筛选-->执行 功能下 IP地址-筛选的格式

1. 现在可以输入IP地址、IP网段、IP范围任意组合
2. 输入的内容要求以逗号分割，例如：192.168.1.1,192.168.1.0/24,192.168.1.1-192.168.1.254
3. 以上输入的内容经过函数处理后，如果都是正确格式的元素，会返回一个列表再接下来的步骤处理，即使输入的是单个IP地址或IP网段或范围

## 20230428 修改 msoffcrypto 替换 pywin32 库

1. 使用msoffcrypto库替换pywin32库，因为这个pywin32只能windows平台使用
2. 过些天会传一份在ubuntu server环境下的代码修改版到一个分支

## 20230429 ubuntu-branch 分支

1. 添加ubuntu-branch 分支
2. 该分支在ubuntu server 22.04 系统下进行测试

## 20230501 修改 result_xxx.log 生成文件的title包含任务描述

1. 修改/func/func_list.py，增加替换返回task_desc
2. 修改/lib/comm.py，修改装饰器对应的代码接收处理task_desc
