from datetime import datetime
import sys
import logging

from nornir.core.task import Result
from nornir_netmiko import netmiko_send_config
# from netmiko import ConnectHandler
from nornir_utils.plugins.tasks.files import write_file

from func_list import config_path


def modify_conf(task, pbar):

    try:
        # 获取资产中定义的信息，传参跑task
        name = task.host.name
        ip = task.host.hostname
        # 控制台提示信息
        # sys.stdout.write(f'正在配置，设备：{ip}   ' + '\r')
        # sys.stdout.flush()
        cmds = task.host.get('config').split(',')
        time_str = datetime.now().strftime("%H%M")

        # 方式一，nornir_netmiko
        output = ''
        config_res = task.run(task=netmiko_send_config, config_commands=cmds, severity_level=logging.DEBUG)
        # task.host.connections['netmiko']
        output += config_res[0].result
        # filepath = config_path + '\\' + '{}_{}_{}.txt'.format(name, ip, time_str)
        filepath = config_path + '/{}_{}_{}.txt'.format(name, ip, time_str)
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

        filepath = config_path + '\\' + '{}_{}_{}.txt'.format(name, ip, time_str)
        config_res_write = task.run(task=write_file,
                                    filename=filepath,
                                    content=output,
                                    severity_level=logging.DEBUG)
                                    '''

        pbar.update()
        return Result(host=task.host, result=output, changed=True)

    except Exception:
        pbar.update()
        return Result(host=task.host, result='配置失败：设备：{}，IP：{}'.format(name, ip), failed=True)
