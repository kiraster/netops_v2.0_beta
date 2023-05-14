from datetime import datetime
import os
import sys
import logging
import difflib

from nornir.core.task import Result
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.tasks.files import write_file

from lib import comm


def check_diff(task, pbar):
    """
    ssh登陆设备，对比检查当前运行配置与已保存配置是否一致
    对设备当前运行配置与已保存配置不一致的，记录变化
    导出路径：\EXPORT\当天日期\diff_conf
    文件格式：name_ip_当前时间.txt
    """

    try:
        # 获取inventory中定义的信息
        name = task.host.name
        ip = task.host.hostname
        platform = task.host.platform

        time_str = datetime.now().strftime("%H%M%S")

        # 根据platform进行处理，若由于版本或型号导致的命令差异，可再加if判断
        if platform == 'hp_comware':
            # 已保存配置
            saved_conf = task.run(task=netmiko_send_command,
                                  command_string='display saved-configuration',
                                  severity_level=logging.DEBUG)

            # 当前运行配置
            curr_conf = task.run(
                task=netmiko_send_command,
                command_string='display current-configuration',
                severity_level=logging.DEBUG)

        elif platform == 'huawei':
            pass
        elif platform == 'cisco':
            pass
        else:
            # raise Exception('暂不支持的platform平台')
            return Result(host=task.host,
                          result='检查出现异常：设备：{}，IP：{}'.format(name, ip),
                          failed=True)

        # 以行为单位分隔形成列表
        saved_list = saved_conf[0].result.splitlines(True)
        curr_list = curr_conf[0].result.splitlines(True)

        # 使用Differ类计算差异
        differ = difflib.Differ()
        diff = list(differ.compare(saved_list, curr_list))

        # 判断saved_list与curr_list是否相同，即 diff 中所有元素的第一个字符是否都为 ' '
        if all(line.startswith(' ') for line in diff):
            pbar.update()
            return Result(
                host=task.host,
                result='检查完成，设备当前运行配置与已保存配置一致：设备：{}，IP：{}'.format(name, ip),
            )
        else:
            output = ''
            for line in diff:
                if line.startswith('-'):
                    # print(line.replace('- ', '- old: ', 1).rstrip())
                    new_line = line.replace('- ', '- old: ', 1).rstrip()
                    output += new_line + '\n'
                elif line.startswith('+'):
                    # print(line.replace('+ ', '+ new: ', 1).rstrip())
                    new_line = line.replace('+ ', '+ new: ', 1).rstrip()
                    output += new_line + '\n'
                else:
                    # print('  ' + line.rstrip())
                    new_line = line.rstrip()
                    output += new_line + '\n'

            # file_path = comm.diff_config_path + '\\' + '{}_{}_{}.txt'.format(
            #     name, ip, time_str)

            file_path = os.path.normpath(
                os.path.join(comm.diff_config_path,
                             '{}_{}_{}.txt'.format(name, ip, time_str)))

            display_res_write = task.run(task=write_file,
                                         filename=file_path,
                                         content=output,
                                         severity_level=logging.DEBUG)

            pbar.update()

            # 定义一个report文件路径，记录当前运行配置与已保存配置不一致的设备列表
            # report_path = comm.diff_config_path + '\\' + 'report_conf_diff.log'
            report_path = os.path.normpath(
                os.path.join(comm.diff_config_path, 'report_conf_diff.log'))
            task.run(task=write_file,
                     filename=report_path,
                     content='Device: {}   IP: {}\n'.format(name, ip),
                     append=True,
                     severity_level=logging.DEBUG)

            return Result(host=task.host,
                          result='检查完成，设备当前运行配置与已保存配置不一致：{}，IP：{}'.format(
                              name, ip),
                          changed=True)

    except Exception as e:
        raise Exception(e)
        # print(e)
        pbar.update()
        return Result(host=task.host,
                      result='检查出现异常：设备：{}，IP：{}'.format(name, ip),
                      failed=True)