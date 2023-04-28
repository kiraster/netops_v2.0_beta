import sys

from nornir.core.task import Result
# from netmiko import ConnectHandler

import logging


def ssh_test(task, pbar):

    # 获取资产中定义的信息，传参跑task
    name = task.host.name
    ip = task.host.hostname
    # 控制台提示信息
    # sys.stdout.write(f'\n正在ssh测试，设备：{ip}   ' + '\r')
    # sys.stdout.flush()
    cmds = task.host.get('config').split(',')

    try:

        # 调用get_connection 获取Netmiko连接
        net_conn = task.host.get_connection('netmiko', task.nornir.config)
        # SSH连接测试成功
        hostname = net_conn.find_prompt()
        output = '{:<18}SSH测试连接成功,获取到设备提示符： {}'.format(ip, hostname)

        pbar.update()
        # pbar.next()
        return Result(host=task.host, result=output)

    except Exception as e:
        # SSH连接测试失败
        # raise Exception(e)
        pbar.update()        
        # pbar.next()
        return Result(host=task.host, result='{:<18}SSH测试连接失败,未获取到设备提示符'.format(ip), failed=True)
