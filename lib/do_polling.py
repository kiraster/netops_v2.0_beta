import datetime
from pysnmp.entity.rfc3413.oneliner import cmdgen


# snmp轮询
def do_pysnmp(ip, community_data):

    # pysnmp 结果存储字典
    pysnmp_dict = {}

    # 定义OID列表和私有OID列表
    # 公共OID
    public_oid = ['1.3.6.1.2.1.1.5.0', '1.3.6.1.2.1.1.3.0']

    # 私有OID
    oid_version = [
        '1.3.6.1.2.1.47.1.1.1.1.10.1',  # S5820V2-54QS-GE，MSR36-20，S6850
        '1.3.6.1.2.1.47.1.1.1.1.10.2',  # S5130S-20P-EI
        '1.3.6.1.2.1.47.1.1.1.1.10.4'
    ]

    oid_sn = ['1.3.6.1.2.1.47.1.1.1.1.11.1', '1.3.6.1.2.1.47.1.1.1.1.11.2']
    oid_model = ['1.3.6.1.2.1.47.1.1.1.1.13.1', '1.3.6.1.2.1.47.1.1.1.1.13.2']
    oid_cpu = [
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.18',
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.4',
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.66',
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.212',  # S5130S-20P-EI
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.97',
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.25',  # S5820V2-54QS-GE 
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.14',
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.175'
    ]
    oid_mem = [
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.18',
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.4',
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.66',
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.212',  # S5130S-20P-EI
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.97',
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.25',  # S5820V2-54QS-GE 
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.14',
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.175'
    ]
    oid_temperature = [
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.468',
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.158',
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.66',
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.212',  # S5130S-20P-EI
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.97',
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.314',  # S5820V2-54QS-GE 
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.18',
        '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.338'
    ]
    oid_power_state = [
        '1.3.6.1.4.1.25506.8.35.9.1.2.1.2.1',  # S5820V2-54QS-GE 
        '1.3.6.1.4.1.25506.8.35.9.1.2.1.2.2'  # S5130S-20P-EI
    ]
    oid_fan_state = ['1.3.6.1.4.1.25506.8.35.9.1.1.1.1.1'
                     ]  # S5820V2-54QS-GE, 对于无风扇设备没有OID

    # 将列表连接为带单引号的字符串
    oid_list_str = ', '.join([
        f"'{element}'"
        for element in public_oid + oid_version + oid_sn + oid_model +
        oid_cpu + oid_mem + oid_temperature + oid_power_state + oid_fan_state
    ])

    try:

        cmdGen = cmdgen.CommandGenerator()

        # getCmd

        errorIndication, errorStatus, errorIndex, varBinds = eval(
            f'cmdGen.getCmd(cmdgen.CommunityData(community_data), cmdgen.UdpTransportTarget((ip, 161)), {oid_list_str})'
        )

        # Check for errors and print out results
        if errorIndication:
            # print(ip + '_' + errorIndication)
            return
        else:
            if errorStatus:
                # print('%s at %s' %
                #       (errorStatus.prettyPrint(),
                #        errorIndex and varBinds[int(errorIndex) - 1] or '?'))
                return
            else:
                # print(varBinds, type(varBinds))
                for name, val in varBinds:

                    # print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
                    if str(name) == '1.3.6.1.2.1.1.1.0':
                        # print(f'设备系统描述：{val}')
                        # pysnmp_dict['sysdescr'] = str(val)
                        pass

                    elif str(name) == '1.3.6.1.2.1.1.5.0':
                        # print(f'设备名称：{val}')
                        pysnmp_dict['sysname'] = str(val)
                        pysnmp_dict['ip'] = ip
                        deal_with_sysname(pysnmp_dict)

                    elif str(name) == '1.3.6.1.2.1.1.3.0':
                        # print(f'设备启动时间：{val}')
                        # 获取到的是 timeticks value ，需要转换成人类能看懂的时间
                        device_uptime = datetime.timedelta(seconds=int(val) /
                                                           100)
                        # 移除秒后的小数位
                        device_uptime = str(device_uptime).split('.')[0]
                        # print(sysuptime, type(sysuptime))
                        pysnmp_dict['device_uptime'] = device_uptime

                    elif str(name) in oid_version:
                        if str(val):
                            # print(f'设备系统软件版本：{val}')
                            pysnmp_dict['device_version'] = str(val)

                    elif str(name) in oid_sn:
                        if str(val):
                            # print(f'设备序列号：{val}')
                            pysnmp_dict['device_sn'] = str(val)

                    elif str(name) in oid_model:
                        if str(val):
                            # print(f'设备型号：{val}')
                            pysnmp_dict['device_model'] = str(val)

                    elif str(name) in oid_cpu:
                        if str(val) and str(val) not in '0':
                            # print(f'设备CPU利用率：{val}')
                            pysnmp_dict['device_cpu'] = str(val) + '%'

                    elif str(name) in oid_mem:
                        if str(val) and str(val) not in '0':
                            # print(f'设备内存利用率：{val}')
                            pysnmp_dict['device_mem'] = str(val) + '%'

                    elif str(name) in oid_temperature:
                        if str(val) and str(val) != '65535':
                            # print(f'设备温度：{val}')
                            pysnmp_dict['device_temperature'] = str(val) + '°C'

                    elif str(name) in oid_power_state:
                        # print(f'设备电源状态：{val}')
                        if str(val) == '1':
                            pysnmp_dict['device_power_state'] = int(val)

                    elif str(name) in oid_fan_state:
                        if str(val):
                            # print(f'设备风扇状态：{val}')
                            pysnmp_dict['device_fan_state'] = int(val)
                        else:
                            pysnmp_dict['device_fan_state'] = 4

                    else:
                        print('有东西没查到哦')

            # 保持字典格式统一，对没有获取到值的key使用''填充
            # pysnmp_dict.setdefault('net_area','')
            # pysnmp_dict.setdefault('device_type','')
            # pysnmp_dict.setdefault('device_location','')
            pysnmp_dict.setdefault('device_uptime','')
            pysnmp_dict.setdefault('device_version','')
            pysnmp_dict.setdefault('device_model','')
            pysnmp_dict.setdefault('device_cpu','')
            pysnmp_dict.setdefault('device_mem','')
            pysnmp_dict.setdefault('device_power_state','')
            pysnmp_dict.setdefault('device_fan_state','')

            return pysnmp_dict
    except Exception as e:
        # return False, e + 'The SNMP of this device is not working.'
        # print(str(e))
        # print(f'IP地址 {ip} snmp查询出错111!')
        return


