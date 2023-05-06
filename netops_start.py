'''
程序入口
'''
import sys
import os
from os import system
# import subprocess
import getpass

# import win32com.client
import msoffcrypto
import io
import pandas as pd
from termcolor import colored

from lib import comm

backup_path, config_path, generate_table, BASE_PATH, EXPORT_PATH, dir_name = comm.create_path()


# 解锁带保护密码的inventory excel 文件
def unlock_xlsx():
    retry_times = 0
    while retry_times < 3:
        try:
            # windows platform
            # password retry 
            # password = getpass.getpass('输入密码：')
            # # 定义inventory路径
            # original_file_path = BASE_PATH + "\\inventory\\inventory_protected.xlsx"
            # target_file_path = BASE_PATH + "\\inventory\\inventory_unprotected.xlsx"
            # # 创建 Excel 应用程序对象
            # excel = win32com.client.Dispatch("Excel.Application")
            # # 打开需要解锁的 Excel 文件，输入密码
            # workbook = excel.Workbooks.Open(original_file_path, False, True, None, password)
            # # 另存为无密码文件
            # workbook.SaveAs(target_file_path, None, "", "")
            # # 关闭工作簿和 Excel 应用程序
            # workbook.Close(False)
            # excel.Quit()
            # os.system(f"python {BASE_PATH}/func/func_list.py")
            # # subprocess.Popen(['python', ' netops_start.py'])
            # sys.exit()

            # ubuntu 22.04 env
            # password retry
            password = getpass.getpass('输入密码：')
            # 定义inventory路径
            original_file_path = BASE_PATH + "\\inventory\\inventory_protected.xlsx"
            target_file_path = BASE_PATH + "\\inventory\\inventory_unprotected.xlsx"

            decrypted = io.BytesIO()

            with open(original_file_path, "rb") as f:
                file = msoffcrypto.OfficeFile(f)
                file.load_key(password=password)  # Use password
                file.decrypt(decrypted)

            df = pd.read_excel(decrypted)
            df.to_excel(target_file_path, index=False)
            os.system(f"python {BASE_PATH}/func/func_list.py")
            # subprocess.Popen(['python', ' netops_start.py'])
            sys.exit()
        except Exception:
            retry_times += 1
            if retry_times == 3:
                print(colored('-' * 42 + '\n>>>输错三次，重新再来<<<', 'red'))
                break


# 确认无保护密码的inventory.xlsx文件已生成
def StartedTheEngine():

    exists_xlsx = '%s\\inventory\\inventory_unprotected.xlsx' % (BASE_PATH)
    if os.path.exists(exists_xlsx):
        os.system(f"python {BASE_PATH}/func/func_list.py")
        # subprocess.Popen(['python', 'netops_start.py'])
        sys.exit()
    else:
        print('-' * 42)
        print(colored('没有已解锁的inventory文件，先解锁', 'blue'))
        unlock_xlsx()


system("title Python-NetOps_2.0_beta")

# 开始执行
if __name__ == "__main__":

    # 执行
    StartedTheEngine()
