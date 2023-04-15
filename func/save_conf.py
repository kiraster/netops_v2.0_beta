from datetime import datetime
import sys
import logging

from nornir.core.task import Result
from nornir_netmiko import netmiko_save_config
from nornir_utils.plugins.tasks.files import write_file

from func_list import config_path

def save_res_write(task, name, ip, time_str, save_res):

    output = save_res[0].result
    filepath = config_path + '\\' + '{}_{}_{}.txt'.format(name, ip, time_str)
    task.run(task=write_file, filename=filepath, content=output, severity_level=logging.DEBUG)
    return output


def save_conf(task, pbar):
 
    try:
        # 获取资产中定义的信息，传参跑task
        name = task.host.name
        ip = task.host.hostname
        platform = task.host.platform
        # 控制台提示信息
        # sys.stdout.write(f'正在保存配置，设备：{ip}   ' + '\r')
        # sys.stdout.flush()
        time_str = datetime.now().strftime("%H%M")
        # netmiko_save_config

        if platform == 'hp_comware':
            save_res = task.run(task=netmiko_save_config, cmd='save force', severity_level=logging.DEBUG)
        elif platform == 'huawei':
            save_res = task.run(task=netmiko_save_config, cmd='save', confirm=True, confirm_response='y', severity_level=logging.DEBUG)
        elif platform == 'cisco':
            pass
        else:
            raise Exception('暂不支持的platform平台')
            return Result(host=task.host, result='保存配置失败：设备：{}，IP：{}'.format(name, ip), failed=True)

        output = save_res_write(task, name, ip, time_str, save_res)
        pbar.update()
        return Result(host=task.host, result=output)

    except Exception:
        pbar.update()
        return Result(host=task.host, result='保存配置失败：设备：{}，IP：{}'.format(name, ip), failed=True)