# 轮询结果处理
def deal_with_sysname(pysnmp_dict):
    """
    此函数根据特定格式的设备名称进行处理
    格式：局点_设备位置_网络区域_设备类型_厂商+型号
    例如：XXX_RDSBJ-10_JCW_AGGE_H3CS5170
    说明：XXX_弱电设备间-10_基础网_汇聚交换机_H3CS5170
    根据需要修改，不改也没关系，表格中的net_area，device_type，device_location三列显示为空
    """

    try:

        # 定义字符串接收 处理后的结果
        net_area_data = ''
        device_type_data = ''
        device_location_data = ''
        # 取出sysname，并以 '_' 分割
        split_data = pysnmp_dict['sysname'].split('_')
        # 判断sysname是否能被'_'分割，或分割后元素个数小于5，判断后进行填充
        if not split_data or len(split_data) < 5:
            pysnmp_dict['net_area'] = ''
            pysnmp_dict['device_type'] = ''
            pysnmp_dict['device_location'] = ''
            pass
        else:
            # 判断网络区域
            if split_data[-3] == 'JC':
                net_area_data = '集成网'
            elif split_data[-4] == 'JC':
                net_area_data = '集成网'
            elif split_data[-3] == 'JCW':
                net_area_data = '基础网'
            elif split_data[-4] == 'JCW':
                net_area_data = '基础网'
            # 根据需要添加更多 elif 判断 ……
            else:
                net_area_data = split_data[2]

            # 判断设备类型
            if split_data[-2] == 'SW':
                device_type_data = '核心交换机'
            elif split_data[-2] == 'AGGE':
                device_type_data = '汇聚交换机'
            elif split_data[-2] == 'ACC':
                device_type_data = '接入交换机'
            # 根据需要添加更多 elif 判断 ……
            else:
                device_type_data = split_data[-2]
            # print('设备类型是：' + device_type_data + split_data[-2])

            # 判断设备位置
            if split_data[1][0].isdigit():
                device_location_data = '信息机房' + split_data[1]
            elif split_data[1].startswith('RDSBJ-'):
                # 此处还要增加一个判断，有些位置 有-1 ，例如XXX_RDSBJ-14-1_JCW_AGGE_H3CS5170
                # 不能只获取到14 后面的 1 也要添加进来
                # XXX_RDSBJ-10_JCW_AGGE_H3CS5170
                # XXX_RDSBJ-14-1_JCW_AGGE_H3CS5170
                device_location_data = '弱电设备间' + split_data[1].split('-', 1)[1]
            elif split_data[1].startswith('RDJ-'):
                device_location_data = '弱电间' + split_data[1].split('-')[1]
            # 根据需要添加更多 elif 判断 ……
            else:
                device_location_data = split_data[1]

            pysnmp_dict['net_area'] = net_area_data
            pysnmp_dict['device_type'] = device_type_data
            pysnmp_dict['device_location'] = device_location_data


    except Exception as e:
        # print(str(e) + pysnmp_dict['sysname'])
        return


if __name__ == '__main__':

    res = do_pysnmp('172.31.100.10', 'public')
    print(res)
