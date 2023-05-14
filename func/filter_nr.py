'''
筛选返回给上一层一个nr对象
'''
import sys
import os

from nornir import InitNornir
from nornir.core.filter import F

from lib import comm
from lib import filter_by


# 1、IP地址-筛选
def filter_by_ip(nr):

    comtent = input(
        '输入格式：[192.168.1.1,192.168.1.0/24,192.168.1.1-192.168.1.254]：').strip(
        )
    res = filter_by.filter_by_ip(comtent)
    if isinstance(res, list):

        def ip_filter(host):
            for ip in res:
                if ip == host.hostname:
                    return True

        nr = nr.filter(filter_func=ip_filter)
        return nr

    else:
        print('It is impossible')
        nr = nr.filter(hostname=comtent)
        return nr


# 2、平台-筛选
def filter_by_platform(nr):

    comtent = input('输入平台：').strip()
    nr = nr.filter(platform=comtent)
    return nr


# 3、设备型号-筛选
def filter_by_model(nr):

    comtent = input('输入设备型号：').strip()
    nr = nr.filter(model=comtent)
    return nr


# 4、区域-筛选
def filter_by_area(nr):

    comtent = input('输入区域：').strip()
    nr = nr.filter(area=comtent)
    return nr


# 5、组合筛选（高级）
def filter_by_adv(nr):

    comtent = input('F对象（~取反 ），& 和 | 执行 AND 和 OR 运算组合筛选：').strip()
    # F(hostname='172.31.100.20') | F(area='JCW')
    nr = eval(f'nr.filter({comtent})')
    # print(nr.inventory.hosts.keys())
    return nr


# 0、返回上一级
def goodbye():

    from func import func_list
    func_list.filter_run()


func_dic = {
    '1': filter_by_ip,
    '2': filter_by_platform,
    '3': filter_by_model,
    '4': filter_by_area,
    '5': filter_by_adv,
    '0': goodbye
}


def run_filter():
    while True:
        print('-' * 42)
        print('''
        1、IP地址-筛选（格式：192.168.1.1,192.168.1.0/24,192.168.1.1-192.168.1.254）
        2、平台-筛选（huawie、hp_comvare、...)
        3、设备型号-筛选(H3C S6850、...)
        4、区域-筛选（JCW、AFW、...)
        5、组合筛选（高级）
        0、返回上一级
        ''')
        print('-' * 42)
        choice = input('输入编号：').strip()
        if choice not in func_dic:
            print('没有该编号对应的功能！')
            continue
        if choice == '0':
            goodbye()

        nr_yaml_path = os.path.normpath(os.path.join(comm.BASE_PATH, 'nornir.yaml'))
        nr = InitNornir(config_file=nr_yaml_path)
        res = func_dic.get(choice)(nr)
        return res
