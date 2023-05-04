import sys
import logging

from nornir.core.task import Result
from nornir_netmiko import netmiko_send_command
import pandas as pd

sys.path.append("")
from lib import do_polling


def task_polling(task, pbar):

    try:
        ip = task.host.hostname
        community_data = task.host.data['community_data']
        name = task.host.name
        
        # th_list = ['设备名称', 'IP地址', '网络区域', '设备类型', '设备位置', '运行时间', '软件版本', '序列号', '设备型号', 'CPU利用率', '内存利用率', '温度', '电源状态', '风扇状态', '轮询时间']
        # 此处result预期是字典格式 {'sysname': 'SW1', 'device_uptime': '1:10:36', ……｝
        result = do_polling.do_pysnmp(ip, community_data)
        # print(type(result))
        # print(result)
        
        # 返回的应该是字典，否则返回错误
        if isinstance(result, dict):

            # 添加轮询时间
            from datetime import datetime
            # 获取当前日期和时间并格式化
            time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            df = pd.DataFrame([result])
            # 添加到 DataFrame 的最右侧
            df['poll_starttime'] = time_str

            # print(df)

            pbar.update()
            return Result(host=task.host, result=df)
        else:
            pbar.update()
            return Result(host=task.host,
                          result='snmp轮询任务失败：设备：{}，IP：{}'.format(name, ip),
                          failed=True)

    except Exception as e:
        print(e)
        pbar.update()
        return Result(host=task.host,
                      result='snmp轮询任务失败：设备：{}，IP：{}'.format(name, ip),
                      failed=True)