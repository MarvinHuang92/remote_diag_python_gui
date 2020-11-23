# -*- coding: UTF-8 -*-

import os, shutil, time, datetime
from tkinter import *
from tkinter import ttk, filedialog  #, dialog
import threading
# import queue

import sys
sys.path.append('..')
from test_scripts import sendAndReceive as sr

config_path = 'cfg/default.ini'
config_dir = 'cfg/'
Authorship = 'Authors: Zhang Di, Huang Marvin, Wang Jian, Wei Haixia, HM Shashikumar from CC-DA/EDB2-CN'

threading.TIMEOUT_MAX = 10  # 设置threading全局超时时间。

class MyThread(threading.Thread):
    def __init__(self, func, name, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.name = name
        self.args = args
 
    def run(self):
        self.result = self.func(*self.args)
 
    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception as e:
            print(e)
            return None

'''
# 生成时间戳方法
def fmtTime(timeStamp):
    timeArray = time.localtime(timeStamp)
    dateTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return dateTime

#自定义re_Text,用于将stdout映射到Queue
class re_Text():
    def __init__(self, queue):
        self.queue = queue
    def write(self, content):
        self.queue.put(content)
'''

class App:
    def __init__(self, master):
        self.master = master
        # 启动时初始化
        self.initWidgets()
        self.initConfig()
        '''
        #new 一个Quue用于保存输出内容
        self.msg_queue = queue.Queue()
        #启动after方法
        self.master.after(100, self.show_msg)
    
    #在show_msg方法里，从Queue取出元素，输出到Trace
    def show_msg(self):
        while not self.msg_queue.empty():
            content = self.msg_queue.get()
            self.t_trace.insert('end', msg + '\n')
            self.t_trace.yview_moveto(1)  # 滚动条移动至最下
 
        #after方法再次调用show_msg
        self.master.after(100, self.show_msg)
        '''

    def initWidgets(self):
        # 声明所有变量
        self.v_txid = StringVar()       #0
        self.v_rxid = StringVar()       #1
        self.v_channel = StringVar()     #2
        self.v_console_input = StringVar()        #3
        self.v_measure_switch = BooleanVar()  #4
        self.v_trace_switch = BooleanVar()#5
        # self.v_rename = BooleanVar()    #6
        # self.v_target_name = StringVar()#7
        # self.v_upload = BooleanVar()    #8
        # self.v_interval = IntVar()      #9
        # self.v_buffer = IntVar()        #10
        # self.v_sfx_dev = BooleanVar()   #11
        # self.v_sfx_stub = BooleanVar()  #12
        # self.v_sfx_sr = BooleanVar()    #13
        # self.v_sfx_flt = BooleanVar()   #14
        # self.v_a2l_dev = BooleanVar()   #15
        # self.v_a2l_stub = BooleanVar()  #16
        # self.v_a2l_sr = BooleanVar()    #17
        # self.v_a2l_flt = BooleanVar()   #18
        self.v_coem_path = StringVar()  #19

        # 设置容器 Frame
        # Layer 1
        f_top = Frame(self.master)
        f_log = Frame(self.master)
        f_top.pack(side=TOP, pady=10)
        f_log.pack(side=BOTTOM, pady=16)
        
        # Layer 2
        f_panel = Frame(f_top)
        f_com = Frame(f_top)
        f_diag = Frame(f_top)
        f_panel.pack(side=LEFT, padx=12)
        f_diag.pack(side=LEFT, padx=12)
        f_com.pack(side=RIGHT, padx=12)
        
        # Layer 3
        f_console_1 = Frame(f_diag)
        f_console_2 = Frame(f_diag)
        f_console_1.pack(side=TOP, pady=3)
        f_console_2.pack(side=BOTTOM, pady=3)
        f_trace_1 = Frame(f_com)
        f_trace_2 = Frame(f_com)
        f_trace_1.pack(side=TOP, pady=3)
        f_trace_2.pack(side=BOTTOM, pady=3)

        # 设置Widget
        # Panel Frame
        Label(f_panel, text='-Control Panel-', width=15).grid(row=0, column=0, padx=5, pady=10)
        Button(f_panel, text='Device Online', width=15, command=self.device_online).grid(row=1, column=0, padx=5, pady=5)
        Button(f_panel, text='Device Offline', width=15, command=self.device_offline).grid(row=1, column=1, padx=5, pady=5)
        Button(f_panel, text='START ', width=15, height=3, command=self.start_trace).grid(row=12, column=0, padx=5, pady=5)
        Button(f_panel, text=' STOP ', width=15, height=3, command=self.stop_trace).grid(row=12, column=1, padx=5, pady=5)
        
        Label(f_panel, text='       Channel:', width=15).grid(row=3, column=0, padx=5, pady=5)
        Label(f_panel, text='Diag Msg ID Tx:', width=15).grid(row=4, column=0, padx=5, pady=5)
        Label(f_panel, text='Diag Msg ID Rx:', width=15).grid(row=5, column=0, padx=5, pady=5)
        ttk.Combobox(f_panel, width=13, textvariable=self.v_channel, values=['can0','can1']).grid(row=3, column=1, padx=5, pady=5)
        ttk.Combobox(f_panel, width=13, textvariable=self.v_txid, values=['0x7A5','0x7A6']).grid(row=4, column=1, padx=5, pady=5)
        ttk.Combobox(f_panel, width=13, textvariable=self.v_rxid, values=['0x7AD','0x7AE']).grid(row=5, column=1, padx=5, pady=5)

        # 占位空白label
        Label(f_panel, text='               ', width=15).grid(row=2, column=0, padx=10, pady=5)
        
        # Label(f_panel, text='               ', width=15).grid(row=6, column=0, padx=10, pady=5)
        Label(f_panel, text='               ', width=15).grid(row=7, column=0, padx=10, pady=5)
        Label(f_panel, text='               ', width=15).grid(row=8, column=0, padx=10, pady=5)
        Label(f_panel, text='               ', width=15).grid(row=9, column=0, padx=10, pady=5)
        Label(f_panel, text='               ', width=15).grid(row=10, column=0, padx=10, pady=5)
        Label(f_panel, text='               ', width=15).grid(row=11, column=0, padx=10, pady=5)
        
        # save config button
        Button(f_panel, text='Save Config', width=15, command=self.saveConfig).grid(row=6, column=0, padx=5, pady=5)
        Button(f_panel, text='Reset Config', width=15, command=self.writeConfig).grid(row=6, column=1, padx=5, pady=5)
        
        '''
        # 在另一个方法中调用了这个widget，所以给它self前缀方便调用
        # 不能将grid写在同一行，否则会在给名字赋值时，将Entry类型理解成NoneType，所有属性都无法识别
        self.cb_sfx_dev = Checkbutton(f_top, text='Develop (Default)', variable=self.v_sfx_dev, command=self.check)
        self.cb_sfx_dev.grid(row=0, column=4, padx=10)
        '''
        
        # Console Frame
        Label(f_console_1, text='-Diag Console- ', width=42, anchor=W).grid(row=0, column=0, padx=5, pady=10)
        
        f_ts_console = Frame(f_console_1)
        f_ts_console.grid(row=1, column=0, padx=5)
        scroll_console = Scrollbar(f_ts_console)  # 滚动条
        scroll_console.pack(side=RIGHT, fill=Y)  # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充与否
        self.t_console = Text(f_ts_console, height=19, width=40)
        self.t_console.pack(side=LEFT, fill=Y)  # 将文本框填充进窗口的左侧
        scroll_console.config(command=self.t_console.yview) # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
        self.t_console.config(yscrollcommand=scroll_console.set) # 将滚动条关联到文本框
        
        Label(f_console_1, text='Input:', width=42, anchor=W).grid(row=2, column=0, padx=5, pady=5)
        Entry(f_console_1, width=42, textvariable=self.v_console_input).grid(row=3, column=0, padx=10, pady=3)
        
        Button(f_console_2, text='Send', width=13, command=self.console_send).grid(row=0, column=0)
        Label(f_console_2, text='', width=9).grid(row=0, column=1)
        Button(f_console_2, text='Clean', width=13, command=self.console_clean).grid(row=0, column=2)

        
        # Trace Frame
        Label(f_trace_1, text='-Trace-', width=56, anchor=W).grid(row=0, column=0, padx=5, pady=10)
        Label(f_trace_1, text='Time | ID | DLC | Data', width=56, anchor=W).grid(row=1, column=0, padx=5, pady=2)
        f_ts_trace = Frame(f_trace_1)
        f_ts_trace.grid(row=2, column=0, padx=5)
        scroll_trace = Scrollbar(f_ts_trace)  # 滚动条
        scroll_trace.pack(side=RIGHT, fill=Y)
        self.t_trace = Text(f_ts_trace, height=21, width=54)
        self.t_trace.pack(side=LEFT, fill=Y)
        scroll_trace.config(command=self.t_trace.yview)
        self.t_trace.config(yscrollcommand=scroll_trace.set)

        Button(f_trace_2, text='Pause', width=13, command=self.pause_trace).grid(row=0, column=1)
        Button(f_trace_2, text='Clean', width=13, command=self.trace_clean).grid(row=0, column=2, padx=30, pady=2)
        Button(f_trace_2, text='Save', width=13, command=self.trace_save).grid(row=0, column=3)


        # Log Frame
        # self.canvas = Canvas(f_log, width=50, height=50)
        # self.canvas.grid(row=0, column=0)
        # image = PhotoImage(file='./img/RPI.ppm')
        # self.canvas.create_image(50,50,anchor=CENTER,image=image)
        Label(f_log, text='Log: ', width=42, anchor=E).grid(row=0, column=1)
        
        f_ts_log = Frame(f_log)
        f_ts_log.grid(row=0, column=2, padx=3, pady=2)
        scroll_log = Scrollbar(f_ts_log)  # 滚动条
        scroll_log.pack(side=RIGHT, fill=Y)
        self.t_log = Text(f_ts_log, height=8, width=102)
        self.t_log.pack(side=LEFT, fill=Y)
        scroll_log.config(command=self.t_log.yview)
        self.t_log.config(yscrollcommand=scroll_log.set)
        
        Label(f_log, text=Authorship, width=102, anchor=E).grid(row=1, column=2)
        

    def dummy_func(self):
        self.new_print('Dummy function running.')
    
    def new_print(self, info):  # 用来将print内容同时显示在log窗口
        print(info)
        self.t_log.insert('end', info + '\n')
        self.t_log.yview_moveto(1)  # 滚动条移动至最下
        # self.t_log.update()
    
    def device_online(self):
        self.new_print('* Device Online.')
        cmd_online_1 = 'sudo ip link set can0 up type can bitrate 500000 dbitrate 2000000 restart-ms 100 berr-reporting on fd on'
        cmd_online_2 = 'sudo ip link set can1 up type can bitrate 500000 dbitrate 2000000 restart-ms 100 berr-reporting on fd on'
        cmd_online_3 = 'sudo ifconfig can0 txqueuelen 65536'
        cmd_online_4 = 'sudo ifconfig can1 txqueuelen 65536'
        os.system(cmd_online_1)
        os.system(cmd_online_2)
        os.system(cmd_online_3)
        os.system(cmd_online_4)
        self.new_print(cmd_online_1)
        self.new_print(cmd_online_2)
        self.new_print(cmd_online_3)
        self.new_print(cmd_online_4)
    
    def device_offline(self):
        self.new_print('* Device Offline.')
        cmd_offline_1 = 'sudo ip link set can0 down'
        cmd_offline_2 = 'sudo ip link set can1 down'
        os.system(cmd_offline_1)
        os.system(cmd_offline_2)
        self.new_print(cmd_offline_1)
        self.new_print(cmd_offline_2)
    
    def get_time(self):
        timeStamp = time.time()  # 1381419600
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y%m%d_%H%M%S", timeArray)
        return otherStyleTime  # 20131010_234000
    
    def console_send(self):
        input = self.v_console_input.get().strip()
        if input != '':
            # 'insert'参数表示插入光标当前位置
            # self.t_console.insert('insert', "Text\n")
            # 'end'参数表示始终插入末尾
            self.t_console.insert('end', 'Tx: ' + input + '\n')
            self.t_console.yview_moveto(1)  # 滚动条移动至最下
            
            T_send = MyThread(func=sr.main_return, name='sending_msg', args=(input, ))
            T_send.start()
            T_send.join()
            res = T_send.get_result()
            print(res)
    
    def console_clean(self):
        self.t_console.delete(1.0, 'end')
    
    def trace_clean(self):
        self.t_trace.delete(1.0, 'end')
    
    def trace_save(self):
        trace_content = self.t_trace.get(1.0, 'end').strip()
        trace_filename = "logs/Trace_%s.log" % self.get_time()
        # os.system("if not exist logs mkdir logs")
        with open(trace_filename, 'w') as f:
            f.writelines(trace_content)
            f.close()
        self.new_print('Trace saved as: ' + trace_filename)

    def writeini(self, config_path):
        with open(config_path, 'w') as f:  # 如果不存在会自动创建，'w'表示写数据，写之前会清空文件中的原有数据
            f.write(self.v_txid.get() + '\n')        #0
            f.write(self.v_rxid.get() + '\n')       #1
            f.write(self.v_channel.get() + '\n')         #2
            f.write(self.v_console_input.get() + '\n')            #3
            f.write(str(self.v_measure_switch.get()) + '\n')      #4
            f.write(str(self.v_trace_switch.get()) + '\n')    #5
            # f.write(str(self.v_rename.get()) + '\n')    #6
            # f.write(self.v_target_name.get() + '\n')    #7
            # f.write(str(self.v_upload.get()) + '\n')    #8
            # f.write(str(self.v_interval.get()) + '\n')  #9
            # f.write(str(self.v_buffer.get()) + '\n')    #10
            # f.write(str(self.v_sfx_dev.get()) + '\n')   #11
            # f.write(str(self.v_sfx_stub.get()) + '\n')  #12
            # f.write(str(self.v_sfx_sr.get()) + '\n')    #13
            # f.write(str(self.v_sfx_flt.get()) + '\n')   #14
            # f.write(str(self.v_a2l_dev.get()) + '\n')   #15
            # f.write(str(self.v_a2l_stub.get()) + '\n')  #16
            # f.write(str(self.v_a2l_sr.get()) + '\n')    #17
            # f.write(str(self.v_a2l_flt.get()) + '\n')   #18
            f.write(str(self.v_coem_path.get()))        #19  # 最后一行不用换行
            
    # 保存到 default.ini
    def saveConfig(self):
        self.writeini(config_path)
        self.new_print('Config Saved.')

    def readini(self, config_path):
        with open(config_path, 'r') as f:
            self.value_ = f.readlines()         # 注意：readlines返回一个list，角标是行号，readline的角标是（每一行）的列号
            self.v_txid.set(self.value_[0].strip())
            self.v_rxid.set(self.value_[1].strip())
            self.v_channel.set(self.value_[2].strip())
            self.v_console_input.set(self.value_[3].strip())
            self.v_repo_path.set(self.value_[4].strip())
            self.v_destination.set(self.value_[5].strip())
            self.v_rename.set(self.value_[6].strip())
            self.v_target_name.set(self.value_[7].strip())
            self.v_upload.set(self.value_[8].strip())
            self.v_interval.set(self.value_[9].strip())
            self.v_buffer.set(self.value_[10].strip())
            self.v_sfx_dev.set(self.value_[11].strip())
            self.v_sfx_stub.set(self.value_[12].strip())
            self.v_sfx_sr.set(self.value_[13].strip())
            self.v_sfx_flt.set(self.value_[14].strip())
            self.v_a2l_dev.set(self.value_[15].strip())
            self.v_a2l_stub.set(self.value_[16].strip())
            self.v_a2l_sr.set(self.value_[17].strip())
            self.v_a2l_flt.set(self.value_[18].strip())
            self.v_coem_path.set(self.value_[19].strip())
            
    # 读取.ini的内容
    def writeConfig(self):
        # 可能不存在对应的文件，try防止报错
        try:
            self.readini(config_path)
        except:
            pass
        self.new_print('Config Read.')
        
    # 启动时初始化
    def initConfig(self):
        try:
            self.readini(config_path)  # 读取初始值（上次Start时保存的值）
        except:
            pass  # 如果找不到初始值，就算了(留空)
        self.v_measure_switch.set(False)
        self.v_trace_switch.set(False)

    def start_trace(self):
        self.new_print('* Start Receiving Messages...')
        self.v_measure_switch.set(True)
        self.v_trace_switch.set(True)
        
        T_start = threading.Thread(target=self.__show_trace, args=('msg.', 0.02))
        T_start.start()
        
    def stop_trace(self):
        self.new_print('* Stop Receiving Messages...')
        self.v_measure_switch.set(False)
        
    def pause_trace(self):
        self.v_trace_switch.set(not self.v_trace_switch.get())
        
        
    # 主要函数，在trace中显示报文
    def __show_trace(self, msg, interval=0):
        T_receive = MyThread(func=sr.main_return, name='sending_msg', args=('121212', ))
        T_receive.start()
        T_receive.join()
        while self.v_measure_switch.get():
            if self.v_trace_switch.get():
                msg = T_receive.get_result()
                self.t_trace.insert('end', msg + '\n')
                self.t_trace.yview_moveto(1)  # 滚动条移动至最下
            if interval:
                time.sleep(interval)
        
 
        



root = Tk()  # 创建Tk对象，Tk代表窗口
root.title('Raspberrypi Remote Diagnostics')  # 设置窗口标题
# for Windows 10
#root.option_add("*Font", ('Courier10 BT', 10))  # 设置全局字体，这样就不用每个控件单独指定字体
# for linux
root.option_add("*Font", ('Monospace', 10))  # 设置全局字体，这样就不用每个控件单独指定字体


w = 1240
h = 700

# 定义函数：令窗口居中
def center_window(w=300, h=200):
    ws = root.winfo_screenwidth()  # 读取显示器分辨率
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)  # x,y是窗口左上角坐标
    y = (hs / 2) - (h / 2)
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))
    root.resizable(False, False)  # 禁止窗口缩放（第一个宽，第二个高）

center_window(w, h)  # 调用自定义函数令窗口居中

# 改变窗口图标
# root.iconbitmap('images/fklogo.ico')
App(root)
root.mainloop()

