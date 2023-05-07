'''
IP地址-筛选（格式：192.168.1.1，192.168.1.0/24，192.168.1.1-192.168.1.254）
'''

import ipaddress

from termcolor import colored


# IP地址-筛选
def filter_by_ip(comtent):
    
    ip_list = []

    # 对输入的内容以逗号分割进行for循环
    # 即使输入单个的IP地址或网络或范围，最后也会返回一个单个元素列表
    for i in comtent.split(','):
        i = i.strip()
        # print(i)
        try:
            # 尝试将输入解析为 IPv4Address ,单IP地址处理
            ip = str(ipaddress.IPv4Address(i))
            ip_list.append(ip)
        except ValueError:
            try:
                # 将输入拆分为两个 IP 地址
                start, end = i.split('-')
                # 尝试将输入解析为 IPv4Address
                ipaddress.IPv4Address(start.strip())
                ipaddress.IPv4Address(end.strip())
                start_ip = int(ipaddress.IPv4Address(start.strip()))
                end_ip = int(ipaddress.IPv4Address(end.strip()))
                for ip in range(start_ip, end_ip+1):
                    ip = ipaddress.IPv4Address(ip)
                    ip_list.append(str(ip))
            except ValueError as e:
                # 尝试将输入解析为 IPv4Network
                try:
                    net = ipaddress.IPv4Network(i)
                    # IP网段处理
                    if net.hostmask != '0.0.0.0':
                        for ip in net.hosts():
                            ip_list.append(str(ip))
                except ValueError:
                    print(colored(f'无法解析IP地址或IP地址范围或IP网络：{i}', 'red'))

    return ip_list