'''
程序入口
'''
import sys
import os
from os import system
import getpass

# import win32com.client
import msoffcrypto
import io
import pandas as pd
from termcolor import colored

from lib import comm


def unlock_xlsx():
    """
    输入保护密码打开 inventory 目录下带保护密码的 excel 文件，并生成一个去除保护密码的副本，最后启动 func_list.py
    """

    retry_times = 0
    while retry_times < 3:
        try:

            # ubuntu 22.04 environment / windows platform
            # password retry
            password = getpass.getpass('输入密码：').strip()
            # 定义inventory路径
            original_file_path = os.path.normpath(os.path.join(comm.BASE_PATH, 'inventory', 'inventory_protected.xlsx'))
            target_file_path = os.path.normpath(os.path.join(comm.BASE_PATH, 'inventory', 'inventory_unprotected.xlsx'))

            decrypted = io.BytesIO()

            with open(original_file_path, "rb") as f:
                file = msoffcrypto.OfficeFile(f)
                file.load_key(password=password)  # Use password
                file.decrypt(decrypted)

            df = pd.read_excel(decrypted)
            df.to_excel(target_file_path, index=False)
            os.system(f"python {comm.BASE_PATH}/func/func_list.py")
            sys.exit()

        except Exception:
            retry_times += 1
            if retry_times == 3:
                print(colored('-' * 42 + '\n>>>输错三次，重新再来<<<', 'red'))
                break


def StartedTheEngine():
    """
    判断无保护密码的inventory.xlsx文件副本已存在，如已存在直接启动 func_list.py，否则调用函数 unlock_xlsx()
    """
    exists_xlsx = os.path.normpath(os.path.join(comm.BASE_PATH, 'inventory', 'inventory_unprotected.xlsx'))
    if os.path.exists(exists_xlsx):
        os.system(f"python {comm.BASE_PATH}/func/func_list.py")
        sys.exit()
    else:
        print('-' * 42)
        print(colored('没有已解锁的inventory文件，先解锁', 'blue'))
        unlock_xlsx()


# 命令行窗口标题
system("title Python-NetOps_2.0_beta")

if __name__ == "__main__":

    StartedTheEngine()
