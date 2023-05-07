from datetime import datetime
import sys
import logging

from nornir.core.task import Result
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.tasks.files import write_file

from lib import comm


def modify_conf(task, pbar):
    """
    根据资产清单表格中“config”列的命令，进行设备配置并将回显内容分别记录
    文件名：name_ip_当前时间.txt
    导出位置：\EXPORT\当天日期\modify_conf
    """

    try:
        # 获取inventory中定义的信息
        name = task.host.name
        ip = task.host.hostname

        cmds = task.host.get('config').split(',')
        time_str = datetime.now().strftime("%H%M%S")

        # 方式一，nornir_netmiko
        output = ''
        config_res = task.run(task=netmiko_send_config,
                              config_commands=cmds,
                              severity_level=logging.DEBUG)
        output += config_res[0].result
        filepath = comm.config_path + '\\' + '{}_{}_{}.txt'.format(
            name, ip, time_str)
        config_res_write = task.run(task=write_file,
                                    filename=filepath,
                                    content=output,
                                    severity_level=logging.DEBUG)

        # 方式二，netmiko
        '''
        # 调用get_connection 获取Netmiko连接
        net_conn = task.host.get_connection('netmiko', task.nornir.config)
        # 特权模式的判断
        secret = net_conn.secret

        # 特权模式的判断
        if secret:
            net_conn.enable()

        output = net_conn.send_config_set(cmds)
        # print(output)

        filepath = comm.config_path + '\\' + '{}_{}_{}.txt'.format(name, ip, time_str)
        config_res_write = task.run(task=write_file,
                                    filename=filepath,
                                    content=output,
                                    severity_level=logging.DEBUG)
        '''

        pbar.update()
        return Result(host=task.host, result=output, changed=True)

    except Exception as e:
        # raise Exception(e)
        # print(e)
        pbar.update()
        return Result(host=task.host,
                      result='配置失败：设备：{}，IP：{}'.format(name, ip),
                      failed=True)
