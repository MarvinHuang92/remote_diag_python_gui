from tkinter import *
from tkinter.ttk import *
import threading
import time
import sys
import queue
 
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
 
class GUI():
 
    def __init__(self, root):
 
        #new 一个Quue用于保存输出内容
        self.msg_queue = queue.Queue()
        self.initGUI(root)
 
    #在show_msg方法里，从Queue取出元素，输出到Text
    def show_msg(self):
 
        while not self.msg_queue.empty():
            content = self.msg_queue.get()
            self.text.insert(INSERT, content)
            self.text.see(END)
 
        #after方法再次调用show_msg
        self.root.after(100, self.show_msg)
 
    def initGUI(self, root):
 
        self.root = root
        self.root.title("test")
        self.root.geometry("400x200+700+500")
        self.root.resizable = False
 
        self.button = Button(self.root, text="click", width=10, command=self.show)
        self.button.pack(side="top")
 
        self.scrollBar = Scrollbar(self.root)
        self.scrollBar.pack(side="right", fill="y")
 
        self.text = Text(self.root, height=10, width=45, yscrollcommand=self.scrollBar.set)
        self.text.pack(side="top", fill=BOTH, padx=10, pady=10)
        self.scrollBar.config(command=self.text.yview)
 
        #启动after方法
        self.root.after(100, self.show_msg)
 
        #将stdout映射到re_Text
        sys.stdout = re_Text(self.msg_queue)
 
        root.mainloop()
 
    def __show(self):
 
        i = 0
        while i < 3:
            print(fmtTime(time.time()))
            time.sleep(1)
            i += 1
 
    def show(self):
        T = threading.Thread(target=self.__show, args=())
        T.start()
 
if __name__ == "__main__":
 
    root = Tk()
    myGUI = GUI(root)