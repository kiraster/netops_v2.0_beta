from datetime import datetime
import sys
import logging

from nornir.core.task import Result
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.tasks.files import write_file

sys.path.append("..")
from func_list import backup_path



def export_conf(task, pbar):
    try:
        # 获取资产中定义的信息，传参跑task
        name = task.host.name
        ip = task.host.hostname
        # 控制台提示信息
        # sys.stdout.write(f'正在备份，设备：{ip}   ' + '\r')
        # sys.stdout.flush()
        cmds = task.host.get('display').split(',')
        time_str = datetime.now().strftime("%H%M")
        output = ''
        for cmd in cmds:
            output += '=' * 100 + '\n' + cmd.center(100, '=') + '\n'
            display_res = task.run(task=netmiko_send_command,
                                   command_string=cmd,
                                   severity_level=logging.DEBUG)
            output += display_res[0].result
            filepath = backup_path + '\\' + '{}_{}_{}.txt'.format(
                name, ip, time_str)

        display_res_write = task.run(task=write_file,
                                     filename=filepath,
                                     content=output,
                                     severity_level=logging.DEBUG)

        pbar.update()
        return Result(host=task.host, result='File saved: {}'.format(filepath))

    except Exception as e:
        # print(e)
        pbar.update()
        return Result(host=task.host, result='备份失败：设备：{}，IP：{}'.format(name, ip), failed=True)
