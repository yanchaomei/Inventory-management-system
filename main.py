from tkinter import *
from tkinter import messagebox
import list
from tkinter.ttk import *

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)  # super()代表父类的定义 不是父类对象
        self.master = master
        self.pack()
        self.createWidget()

    def createWidget(self):
        self.label1 = Label(self, text="药品库存管理信息系统")
        self.label1.grid(row=0, column=1)
        # 创建用户名输入框
        self.label2 = Label(self, text="用户名")
        self.label2.grid(row=1, column=0)

        v1 = StringVar()
        self.entry1 = Entry(self, textvariable=v1)
        self.entry1.grid(row=1, column=1)


        # 创建密码输入框
        self.label3 = Label(self, text="密码")
        self.label3.grid(row=2, column=0)

        v2 = StringVar()
        self.entry2 = Entry(self, textvariable=v2)
        self.entry2.grid(row=2, column=1)

        #  创建登录按钮
        self.btn1 = Button(self,text="登录", command=self.login)
        self.btn1.grid(row=5, column=1)

        # 创建一个退出按钮
        self.btn_Quit = Button(self, text="退出", command=root.destroy)
        self.btn_Quit.grid(row=5, column=2)

    def login(self):
        username = self.entry1.get()
        password = self.entry2.get()

        if username == "" and password == "":
            create_frame1()

        else:
            messagebox.showinfo("sorry", "登录失败")


def create_frame1(p=None):
    global root1
    root1 = Tk()
    if p == "return_back":
        list.root.destroy()
    else:
        root.destroy()
    root1.geometry("1000x700+250+50")
    root1.title("药品库存管理信息系统")
    btnText = ("库存基本数据管理","入库管理","出库管理","盘点管理")
    funclist = (frame1_button1, frame1_button2, frame1_button3, frame1_button4)
    i = 0
    for text in btnText:
        Button(root1, text=text, command=funclist[i]).pack(side="left", padx="10",anchor="n")
        i = i + 1
    Button(root1, text="退回登录界面", command=return_to_main_frame).pack(side="left", padx="10",anchor="n")
    root1.mainloop()

def frame1_button1():
    root1.destroy()
    columns = ("id","仓库大小", "货架数量", "货架规格", "推车数量", "推车规格", "库工人数")
    name = "库存基本数据"
    list.main(columns, name)

def frame1_button2():
    root1.destroy()
    columns = ("id","产品代码", "名称", "入库数量", "单位", "日期", "操作者", "存货货位")
    name = "入库管理"
    list.main(columns, name)

def frame1_button3():
    root1.destroy()
    columns = ("id","产品代码", "名称", "出库数量", "单位", "日期", "操作者", "出货货位")
    name = "出库管理"
    list.main(columns, name)

def frame1_button4():
    root1.destroy()
    columns = ("id","产品代码", "名称", "出库数量", "单位 ", "入库数量", "单位", "结余", "空余货位", "日期", "操作者")
    name = "盘点管理"
    list.main(columns, name)

def return_to_main_frame():
    root1.destroy()
    main_frame()

def main_frame():
    global root
    # 主窗口对象 root
    root = Tk()
    # 通过geometry方法确定窗口在屏幕中的位置以及窗口的大小
    root.geometry("500x200+500+100")
    root.title("药品库存管理信息系统")
    app = Application(master=root)
    # 进入事件主循环 等待响应
    root.mainloop()


if __name__ == "__main__":
    main_frame()



