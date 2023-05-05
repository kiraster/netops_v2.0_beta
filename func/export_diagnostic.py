from datetime import datetime
import re

from nornir.core.task import Result
import netmiko

def export_info(task, server_ip, pbar):

    try:
        # 获取资产中定义的信息
        name = task.host.name
        ip = task.host.hostname
        platform = task.host.platform

        output = ''
        time_str = datetime.now().strftime('%Y%m%d_%H%M%S')

        #  establish a new connection of that type with default parameters and return it
        net_conn = task.host.get_connection('netmiko', task.nornir.config)

        if platform == 'hp_comware':

            # 保存诊断信息到文件
            dis_diag_info = [['display diagnostic-information', ']:'], ['y\n', ']:'], ['\n', '>']]
            output += net_conn.send_multiline(dis_diag_info)
            # 提及保存的诊断信息文件名
            pattern = r'\[([^]]*flash:[^]]*\.gz)]'
            diag_info_path = re.search(pattern, output).group(1)

            
            # 保存诊断日志文件
            output += net_conn.send_command(command_string='diagnostic-logfile save')

            # 保存日志到文件
            output += net_conn.send_command(command_string='logfile save')

            # 上传诊断信息文件
            put_diag_info = f'tftp {server_ip} put {diag_info_path}'
            output += net_conn.send_command(command_string=put_diag_info)

            # 上传诊断日志文件
            put_diag_log = f'tftp {server_ip} put flash:/diagfile/diagfile.log diagfile_{time_str}.log'
            output += net_conn.send_command(command_string=put_diag_log)

            # 上传日志文件
            put_log = f'tftp {server_ip} put flash:/logfile/logfile.log logfile_{time_str}.log'
            output += net_conn.send_command(command_string=put_log)

            pbar.update()  
            return Result(host=task.host, result='导出诊断信息、诊断日志、日志完成：设备：{}，IP：{}'.format(name, ip))

        elif platform == 'huawei':
            pass
        elif platform == 'cisco':
            pass
        else:
            pbar.update()  
            return Result(host=task.host, result='导出诊断信息、诊断日志、日志失败：设备：{}，IP：{}'.format(name, ip), failed=True)



    except Exception as e:
        # raise Exception(e)
        pbar.update()        
        return Result(host=task.host, result='导出诊断信息、诊断日志、日志失败：设备：{}，IP：{}'.format(name, ip), failed=True)