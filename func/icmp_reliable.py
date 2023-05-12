import sys

from nornir.core.task import Result
import ping3


# 批量ping测试
def ping_test(task, pbar):

    # 获取资产中定义的信息
    name = task.host.name
    ip = task.host.hostname

    ping3.EXCEPTIONS = True

    try:
        ping3.ping(ip)
        output = '{:<18}ping测试成功, {}'.format(ip, name)
        pbar.update()
        return Result(host=task.host, result=output)

    except Exception as e:
        # raise Exception(e)
        pbar.update()
        return Result(host=task.host,
                      result='{:<18}ping测试失败, {}'.format(ip, name),
                      failed=True)
