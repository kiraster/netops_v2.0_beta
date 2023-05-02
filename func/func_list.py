'''
程序入口
'''
from os import system
from datetime import datetime
import os
import sys
import logging
import atexit

from nornir import InitNornir
from nornir.core.task import Result
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from tqdm import tqdm
from progress.bar import Bar
from prettytable import PrettyTable

sys.path.append("")
from lib import comm

# 定义一个没什么用的头
welcome_str = '`LIFE IS A FUCKING MOVIE`'

# 创建文件夹
backup_path, config_path, generate_table, BASE_PATH, EXPORT_PATH, dir_name = comm.create_path()

# 初始化创建一个 Nornir 对象
nr = InitNornir(config_file=BASE_PATH + "\\nornir.yaml")


# 1、批量备份配置
# 记录程序执行时间装饰器
@comm.timer
# 记录运行结果的装饰器
@comm.result_count
# 保存运行结果记录的装饰器
@comm.result_write
def export_conf():

    # nr = InitNornir(config_file="nornir.yaml")
    # tqdm 进度条 参数
    pbar = tqdm(total=len(nr.inventory.hosts), desc="Running tasks on devices", unit="device(s)", colour='green')

    import export_conf

    task_desc = 'TASK: Export Configuration Of Device'
    results = nr.run(task=export_conf.export_conf, pbar=pbar, name=task_desc, on_failed=True)
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

    # nr = InitNornir(config_file="nornir.yaml")
    pbar = tqdm(total=len(nr.inventory.hosts), desc="Running tasks on devices", unit="device(s)", colour='green')

    import modify_conf

    task_desc = 'TASK: Modify Configuration Of Device'
    results = nr.run(task=modify_conf.modify_conf, pbar=pbar, name=task_desc, on_failed=True)
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

    # 给出选项，默认回车执行定义好的表格数据，按除0外任一简执行手动输入
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

        if choice not in ['0', '1', '2', '3', '4', '5']:
            print('请输入正确的功能编号！')
            continue

        if choice == '0':
            run()

        if choice == '1':
            # 1、备份配置
            nr = filter_nr.run_filter()
            pbar = tqdm(total=len(nr.inventory.hosts), desc="Running tasks on devices", unit="device(s)", colour='green')

            import export_conf

            task_desc = 'TASK: Export Configuration Of Device'
            results = nr.run(task=export_conf.export_conf, pbar=pbar, name=task_desc, on_failed=True)
            pbar.close()
            # Nornir task 任务执行失败的主机
            failed_hosts = list(results.failed_hosts.keys())
            hosts_list, failed_hosts_list = comm.create_count_list(nr, failed_hosts)
            print_result(results)
            return hosts_list, failed_hosts_list, task_desc

        if choice == '2':
            # 2、修改配置
            nr = filter_nr.run_filter()
            pbar = tqdm(total=len(nr.inventory.hosts), desc="Running tasks on devices", unit="device(s)", colour='green')

            import modify_conf

            task_desc = 'TASK: Modify Configuration Of Device'
            results = nr.run(task=modify_conf.modify_conf, pbar=pbar, name=task_desc, on_failed=True)
            pbar.close()
            # Nornir task 任务执行失败的主机
            failed_hosts = list(results.failed_hosts.keys())
            hosts_list, failed_hosts_list = comm.create_count_list(nr, failed_hosts)
            print_result(results)
            return hosts_list, failed_hosts_list, task_desc

        if choice == '3':
            # 3、ssh测试
            nr = filter_nr.run_filter()
            pbar = tqdm(total=len(nr.inventory.hosts), desc="Running tasks on devices", unit="device(s)", colour='green')
            # pbar = Bar('Processing', width=67, max=len(nr.inventory.hosts), suffix='%(index)d/%(max)d' + '\t' + '%(percent)d%%')

            import ssh_reliable

            task_desc = 'TASK: SSH Reachability Detection'
            results = nr.run(task=ssh_reliable.ssh_test, pbar=pbar, name=task_desc, on_failed=True)
            pbar.close()
            # pbar.finish()
            # Nornir task 任务执行失败的主机
            failed_hosts = list(results.failed_hosts.keys())
            hosts_list, failed_hosts_list = comm.create_count_list(nr, failed_hosts)
            print_result(results)
            return hosts_list, failed_hosts_list, task_desc

        if choice == '4':
            # 4、ping测试
            nr = filter_nr.run_filter()
            pbar = tqdm(total=len(nr.inventory.hosts), desc="Running tasks on devices", unit="device(s)", colour='green')

            import icmp_reliable

            task_desc = 'TASK: Ping Reachability Detection'
            results = nr.run(task=icmp_reliable.ping_test, pbar=pbar, name=task_desc)
            pbar.close()
            # Nornir task 任务执行失败的主机
            failed_hosts = list(results.failed_hosts.keys())
            hosts_list, failed_hosts_list = comm.create_count_list(nr, failed_hosts)
            print_result(results)
            return hosts_list, failed_hosts_list, task_desc

        if choice == '5':
            # 5、保存配置
            nr = filter_nr.run_filter()
            pbar = tqdm(total=len(nr.inventory.hosts), desc="Running tasks on devices", unit="device(s)", colour='green')

            import save_conf

            task_desc = 'TASK:  Save Configuration'
            results = nr.run(task=save_conf.save_conf, pbar=pbar, name=task_desc)
            pbar.close()
            # Nornir task 任务执行失败的主机
            failed_hosts = list(results.failed_hosts.keys())
            hosts_list, failed_hosts_list = comm.create_count_list(nr, failed_hosts)
            print_result(results)
            return hosts_list, failed_hosts_list, task_desc


