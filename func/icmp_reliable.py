import sys
# import logging

from nornir.core.task import Result
import ping3

# 批量ping测试
def ping_test(task, pbar):

    # 获取资产中定义的信息，传参跑task
    name = task.host.name
    ip = task.host.hostname

    ping3.EXCEPTIONS = True 
    # 控制台提示信息
    # sys.stdout.write(f'正在ping测试，设置：{ip}   ' + '\r')
    # sys.stdout.flush()
    try:
        ping3.ping(ip)
        output = '{:<18}ping测试成功, {}'.format(ip, name)
        pbar.update()
        return Result(host=task.host, result=output)

    except Exception as e:
        # raise Exception(e)
        pbar.update()
        return Result(host=task.host, result='{:<18}ping测试失败, {}'.format(ip, name), failed=True)

