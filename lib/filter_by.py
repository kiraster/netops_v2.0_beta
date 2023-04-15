'''
IP地址-筛选（格式：192.168.1.1、192.168.1.0/24、192.168.1.1-192.168.1.254）
'''

import ipaddress

from termcolor import colored


# IP地址-筛选
def filter_by_ip(comtent):
    while True:

        ip_list = []

        try:
            # 尝试将输入解析为 IPv4Address ,单IP地址处理
            ip = str(ipaddress.IPv4Address(comtent))
            return ip

        except ValueError:
            try:
                # 将输入拆分为两个 IP 地址
                start, end = comtent.split('-')
                # 尝试将输入解析为 IPv4Address
                ipaddress.IPv4Address(start.strip())
                ipaddress.IPv4Address(end.strip())
                start_ip = int(ipaddress.IPv4Address(start.strip()))
                end_ip = int(ipaddress.IPv4Address(end.strip()))
                for ip in range(start_ip, end_ip+1):
                    ip = ipaddress.IPv4Address(ip)
                    ip_list.append(str(ip))

                return ip_list

            except ValueError as e:
                # 尝试将输入解析为 IPv4Network
                try:
                    net = ipaddress.IPv4Network(comtent)
                    # IP网段处理
                    # nr_fitlter = 'IPv4Network'
                    if net.hostmask != '0.0.0.0':
                        nr_list = []
                        for ip in net.hosts():
                            ip_list.append(str(ip))

                    return ip_list

                except ValueError:
                    print(colored('不是 IPv4 地址、IPv4 网络或 IPv4 地址范围格式', 'red'))
                    break