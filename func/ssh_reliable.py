from nornir.core.task import Result


def ssh_test(task, pbar):
    """
    ssh登陆登陆设备，获取到设备的prompt作为依据判断ssh可达
    """

    # 获取inventory中定义的信息
    name = task.host.name
    ip = task.host.hostname

    try:

        # 调用get_connection 获取Netmiko连接
        net_conn = task.host.get_connection('netmiko', task.nornir.config)
        # SSH连接测试成功
        hostname = net_conn.find_prompt()
        output = '{:<18}SSH测试连接成功,获取到设备提示符： {}'.format(ip, hostname)

        pbar.update()
        return Result(host=task.host, result=output)

    except Exception as e:
        # SSH连接测试失败
        # raise Exception(e)
        pbar.update()
        return Result(host=task.host,
                      result='{:<18}SSH测试连接失败,未获取到设备提示符'.format(ip),
                      failed=True)
