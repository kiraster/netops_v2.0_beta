'''
功能菜单
'''
from os import system
from datetime import datetime
import os
import sys
import atexit

from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from tqdm import tqdm
from progress.bar import Bar
from prettytable import PrettyTable
from termcolor import colored

sys.path.append("")
from lib import comm

# 定义一个没什么用的头
welcome_str = '`LIFE IS A FUCKING MOVIE`'

# 初始化创建一个 Nornir 对象
nr = InitNornir(config_file=comm.BASE_PATH + "\\nornir.yaml")


# 1、批量备份配置
# 记录程序执行时间装饰器
@comm.timer
# 记录运行结果的装饰器
@comm.result_count
# 保存运行结果记录的装饰器
@comm.result_write
def export_conf():

    # tqdm 进度条 参数
    pbar = tqdm(total=len(nr.inventory.hosts),
                desc="Running tasks on devices",
                unit="device(s)",
                colour='green')

    import export_conf

    task_desc = 'TASK: Export Configuration Of Device'
    results = nr.run(task=export_conf.export_conf,
                     pbar=pbar,
                     name=task_desc,
                     on_failed=True)
    pbar.close()

    # Nornir task 任务执行失败的主机
    failed_hosts = list(results.failed_hosts.keys())
    # 生成用于统计主机的列表，统计并打印在任务结束末尾
    hosts_list, failed_hosts_list = comm.create_count_list(nr, failed_hosts)
    print_result(results)
    return hosts_list, failed_hosts_list, task_desc


# 2、批量修改配置
@comm.timer
@comm.result_count
@comm.result_write
def modify_conf():

    pbar = tqdm(total=len(nr.inventory.hosts),
                desc="Running tasks on devices",
                unit="device(s)",
                colour='green')

    import modify_conf

    task_desc = 'TASK: Modify Configuration Of Device'
    results = nr.run(task=modify_conf.modify_conf,
                     pbar=pbar,
                     name=task_desc,
                     on_failed=True)
    pbar.close()

    # Nornir task 任务执行失败的主机
    failed_hosts = list(results.failed_hosts.keys())
    hosts_list, failed_hosts_list = comm.create_count_list(nr, failed_hosts)
    print_result(results)
    return hosts_list, failed_hosts_list, task_desc


