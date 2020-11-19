# -*- coding:UTF-8 -*-

import os, shutil, time, datetime
from tkinter import *
from tkinter import ttk, filedialog  #, dialog

config_path = 'cfg/default.ini'
config_dir = 'cfg/'
Authorship = 'Authors: Zhang Di, Huang Marvin, Wang Jian, Wei Haixia, HM Shashikumar from CC-DA/EDB2-CN'

class App:
    def __init__(self, master):
        self.master = master
        self.initWidgets()
        try:
            self.initValues()  # 读取初始值（上次Start时保存的值）
            self.check()       # 在初始化时根据checkbox状态决定entry是否可用，默认是False，所以这个步骤必须在initValues之后，而不能写在initWidget里面，不然即使ini中写了True也读不进来
        except:
            pass  # 如果找不到初始值，就算了(留空)

    def initWidgets(self):
        # 声明所有变量
        self.v_txid = StringVar()       #0
        self.v_rxid = StringVar()       #1
        
        self.v_console_input = StringVar()     #2
        self.v_tag = StringVar()        #3
        self.v_repo_path = StringVar()  #4
        self.v_destination = StringVar()#5
        self.v_rename = BooleanVar()    #6
        self.v_target_name = StringVar()#7
        self.v_upload = BooleanVar()    #8
        self.v_interval = IntVar()      #9
        self.v_buffer = IntVar()        #10
        self.v_sfx_dev = BooleanVar()   #11
        self.v_sfx_stub = BooleanVar()  #12
        self.v_sfx_sr = BooleanVar()    #13
        self.v_sfx_flt = BooleanVar()   #14
        self.v_a2l_dev = BooleanVar()   #15
        self.v_a2l_stub = BooleanVar()  #16
        self.v_a2l_sr = BooleanVar()    #17
        self.v_a2l_flt = BooleanVar()   #18
        self.v_coem_path = StringVar()  #19

        # 设置容器 Frame
        # Layer 1
        f_top = Frame(self.master)
        f_log = Frame(self.master)
        f_top.pack(side=TOP, pady=10)
        f_log.pack(side=BOTTOM, pady=16)
        # Layer 2
        f_panels = Frame(f_top)
        f_consoles = Frame(f_top)
        f_panels.pack(side=LEFT, padx=12)
        f_consoles.pack(side=RIGHT, padx=12)
        # Layer 3
        f_panel_1 = Frame(f_panels)
        f_panel_2 = Frame(f_panels)
        f_panel_1.pack(side=TOP, pady=3)
        f_panel_2.pack(side=BOTTOM, pady=3)
        f_console_1 = Frame(f_consoles)
        f_console_2 = Frame(f_consoles)
        f_console_1.pack(side=TOP, pady=3)
        f_console_2.pack(side=BOTTOM, pady=3)

        # 设置Widget
        # Panel 1 Frame
        Label(f_panel_1, text='Diag Messege ID', width=15).grid(row=0, column=0, padx=10, pady=5)
        Label(f_panel_1, text='Sending        ', width=15).grid(row=1, column=0, padx=10, pady=5)
        Label(f_panel_1, text='Response       ', width=15).grid(row=1, column=1, padx=10, pady=5)
        Entry(f_panel_1, width=15, textvariable=self.v_console_input).grid(row=1, column=0, padx=10, pady=5)
        Entry(f_panel_1, width=15, textvariable=self.v_console_input).grid(row=1, column=1, padx=10, pady=5)
        ttk.Combobox(f_panel_1, width=15, textvariable=self.v_txid, values=['0x7DA', '0x7DA', '0x7DA', '0x7DA', '0x7DA']).grid(row=2, column=0)
        ttk.Combobox(f_panel_1, width=15, textvariable=self.v_txid, values=['0x7DA', '0x7DA', '0x7DA', '0x7DA', '0x7DA']).grid(row=2, column=1)
        # 占位空白label
        Label(f_panel_1, text='               ', width=15).grid(row=3, column=0, padx=10, pady=5)
        Label(f_panel_1, text='               ', width=15).grid(row=4, column=0, padx=10, pady=5)
        Label(f_panel_1, text='               ', width=15).grid(row=5, column=0, padx=10, pady=5)
        Label(f_panel_1, text='               ', width=15).grid(row=6, column=0, padx=10, pady=5)
        Label(f_panel_1, text='               ', width=15).grid(row=7, column=0, padx=10, pady=5)
        Label(f_panel_1, text='               ', width=15).grid(row=8, column=0, padx=10, pady=5)
        
        # Panel 2 Frame
        Label(f_panel_2, text='Panel 2        ', width=15).grid(row=0, column=0, padx=10, pady=5)
        # 空白按钮
        Button(f_panel_2, text='Demo Button    ', width=11, command=self.dummy_func).grid(row=2, column=0)
        
        '''
        # 在另一个方法中调用了这个widget，所以给它self前缀方便调用
        # 不能将grid写在同一行，否则会在给名字赋值时，将Entry类型理解成NoneType，所有属性都无法识别
        self.cb_sfx_dev = Checkbutton(f_top, text='Develop (Default)', variable=self.v_sfx_dev, command=self.check)
        self.cb_sfx_dev.grid(row=0, column=4, padx=10)
        '''
        
        # Console Frame
        Label(f_console_1, text='Console', width=7).grid(row=0, column=0)
        
        f_ts_console = Frame(f_console_1)
        f_ts_console.grid(row=0, column=1, padx=10, pady=5)
        scroll_console = Scrollbar(f_ts_console)  # 滚动条
        scroll_console.pack(side=RIGHT, fill=Y)  # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充与否
        self.t_console = Text(f_ts_console, height=20, width=60)
        self.t_console.pack(side=LEFT, fill=Y)  # 将文本框填充进窗口的左侧
        scroll_console.config(command=self.t_console.yview) # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
        self.t_console.config(yscrollcommand=scroll_console.set) # 将滚动条关联到文本框
        
        Label(f_console_1, text='Input  ', width=7).grid(row=1, column=0)
        Entry(f_console_1, width=62, textvariable=self.v_console_input).grid(row=1, column=1, padx=10, pady=3)
        
        Label(f_console_2, text='  ', width=7).grid(row=0, column=0)  # 占位用
        Button(f_console_2, text='   Send   ', width=12, command=self.send_msg).grid(row=0, column=1)
        Button(f_console_2, text='  Clean   ', width=12, command=self.clean_msg).grid(row=0, column=2, padx=45)
        Button(f_console_2, text='Save As...', width=12, command=self.save_msg).grid(row=0, column=3)

        # Log Frame
        Label(f_log, text='Log', width=4, anchor=W).grid(row=0, column=0)
        
        f_ts_log = Frame(f_log)
        f_ts_log.grid(row=0, column=1, padx=3, pady=2)
        scroll_log = Scrollbar(f_ts_log)  # 滚动条
        scroll_log.pack(side=RIGHT, fill=Y)
        self.t_log = Text(f_ts_log, height=8, width=96)
        self.t_log.pack(side=LEFT, fill=Y)
        scroll_log.config(command=self.t_log.yview)
        self.t_log.config(yscrollcommand=scroll_log.set)
        
        Label(f_log, text=Authorship, width=96, anchor=E).grid(row=1, column=1)
        

    def dummy_func(self):
        print('Dummy function running.')
        
    def get_time(self):
        timeStamp = time.time()  # 1381419600
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y%m%d_%H%M%S", timeArray)
        return otherStyleTime  # 20131010_234000
    
    def send_msg(self):
        input = self.v_console_input.get().strip()
        if input != '':
            # 'insert'参数表示插入光标当前位置
            # self.t_console.insert('insert', "Text\n")
            # 'end'参数表示始终插入末尾
            self.t_console.insert('end', input + '\n')
    
    def clean_msg(self):
        self.t_console.delete(1.0, 'end')
    
    def save_msg(self):
        console_content = self.t_console.get(1.0, 'end').strip()
        console_filename = "logs/Console_%s.log" % self.get_time()
        os.system("if not exist logs mkdir logs")
        with open(console_filename, 'w') as f:
            f.writelines(console_content)
            f.close()
        self.t_log.insert('end', 'Consoles saved as: ' + console_filename + '\n')


    # 改变entry是否处于活动状态，注意顺序：先检查sfx再检查a2l
    def check(self):
        # upoad
        if not self.v_upload.get():
            self.e_destination.config(state='disabled')
        else:
            self.e_destination.config(state='normal')
        # rename
        if not self.v_rename.get():
            self.e_target_name.config(state='disabled')
        else:
            self.e_target_name.config(state='normal')
        # Dev软件和Flt不能同时做
        if self.v_sfx_dev.get():
            self.v_sfx_flt.set(False)
            self.cb_sfx_flt.config(state='disabled')
        else:
            self.cb_sfx_flt.config(state='normal')
        if self.v_sfx_flt.get():
            self.v_sfx_dev.set(False)
            self.v_sfx_stub.set(False)
            self.v_sfx_sr.set(False)
            self.cb_sfx_dev.config(state='disabled')
            self.cb_sfx_stub.config(state='disabled')
            self.cb_sfx_sr.config(state='disabled')
        else:
            self.cb_sfx_dev.config(state='normal')
            self.cb_sfx_stub.config(state='normal')
            self.cb_sfx_sr.config(state='normal')
        # a2l_dev
        if not self.v_sfx_dev.get():
            self.cb_a2l_dev.config(state='disabled')
        else:
            self.cb_a2l_dev.config(state='normal')
        # a2l_stub
        if not self.v_sfx_stub.get():
            self.cb_a2l_stub.config(state='disabled')
        else:
            self.cb_a2l_stub.config(state='normal')
        # a2l_sr 是默认disable的
        # a2l_flt
        if not self.v_sfx_flt.get():
            self.cb_a2l_flt.config(state='disabled')
        else:
            self.cb_a2l_flt.config(state='normal')

    # 获取桌面路径
    def get_desktop(self):
        desktop_raw = os.path.join(os.path.expanduser("~"), 'Desktop')
        return desktop_raw.replace('\\', '/').strip()

    # 选择destination路径
    def selectPath_dest(self):
        self.path_ = filedialog.askdirectory(initialdir=self.get_desktop())
        if self.path_ is not '':
            self.v_destination.set(self.path_)

    # 选择repo_path路径
    def selectPath_repo(self):
        # self.path_ = filedialog.askopenfilename(initialdir=self.get_desktop())  # 这个方法选择文件
        self.path_ = filedialog.askdirectory(initialdir=self.get_desktop())  # 这个方法选择文件夹
        if self.path_ is not '':
            self.v_repo_path.set(self.path_)

    def writeini(self, config_path):
        with open(config_path, 'w') as f:  # 如果不存在会自动创建，'w'表示写数据，写之前会清空文件中的原有数据
            f.write(self.v_txid.get() + '\n')        #0
            f.write(self.v_rxid.get() + '\n')       #1
            f.write(self.v_console_input.get() + '\n')         #2
            f.write(self.v_tag.get() + '\n')            #3
            f.write(self.v_repo_path.get() + '\n')      #4
            f.write(self.v_destination.get() + '\n')    #5
            f.write(str(self.v_rename.get()) + '\n')    #6
            f.write(self.v_target_name.get() + '\n')    #7
            f.write(str(self.v_upload.get()) + '\n')    #8
            f.write(str(self.v_interval.get()) + '\n')  #9
            f.write(str(self.v_buffer.get()) + '\n')    #10
            f.write(str(self.v_sfx_dev.get()) + '\n')   #11
            f.write(str(self.v_sfx_stub.get()) + '\n')  #12
            f.write(str(self.v_sfx_sr.get()) + '\n')    #13
            f.write(str(self.v_sfx_flt.get()) + '\n')   #14
            f.write(str(self.v_a2l_dev.get()) + '\n')   #15
            f.write(str(self.v_a2l_stub.get()) + '\n')  #16
            f.write(str(self.v_a2l_sr.get()) + '\n')    #17
            f.write(str(self.v_a2l_flt.get()) + '\n')   #18
            f.write(str(self.v_coem_path.get()))        #19
            
    # 保存到 default.ini 和 项目名.ini
    def saveConfig(self):
        self.writeini(config_path)
        self.writeini(config_dir + self.v_txid.get() + '.ini')

    def readini(self, config_path):
        with open(config_path, 'r') as f:
            self.value_ = f.readlines()         # 注意：readlines返回一个list，角标是行号，readline的角标是（每一行）的列号
            self.v_txid.set(self.value_[0].strip())
            self.v_rxid.set(self.value_[1].strip())
            self.v_console_input.set(self.value_[2].strip())
            self.v_tag.set(self.value_[3].strip())
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
    
    # 启动时，读取default.ini内容
    def initValues(self):
        self.readini(config_path)
        if self.v_txid.get().strip() == '':
            self.v_txid.set('BJEV')
        if self.v_rxid.get().strip() == '':
            self.v_rxid.set('HMU5SZH')
        if self.v_coem_path.get().strip() == '':
            self.v_rxid.set('apl/saic')
            
    # 读取 对应项目名.ini 的内容
    def refreshValues(self):
        # 可能不存在对应的文件，try防止报错
        try:
            self.readini(config_dir + self.v_txid.get() + '.ini')
        except:
            pass
        # 再刷新一次entry的状态
        self.check()


        
    # 主函数
    def main(self):
        pass
        



root = Tk()  # 创建Tk对象，Tk代表窗口
root.title('Raspberrypi Remote Diagnostics - CAN FD')  # 设置窗口标题
root.option_add("*Font", ('Arial', 11))  # 设置全局字体，这样就不用每个控件单独指定字体

w = 960
h = 640

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
