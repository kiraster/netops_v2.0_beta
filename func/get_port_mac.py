import logging

from nornir.core.task import Result
from nornir_netmiko import netmiko_send_command
import pandas as pd


def get_port_mac(task, pbar):
    """
    获取交换机MAC地址表和trunk接口信息，求差集获取到非trunk接口的MAC地址表
    不同厂商的名称和命令可能不一致，按需修改
    """

    try:
        # 获取inventory中定义的信息
        name = task.host.name
        ip = task.host.hostname

        platform = task.host.platform

        # 编写基于platform执行对应命令获取回显内容的判断来获取MAC地址表，
        # 如果由于同平台不同产品或不同版本之间的命令差异或回显差异，可以在if语句下添加比如型号判断或版本判断或手动调整task.run执行返回的结果进行同一格式
        # 这些判断的元素【型号或版本】需要提前在inventory文件里定义
        if platform == 'hp_comware':
            output_mac_table = task.run(task=netmiko_send_command,
                                        command_string='display mac-address',
                                        use_textfsm=True,
                                        severity_level=logging.DEBUG)
            # display port trunk的textfsm模板为手动添加，文件在：venv\Lib\site-packages\ntc_templates\templates\hp_comware_display_port_trunk_local.textfsm
            # 如需添加其他platform的模板，按规律添加，注意修改venv\Lib\site-packages\ntc_templates\templates\index 文件
            output_port_trunk = task.run(task=netmiko_send_command,
                                         command_string='display port trunk',
                                         use_textfsm=True,
                                         severity_level=logging.DEBUG)
        elif platform == 'huawei':
            pass
        elif platform == 'cisco':
            pass
        else:
            # platform not in ['hp_comware', 'huawei', 'cisco',……]:
            raise Exception('暂不支持的platform平台')
            return Result(host=task.host,
                          result='获取MAC地址表信息失败：设备：{}，IP：{}'.format(name, ip),
                          failed=True)

        # 构建表格列数据
        mac_table_df1 = pd.DataFrame(columns=['device'],
                                     data=[[name + '_' + ip]] *
                                     len(output_mac_table[0].result))

        mac_table_df2 = pd.DataFrame(output_mac_table[0].result)

        port_trunk_df = pd.DataFrame(output_port_trunk[0].result)

        # DataFrame横向拼接
        mac_table_df = pd.concat([mac_table_df1, mac_table_df2], axis=1)

        # isin取反，保留非trunk port
        df = mac_table_df[~mac_table_df['interface'].
                          isin(port_trunk_df['port_trunk'])]

        # print(df)
        pbar.update()
        return Result(host=task.host, result=df)

    except Exception:
        pbar.update()
        return Result(host=task.host,
                      result='获取MAC地址表信息失败：设备：{}，IP：{}'.format(name, ip),
                      failed=True)