# 3、筛选-->>执行 批量任务
@comm.timer
@comm.result_count
@comm.result_write
def filter_run():

    import filter_nr

    # 打印选项，输入对应数字，进行下一步，输入数字0返回上一级
    while True:
        print('-' * 42)
        print('''
        1、备份配置
        2、修改配置
        3、ssh测试
        4、ping测试
        5、保存配置
        0、返回上一级
        ''')
        print('-' * 42)

        choice = input('输入数字编号：').strip()

        if choice == '0':
            run()

        elif choice == '1':
            # 1、备份配置
            nr = filter_nr.run_filter()
            pbar = tqdm(total=len(nr.inventory.hosts),
                        desc="Running tasks on devices",
                        unit="device(s)",
                        colour='green')

            import export_conf

            task_desc = 'TASK: Export Configuration Of Device'
            results = nr.run(task=export_conf.export_conf,
                             pbar=pbar,
                             name=task_desc,
                             on_failed=True)
            pbar.close()
            # Nornir task 任务执行失败的主机
            failed_hosts = list(results.failed_hosts.keys())
            hosts_list, failed_hosts_list = comm.create_count_list(
                nr, failed_hosts)
            print_result(results)
            return hosts_list, failed_hosts_list, task_desc

        elif choice == '2':
            # 2、修改配置
            nr = filter_nr.run_filter()
            pbar = tqdm(total=len(nr.inventory.hosts),
                        desc="Running tasks on devices",
                        unit="device(s)",
                        colour='green')

            import modify_conf

            task_desc = 'TASK: Modify Configuration Of Device'
            results = nr.run(task=modify_conf.modify_conf,
                             pbar=pbar,
                             name=task_desc,
                             on_failed=True)
            pbar.close()
            # Nornir task 任务执行失败的主机
            failed_hosts = list(results.failed_hosts.keys())
            hosts_list, failed_hosts_list = comm.create_count_list(
                nr, failed_hosts)
            print_result(results)
            return hosts_list, failed_hosts_list, task_desc

        elif choice == '3':
            # 3、ssh测试
            nr = filter_nr.run_filter()
            pbar = tqdm(total=len(nr.inventory.hosts),
                        desc="Running tasks on devices",
                        unit="device(s)",
                        colour='green')

            import ssh_reliable

            task_desc = 'TASK: SSH Reachability Detection'
            results = nr.run(task=ssh_reliable.ssh_test,
                             pbar=pbar,
                             name=task_desc,
                             on_failed=True)
            pbar.close()

            # Nornir task 任务执行失败的主机
            failed_hosts = list(results.failed_hosts.keys())
            hosts_list, failed_hosts_list = comm.create_count_list(
                nr, failed_hosts)
            print_result(results)
            return hosts_list, failed_hosts_list, task_desc

        elif choice == '4':
            # 4、ping测试
            nr = filter_nr.run_filter()
            pbar = tqdm(total=len(nr.inventory.hosts),
                        desc="Running tasks on devices",
                        unit="device(s)",
                        colour='green')

            import icmp_reliable

            task_desc = 'TASK: Ping Reachability Detection'
            results = nr.run(task=icmp_reliable.ping_test,
                             pbar=pbar,
                             name=task_desc)
            pbar.close()
            # Nornir task 任务执行失败的主机
            failed_hosts = list(results.failed_hosts.keys())
            hosts_list, failed_hosts_list = comm.create_count_list(
                nr, failed_hosts)
            print_result(results)
            return hosts_list, failed_hosts_list, task_desc

        elif choice == '5':
            # 5、保存配置
            nr = filter_nr.run_filter()
            pbar = tqdm(total=len(nr.inventory.hosts),
                        desc="Running tasks on devices",
                        unit="device(s)",
                        colour='green')

            import save_conf

            task_desc = 'TASK:  Save Configuration'
            results = nr.run(task=save_conf.save_conf,
                             pbar=pbar,
                             name=task_desc)
            pbar.close()
            # Nornir task 任务执行失败的主机
            failed_hosts = list(results.failed_hosts.keys())
            hosts_list, failed_hosts_list = comm.create_count_list(
                nr, failed_hosts)
            print_result(results)
            return hosts_list, failed_hosts_list, task_desc

        else:
            print(f'输入的[{choice}]没有对应功能！')
            continue


# 4、获取交换机 端口-MAC地址 对应表
@comm.timer
@comm.result_count
@comm.result_write
def get_port_mac():

    # 此处过滤出执行的设备，如筛选出接入交换机
    # nr = nr.filter(F(hostname='172.31.100.24') | F(hostname='172.31.100.26'))
    pbar = tqdm(total=len(nr.inventory.hosts),
                desc="Running tasks on devices",
                unit="device(s)",
                colour='green')

    import get_port_mac

    task_desc = 'TASK: Get Port-MAC Table'
    results = nr.run(task=get_port_mac.get_port_mac,
                     pbar=pbar,
                     name=task_desc,
                     on_failed=True)
    pbar.close()

    # 处理表格数据
    bar = Bar('End of summer:', width=67, max=1, suffix='%(index)d/%(max)d')
    time_str = datetime.now().strftime('%Y%m%d_%H%M%S')

    # 声明全局变量mac_file_path，用于 5、根据输入的MAC地址查询对应设备 中载入文件路径

    global mac_file_path

    mac_file_path = comm.generate_table + '\\' + time_str + '_MAC地址表' + '.xlsx'
    comm.concat_dataframe(results, mac_file_path)
    bar.next()
    bar.finish()
    print(f'File saved: {mac_file_path}')

    # Nornir task 任务执行失败的主机
    failed_hosts = list(results.failed_hosts.keys())
    hosts_list, failed_hosts_list = comm.create_count_list(nr, failed_hosts)
    # print_result 无法对返回的DataFrame进行处理，使用print_result会提示错误：ValueError: The truth value of a DataFrame is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
    # print_result(results)
    return hosts_list, failed_hosts_list, task_desc


