## NetOps_v2.0_beta

一个使用`nornir`框架编写的跑脚本工具

`main`分支是在windows平台下运行的脚本

`ubuntu-branch`分支是在ubuntu server下运行的脚本（其他linux发行版，应该也可以）

更多详细介绍，移步Blog：https://kiraster.github.io/posts/9571d5ee.html

![ScreenCaputure230506035629](https://s2.loli.net/2023/05/06/sWZdHkmLDlqevxB.jpg)

## 测试环境

### windows

- Microsoft Windows 10 Pro 21H2
- Visual studio code Update 1.77.3
- Python 3.10.10
- nornir==3.3.0

### Ubuntu 

- Ubuntu 22.04.2 LTS
- Python 3.10.6
- nornir==3.3.0

### Simulation Software 

- HCL 5.7.2
- DeviceModel：H3C S5820V2-54QS-GE

## Topology

![lab_test](https://s2.loli.net/2023/05/05/L7nI9fTp3zEk6Rq.png)

## 功能

1. 批量备份配置
   - 根据加载的设备清单，读取ssh登陆信息登陆设备，执行display列中的display命令，将回显内容写入到`EXPORT\当天日期\export_conf`文件夹下，每个设备的回显内容分别记录在一个txt文件(格式：name + ip + 当前时间.txt)，运行结果记录在`EXPORT\当天日期\result_当天日期.log`文件
2. 批量修改配置
   - 根据加载的设备清单，读取ssh登陆信息登陆设备，执行config列中的config命令，将回显内容写入到`EXPORT\当天日期\modify_conf`文件夹下，每个设备的回显内容分别记录在一个txt文件(格式：name + ip + 当前时间.txt)，运行结果记录在`EXPORT\当天日期\result_当天日期.log`文件
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
   - 该功能通过获取交换机MAC地址表和trunk接口信息，求差集获取到非trunk接口的MAC地址表，表格文件存储到`EXPORT\当天日期\generate_table`，格式为：`当天日期_当前时间_MAC地址表.xlsx`
   - 强烈建议在代码`task.run`前进行filter过滤接入交换机的`nr对象`
   - 运行结果记录在`EXPORT\当天日期\result_当天日期.log`文件
5. 搜索MAC地址对应设备
   - 本功能依赖功能4中生成的MAC地址表，需要使用本功能先执行功能4
   - 输入的MAC地址格式任意，可以是全匹配如：4426-0f92-0d06，也可以是其中部分如：0d06 或 4426，或者任意字符（没有意义）
6. 批量snmp轮询
   - 根据加载的设备清单，执行snmp_get操作，将获取到的结果写入到SNMP轮询结果表，表格文件存储到`EXPORT\当天日期\generate_table`，格式为：`当天日期_当前时间_snmp轮询结果表.xlsx`
   - 运行结果记录在`EXPORT\当天日期\result_当天日期.log`文件
6. 批量ssh可达性测试
   - 根据加载的设备清单，读取ssh登陆信息登陆设备，以获取到设备的`prompt`作为依据判断ssh可达，运行结果记录在`EXPORT\当天日期\result_当天日期.log`文件
7. 批量ping可达性测试
   - 根据加载的设备清单，执行ping操作，以没有异常作为依据判断ping可达，运行结果记录在`EXPORT\当天日期\result_当天日期.log`文件
8. 批量保存配置
   - 根据加载的设备清单，执行`netmiko_save_config`操作，以没有异常作为依据判断保存成功，运行结果记录在`EXPORT\当天日期\result_当天日期.log`文件
9. 显示设备清单
   - 根据加载的设备清单，列出['name', 'ip', 'platform', 'model', 'device_type', 'area', 'location', 'version', 'sn']等内容
11. 导出诊断信息和日志（TFTP）
    - 根据`nr.filter(hostname=device_ip)`过滤单台设备，对设备的诊断信息文件，诊断日志文件和日志文件上传到 TFTP 服务器


## 说明：

1. 在nornir 3.3.0框架上进行功能编写
2. 使用`nornir`自带的并发机制，专注于功能的实现
2. `nornir`具有与其他开源模块的联动功能，如`netbox`、`sql`、`scrapli`、`napalm`等，具有强扩展性

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
    5、保存配置
      同上
    0、返回上一级
4、获取交换机 端口-MAC地址
5、搜索MAC地址对应设备
6、批量snmp轮询
7、批量ssh可达性测试
8、批量ping可达性测试
9、批量保存配置
10、查看设备清单
11、导出诊断信息和日志（TFTP）
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


## 20230412 添加自定义textfsm 模板
1. 在`venv\Lib\site-packages\ntc_templates\templates\index`文件里添加记录

2. 添加`venv\Lib\site-packages\ntc_templates\templates\hp_comware_display_port_trunk_local.textfsm` 模板文件


## 20230413 添加根据 MAC 地址搜索对应设备
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

## 20230503 添加组合筛选（高级）代码

1. 使用eval，将字符串形式的代码直接转化成可执行的代码
2. 组合筛选格式：F对象（~取反 ），& 和 | 执行 AND 和 OR 运算组合筛选
3. 举例：进入对应菜单后直接输入-->> F(hostname='172.31.100.20') | F(area='JCW') 等形式字符串
4. 代码中使用eval()函数，带来一定的`麻烦`，后面想到解决办法再修改

## 20230504 添加 SNMP 轮询和修改 功能 4 和功能 5 文件生成

1. 新增 `6、批量snmp轮询`对设备进行内置OID（可在lib/do_polling.py文件修改）轮询
2. 添加lib/do_polling.py文件，根据传入的IP地址和只读团体字（SNMPv2)对设备进行轮询，并返回字典给上一步的函数
3. 修改`获取交换机 端口-MAC地址`功能，现在运行只生成一个表格文件（格式：当天日期_当前时间_MAC地址表.xlsx）
4. 修改`搜索MAC地址对应设备`功能，现在只搜索本次运行脚本最后一次生成的MAC地址表
5. 修改`EXPORT`下批量导出文件的开头格式为100个‘=’ + 命令字符串居中两头填充'='
6. 代码中使用eval()函数，带来一定的`麻烦`，后面想到解决办法再修改

## 20230505 添加 导出诊断信息和日志

1. 新增 `11、导出诊断信息和日志`功能
2. 对设备的诊断信息文件，诊断日志文件和日志文件上传到 TFTP 服务器
3. 目前的设置是使用`nr.filter(hostname=device_ip)`过滤后进行单台设备操作
4. 目前的设置只添加华三设备的导出方式（预留其他`platform`的elif判断）
5. 使用该功能前需要开启`TFTP`服务端软件

## 20230506 修改功能 4 和功能 6 生成的表格样式

1. 修改表格表头为全英文大写
2. 修改表格自动调整列宽
3. 移除无用代码和修改变量名

## 20230507 修改路径变量获取方式 移除无用代码 

1. 现在以comm.xx的方式获取对应的路径变量
2. 功能5 添加判断全局变量`mac_file_path`是否存在来执行搜索
3. 移除无用代码和无关注释
4. 调整部分代码缩进，添加必要注释
5. 减少代码中过多的执行`nr`初始化对象

## 20230512 修改send_multiline 添加参数和更新ubuntu-branch分支

1. 设备处理生成诊断文件需要反应时间，添加`delay_factor=30`
2. `main`分支功能同步更新到`ubuntu-branch`分支