import subprocess
import sys


# 常用编码
GBK = 'gbk'
UTF8 = 'utf-8'

# 解码方式，一般 py 文件执行为utf-8 ，cmd 命令为 gbk
current_encoding = UTF8 


popen = subprocess.Popen(['python3', '../msg_generator.py'],  # 需要执行的文件路径
                         stdout = subprocess.PIPE,
                         stderr = subprocess.PIPE,
                         bufsize=1)

# 重定向标准输出
while popen.poll() is None:                      # None表示正在执行中
    r = popen.stdout.readline().decode(current_encoding)
    print(r)
#    sys.stdout.write(r)                                # 可修改输出方式，比如控制台、文件等

# 重定向错误输出
if popen.poll() != 0:                                   # 不为0表示执行错误
    err = popen.stderr.read().decode(current_encoding)
#    sys.stdout.write(err)                             # 可修改输出方式，比如控制台、文件等