# 5、根据输入的MAC地址查询对应设备
@comm.timer
# @comm.result_count
# @comm.result_write
def search_mac():
    """
    判断全局变量 mac_file_path 是否存在，如存在则读取Excel文件，输入关键字搜索并打印结果，若不存在则返回文字提示
    """

    # 判断全局变量 mac_file_path 是否存在
    if 'mac_file_path' in globals():
        # 读取Excel文件
        data = comm.split_cells(mac_file_path)
        # 输入关键字
        keyword = input(
            'Please enter the mac-address you want to search: ').strip()
        # 根据关键字筛选行
        result = data[data['MACADDRESS'].str.contains(keyword, na=False)]
        # 输出结果
        print(result)

    else:
        print(colored('\n>>>先执行 功能4 [获取交换机 端口-MAC地址 对应表]<<<', 'red'))


# 6、根据代码内置OID对设备进行snmp轮询
@comm.timer
@comm.result_count
@comm.result_write
def snmp_polling():

    pbar = tqdm(total=len(nr.inventory.hosts),
                desc="Running tasks on devices",
                unit="device(s)",
                colour='green')

    import snmp_polling

    task_desc = 'TASK: Do SNMP Polling'
    results = nr.run(task=snmp_polling.task_polling,
                     pbar=pbar,
                     name=task_desc,
                     on_failed=True)
    pbar.close()

    # 处理表格数据
    bar = Bar('End of summer:', width=67, max=1, suffix='%(index)d/%(max)d')
    time_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_path = comm.generate_table + '\\' + time_str + '_SNMP轮询结果表' + '.xlsx'
    comm.concat_dataframe(results, file_path)
    bar.next()
    bar.finish()
    print(f'File saved: {file_path}')

    # Nornir task 任务执行失败的主机
    failed_hosts = list(results.failed_hosts.keys())
    hosts_list, failed_hosts_list = comm.create_count_list(nr, failed_hosts)
    # print_result 无法对返回的DataFrame进行处理，使用print_result会提示错误：ValueError: The truth value of a DataFrame is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
    # print_result(results)
    return hosts_list, failed_hosts_list, task_desc


# 7、批量ssh可达性测试
@comm.timer
@comm.result_count
@comm.result_write
def ssh_reliable():

    pbar = tqdm(total=len(nr.inventory.hosts),
                desc="Running tasks on devices",
                unit="device(s)",
                colour='green')

    import ssh_reliable

    task_desc = 'TASK: SSH Reachability Detection'
    results = nr.run(task=ssh_reliable.ssh_test,
                     pbar=pbar,
                     name=task_desc,
                     on_failed=True)
    pbar.close()

    # Nornir task 任务执行失败的主机
    failed_hosts = list(results.failed_hosts.keys())
    hosts_list, failed_hosts_list = comm.create_count_list(nr, failed_hosts)
    print_result(results)
    return hosts_list, failed_hosts_list, task_desc


# 8、批量ping可达性测试
@comm.timer
@comm.result_count
@comm.result_write
def icmp_reliable():

    pbar = tqdm(total=len(nr.inventory.hosts),
                desc="Running tasks on devices",
                unit="device(s)",
                colour='green')

    import icmp_reliable

    task_desc = 'TASK: Ping Reachability Detection'
    results = nr.run(task=icmp_reliable.ping_test,
                     pbar=pbar,
                     name=task_desc,
                     on_failed=True)
    pbar.close()

    # Nornir task 任务执行失败的主机
    failed_hosts = list(results.failed_hosts.keys())
    hosts_list, failed_hosts_list = comm.create_count_list(nr, failed_hosts)
    print_result(results)
    return hosts_list, failed_hosts_list, task_desc


# 9、保存配置
@comm.timer
@comm.result_count
@comm.result_write
def save_conf():

    pbar = tqdm(total=len(nr.inventory.hosts),
                desc="Running tasks on devices",
                unit="device(s)",
                colour='green')

    import save_conf

    task_desc = 'TASK: Save Configuration'
    results = nr.run(task=save_conf.save_conf,
                     pbar=pbar,
                     name=task_desc,
                     on_failed=True)
    pbar.close()

    # Nornir task 任务执行失败的主机
    failed_hosts = list(results.failed_hosts.keys())
    hosts_list, failed_hosts_list = comm.create_count_list(nr, failed_hosts)
    print_result(results)
    return hosts_list, failed_hosts_list, task_desc


