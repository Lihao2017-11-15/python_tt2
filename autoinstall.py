import sys
import os
import subprocess
ret = []
while True:
    msg = subprocess.getoutput("python main.py")
    nmn = "No module named"
    if msg.index("No module named"):
        modulename = msg[msg.index(nmn)+len(nmn)+1:].split("'")[1]
        ret.append(modulename)
        os.system(f"pip install {modulename}")
        if subprocess.getoutput(f"pip install {modulename}").index("ERROR: No matching distribution found for")>0:
            print("模块名称错误，需要手动安装")
            sys.exit()
    else:
        break

print(f"自动安装模块：{ret}")    