import subprocess
p = subprocess.Popen('candump can1', shell=True, stdout=subprocess.PIPE)
for i in iter(p.stdout.readline, 'b'):
    if not i:
        break
    print(i.decode('gbk'))