# 10、显示设备清单
def itemized_list():

    tb = PrettyTable([
        'name', 'ip', 'platform', 'model', 'device_type', 'area', 'location',
        'version', 'sn'
    ])
    for n, h in nr.inventory.hosts.items():
        tb.add_row([
            n, h.hostname, h.platform, h.data['model'], h.data['device_type'],
            h.data['area'], h.data['location'], h.data['version'], h.data['sn']
        ])
    print(tb)


# 11、导出诊断信息和日志
@comm.timer
@comm.result_count
@comm.result_write
def export_diagnostic_logfile():

    # 输入TFTP服务端地址
    # server_ip = input('输入TFTP服务端地址：').strip()
    # 校验输入的IP地址格式
    retry_times = 0
    while retry_times < 3:
        server_ip = input('输入TFTP服务端地址：').strip()
        if comm.is_valid_ipv4_input(server_ip):
            break
        retry_times += 1
        if retry_times == 3:
            print(colored('-' * 42 + '\n>>>输错三次，重新再来<<<', 'red'))
            run()

    # 输入设备IP地址
    # comtent = input('输入设备IP地址：').strip()
    # 校验输入的IP地址格式
    retry_times = 0
    while retry_times < 3:
        device_ip = input('输入设备IP地址：').strip()
        if comm.is_valid_ipv4_input(device_ip):
            break
        retry_times += 1
        if retry_times == 3:
            print(colored('-' * 42 + '\n>>>输错三次，重新再来<<<', 'red'))
            run()

    nr_new = nr.filter(hostname=device_ip)

    pbar = tqdm(total=len(nr_new.inventory.hosts),
                desc="Running tasks on devices",
                unit="device(s)",
                colour='green')

    import export_diagnostic

    task_desc = 'TASK: Export Diagnostic And Logfile'
    results = nr_new.run(task=export_diagnostic.export_info,
                         server_ip=server_ip,
                         pbar=pbar,
                         name=task_desc,
                         on_failed=True)
    pbar.close()

    # Nornir task 任务执行失败的主机
    failed_hosts = list(results.failed_hosts.keys())
    hosts_list, failed_hosts_list = comm.create_count_list(
        nr_new, failed_hosts)
    print_result(results)
    return hosts_list, failed_hosts_list, task_desc


# 0、退出
def goodbye():
    exit()


# 程序退出时自动清除inventory_unprotected.xlsx文件
@atexit.register
def del_unprotected_xlsx():
    target_file_path = comm.BASE_PATH + "\\inventory\\inventory_unprotected.xlsx"
    # 以下操作是直接删除，不是移动到回收站
    os.remove(target_file_path)


# 创建函数功能字典
func_dic = {
    '1': export_conf,
    '2': modify_conf,
    '3': filter_run,
    '4': get_port_mac,
    '5': search_mac,
    '6': snmp_polling,
    '7': ssh_reliable,
    '8': icmp_reliable,
    '9': save_conf,
    '10': itemized_list,
    '11': export_diagnostic_logfile,
    '0': goodbye,
}


# 打印功能列表
def run():
    while True:
        print('-' * 42)
        print('''
    {}\n
        1、批量备份配置
        2、批量修改配置
        3、筛选-->执行
        4、获取交换机 端口-MAC地址
        5、搜索MAC地址对应设备
        6、批量snmp轮询
        7、批量ssh可达性测试
        8、批量ping可达性测试
        9、批量保存配置
        10、查看设备清单
        11、导出诊断信息和日志（TFTP）
        0、退出
            '''.format(welcome_str))
        print('-' * 42)
        choice = input('输入功能编号：').strip()
        if choice not in func_dic:
            print('请输入正确的功能编号！')
            continue
        func_dic.get(choice)()


system("title Python-NetOps_2.0_beta")

# 开始执行
if __name__ == "__main__":

    # 执行功能列表函数
    run()
