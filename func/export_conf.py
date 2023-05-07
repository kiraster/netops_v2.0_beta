from datetime import datetime
import sys
import logging

from nornir.core.task import Result
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.tasks.files import write_file

from lib import comm


def export_conf(task, pbar):
    """
    根据资产清单表格中“display”列的命令，导出设备配置
    文件名：name_ip_当前时间.txt
    导出路径：\EXPORT\当天日期\export_conf
    """

    try:
        # 获取inventory中定义的信息
        name = task.host.name
        ip = task.host.hostname

        cmds = task.host.get('display').split(',')
        time_str = datetime.now().strftime("%H%M%S")

        output = ''

        for cmd in cmds:
            output += '=' * 100 + '\n' + cmd.center(100, '=') + '\n'
            display_res = task.run(task=netmiko_send_command,
                                   command_string=cmd,
                                   severity_level=logging.DEBUG)
            output += display_res[0].result

        file_path = comm.backup_path + '\\' + '{}_{}_{}.txt'.format(
            name, ip, time_str)

        display_res_write = task.run(task=write_file,
                                     filename=file_path,
                                     content=output,
                                     severity_level=logging.DEBUG)

        pbar.update()
        return Result(host=task.host,
                      result='File saved: {}'.format(file_path))

    except Exception as e:
        # raise Exception(e)
        # print(e)
        pbar.update()
        return Result(host=task.host,
                      result='备份失败：设备：{}，IP：{}'.format(name, ip),
                      failed=True)