# 4、获取交换机 端口-MAC地址 对应表
@comm.timer
@comm.result_count
@comm.result_write
def get_port_mac():
    
    # nr = InitNornir(config_file="nornir.yaml")
    # nr = InitNornir(config_file=BASE_PATH + "\\nornir.yaml")
    # 此处过滤要执行的主机，如筛选出接入交换机
    # nr = nr.filter(F(hostname='172.31.100.24') | F(hostname='172.31.100.26'))
    pbar = tqdm(total=len(nr.inventory.hosts), desc="Running tasks on devices", unit="device(s)", colour='green')
    # pbar = Bar('Processing', width=67, max=len(nr.inventory.hosts), suffix='%(index)d/%(max)d' + '\t' + '%(percent)d%%')

    import get_port_mac

    task_desc = 'TASK: Get Port-MAC Table'
    results = nr.run(task=get_port_mac.get_port_mac, pbar=pbar, name=task_desc, on_failed=True)
    pbar.close()
    # pbar.finish()
    # 处理表格数据
    bar = Bar('End of summer:', width=67, max=1, suffix = '%(index)d/%(max)d')
    time_str = datetime.now().strftime("%Y%m%d")
    file_path = generate_table + '\\' +  time_str + '_MAC地址表' + '.xlsx'
    file_path_for_search = generate_table + '\\' +  time_str + '_MAC地址表_SEARCH' + '.xlsx'
    comm.concat_dataframe(results, file_path, file_path_for_search)
    bar.next()
    bar.finish()
    print(f'File saved: {file_path}')

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

    import pandas as pd

    # 需要先获取交换机的mac地址表，当天日期
    time_str = datetime.now().strftime("%Y%m%d")
    # 读取Excel文件
    file_path_for_search = generate_table + '\\' +  time_str + '_MAC地址表_SEARCH' + '.xlsx'
    data = pd.read_excel(file_path_for_search)
    # 输入关键字
    keyword = input('Please enter the mac-address you want to search: ')
    # 根据关键字筛选行
    result = data[data['macaddress'].str.contains(keyword, na=False)]
    # 输出结果
    print(result)


# 7、批量ssh可达性测试
@comm.timer
@comm.result_count
@comm.result_write
def ssh_reliable():

    # nr = InitNornir(config_file="nornir.yaml")
    pbar = tqdm(total=len(nr.inventory.hosts), desc="Running tasks on devices", unit="device(s)", colour='green')
    # pbar = Bar('Processing', width=67, max=len(nr.inventory.hosts), suffix='%(index)d/%(max)d' + '\t' + '%(percent)d%%')

    import ssh_reliable

    task_desc = 'TASK: SSH Reachability Detection'
    results = nr.run(task=ssh_reliable.ssh_test, pbar=pbar, name=task_desc, on_failed=True)
    pbar.close()
    # pbar.finish()
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

    # nr = InitNornir(config_file="nornir.yaml")
    pbar = tqdm(total=len(nr.inventory.hosts), desc="Running tasks on devices", unit="device(s)", colour='green')

    import icmp_reliable

    task_desc = 'TASK: Ping Reachability Detection'
    results = nr.run(task=icmp_reliable.ping_test, pbar=pbar, name=task_desc, on_failed=True)
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

    # nr = InitNornir(config_file="nornir.yaml")
    pbar = tqdm(total=len(nr.inventory.hosts), desc="Running tasks on devices", unit="device(s)", colour='green')

    import save_conf

    task_desc = 'TASK: Save Configuration'
    results = nr.run(task=save_conf.save_conf, pbar=pbar, name=task_desc, on_failed=True)
    pbar.close()
    # Nornir task 任务执行失败的主机
    failed_hosts = list(results.failed_hosts.keys())
    hosts_list, failed_hosts_list = comm.create_count_list(nr, failed_hosts)
    print_result(results)
    return hosts_list, failed_hosts_list, task_desc


# 10、显示设备清单
def itemized_list():

    tb = PrettyTable(['name', 'ip', 'platform', 'model', 'device_type', 'area', 'location', 'version', 'sn'])
    for n, h in nr.inventory.hosts.items():
        tb.add_row([n, h.hostname, h.platform, h.data['model'], h.data['device_type'], h.data['area'], h.data['location'], h.data['version'], h.data['sn']])
    print(tb)


# 0、退出
def goodbye():
    exit()

# 程序退出时自动清除inventory_unprotected.xlsx文件
@atexit.register
def del_unprotected_xlsx():
    target_file_path = BASE_PATH + "\\inventory\\inventory_unprotected.xlsx"
    # 以下操作是直接删除，不是移动到回收站
    os.remove(target_file_path)
    

# 创建函数功能字典
func_dic = {
    '1': export_conf,
    '2': modify_conf,
    '3': filter_run,
    '4': get_port_mac,
    '5': search_mac,
    '7': ssh_reliable,
    '8': icmp_reliable,
    '9': save_conf,
    '10': itemized_list,
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
        7、批量ssh可达性测试
        8、批量ping可达性测试
        9、批量保存配置
        10、查看设备清单
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
