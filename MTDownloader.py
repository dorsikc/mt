import os
import winreg as reg
import requests

if not os.path.exists("C:/cell3/mt"): os.makedirs("C:/cell3/mt")
if not os.path.exists("C:/cell3/mt/mt.bat"):
    with open("C:/cell3/mt/mt.bat", "w") as f:
        f.write("@echo off\npy C:\cell3\mt\mt.py %*")
if not os.path.exists("C:/cell3/mt/mt.py"):
    with open("C:/cell3/mt/mt.py", "w") as f:
        f.write(requests.get("https://raw.githubusercontent.com/dorsikc/mt/main/mt.py").text)

if not os.path.exists("C:/cell3/mt/modules"): os.makedirs("C:/cell3/mt/modules")
if not os.path.exists("C:/cell3/mt/projects"): os.makedirs("C:/cell3/mt/projects")

new_path = r'C:\cell3\mt'
path_key = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, path_key, 0, reg.KEY_SET_VALUE) as key:
    current_path, _ = reg.QueryValueEx(key, 'Path')
if new_path not in current_path:
    new_path = current_path + ';' + new_path
    reg.SetValueEx(key, 'Path', 0, reg.REG_EXPAND_SZ, new_path)
    print(f'Folder "{new_path}" successfuly added to PATH')
else:
    print(f'Folder "{new_path}" already added to PATH')