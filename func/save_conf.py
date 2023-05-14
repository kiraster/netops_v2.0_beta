from datetime import datetime
import os
import sys
import logging

from nornir.core.task import Result
from nornir_netmiko import netmiko_save_config
from nornir_utils.plugins.tasks.files import write_file

from lib import comm

# def save_res_write(task, name, ip, time_str, save_res):

#     output = save_res[0].result
#     file_path = comm.config_path + '\\' + '{}_{}_{}.txt'.format(name, ip, time_str)
#     task.run(task=write_file, filename=filepath, content=output, severity_level=logging.DEBUG)
#     return output


def save_conf(task, pbar):
    """
    执行netmiko_save_config操作保存设备配置
    """

    try:
        # 获取inventory中定义的信息
        name = task.host.name
        ip = task.host.hostname
        platform = task.host.platform

        time_str = datetime.now().strftime("%H%M")

        # 根据platform进行保存操作
        if platform == 'hp_comware':
            save_res = task.run(task=netmiko_save_config,
                                cmd='save force',
                                severity_level=logging.DEBUG)
        elif platform == 'huawei':
            save_res = task.run(task=netmiko_save_config,
                                cmd='save',
                                confirm=True,
                                confirm_response='y',
                                severity_level=logging.DEBUG)
        elif platform == 'cisco':
            pass
        else:
            raise Exception('暂不支持的platform平台')
            return Result(host=task.host,
                          result='保存配置失败：设备：{}，IP：{}'.format(name, ip),
                          failed=True)

        # output = save_res_write(task, name, ip, time_str, save_res)
        output = save_res[0].result
        # file_path = comm.config_path + '\\' + '{}_{}_{}.txt'.format(
        #     name, ip, time_str)
        file_path = os.path.normpath(
            os.path.join(comm.config_path,
                         '{}_{}_{}.txt'.format(name, ip, time_str)))
        display_res_write = task.run(task=write_file,
                                     filename=file_path,
                                     content=output,
                                     severity_level=logging.DEBUG)
        pbar.update()
        return Result(host=task.host, result=output)

    except Exception:
        pbar.update()
        return Result(host=task.host,
                      result='保存配置失败：设备：{}，IP：{}'.format(name, ip),
                      failed=True)
