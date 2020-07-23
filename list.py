"""
此文件提供选中各个模块后显示不同的列表，提供给main模块的接口主要是list.main()函数
传入列名称元组和当前所处模块名字，就能得到不同的列表显示在GUI上
"""

from tkinter import ttk
from tkinter import *
from tkinter import simpledialog
import main as main_module
import database

def main(columns, names):
    global root,treeview,newb,content,db,return_to_last,deleteb,searchb
    db = database.DataBase(names) # 初始化数据库，连接数据库并得到对应table的数据
    content = db.Search() # 内容

    root = Tk()  # 初始框的声明
    treeview = ttk.Treeview(root, height=18, show="headings", columns=columns)  # 表格
    root.title(names)

    geometry = ""
    if names == "库存基本数据":
        geometry = "700x700+250+50"

    elif names == "入库管理":
        geometry = "800x700+250+50"

    elif names == "出库管理":
        geometry = "800x700+250+50"

    elif names == "盘点管理":
        geometry = "1100x700+250+50"

    root.geometry(geometry)

    for strs in columns:
        treeview.column(strs, width=100, anchor='center')
        treeview.heading(strs, text=strs)

    treeview.pack(side=LEFT, fill=BOTH)
    treeview.bind('<Double-1>', set_cell_value)
    # 新建按钮初始化
    newb = ttk.Button(root, text='新建条目', width=15, command=lambda: newrow(names))
    newb.place(x=30, y=(len(content) - 1) * 20 + 45)

    # 删除按钮初始化
    deleteb = ttk.Button(root, text="删除", width=15, command=delete)
    deleteb.place(x=160, y=(len(content) - 1) * 20 + 45)
    # 查询按钮初始化
    searchb = ttk.Button(root, text="查询", width=15, command=search)
    searchb.place(x=300, y=(len(content) - 1) * 20 + 45)

    # 返回按钮初始化
    return_to_last = ttk.Button(root, text='返回', width=15, command=lambda: main_module.create_frame1("return_back"))
    return_to_last.place(x=460, y=(len(content) - 1) * 20 + 45)

    # 从数据库得到数据并插入到GUI中的列表里
    for i in range(len(content)):
        treeview.insert('', i, values=content[i])

    for col in columns:  # 绑定函数，使表头可排序 , command=lambda _col=col: treeview_sort_column(treeview, _col, False)
        treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeview, _col, False))
    root.mainloop()  # 进入消息循环


def treeview_sort_column(tv, col, reverse):  # Treeview、列名、排列方式
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)  # 排序方式
    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):  # 根据排序后索引移动
        tv.move(k, '', index)
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

def search():
    sql = simpledialog.askstring("查找", "请输入SQL语句")

    content =  db.Search(sql)
    for ii in treeview.get_children():
        treeview.delete(ii)

    for i in range(len(content)):
        treeview.insert('', i, iid="I00{0}".format(i + 1), values=content[i])
    newb.place(x=30, y=(len(content) - 1) * 20 + 45)
    return_to_last.place(x=460, y=(len(content) - 1) * 20 + 45)
    deleteb.place(x=160, y=(len(content) - 1) * 20 + 45)
    searchb.place(x=300, y=(len(content) - 1) * 20 + 45)


    treeview.update()

def delete():
    item = treeview.selection()
    if not item:
        return
    item_text = treeview.item(item, "values")
    id = item_text[0]

    for ii in treeview.get_children():
        treeview.delete(ii)

    db.Delete(id)

    content = db.Search()
    newb.place(x=30, y=(len(content) - 1) * 20 + 45)
    return_to_last.place(x=460, y=(len(content) - 1) * 20 + 45)
    deleteb.place(x=160, y=(len(content) - 1) * 20 + 45)
    searchb.place(x=300, y=(len(content) - 1) * 20 + 45)

    for i in range(len(content)):
        treeview.insert('', i,iid="I00{0}".format(i+1) , values=content[i])

    treeview.update()

def set_cell_value(event):  # 双击进入编辑状态
    for item in treeview.selection():
        # item = I001
        item_text = treeview.item(item, "values")
        id = item_text[0]
        # print(item_text[0:2])  # 输出所选行的值
    column = treeview.identify_column(event.x)  # 列
    row = treeview.identify_row(event.y)  # 行
    cn = int(str(column).replace('#', ''))
    rn = int(str(row).replace('I', ''))
    entryedit = Text(root, width=10, height=1)
    entryedit.place(x=16 + (cn - 1) * 100, y=6 + rn * 20)

    def saveedit():
        field = treeview.column(column)['id']
        treeview.set(item, column=column, value=entryedit.get(0.0, "end"))
        # 修改后插入数据库
        # print(str(id),str(field),entryedit.get(0.0, "end"))
        db.Change(id,field,entryedit.get(0.0, "end").strip())

        entryedit.destroy()
        okb.destroy()

    okb = ttk.Button(root, text='OK', width=4, command=saveedit)
    okb.place(x=90 + (cn - 1) * 100, y=2 + rn * 20)

# 新建条目，我准备插入None，然后在修改条目那里再做文章
def newrow(names):
    # 增加一行，写入数据库
    # 根据不同的table，新增的条目初始化的类型是不同的
    global content

    def updata_list(temp):
        db.Add(temp)
        content = db.Search()
        for ii in treeview.get_children():
            treeview.delete(ii)

        for i in range(len(content)):
            treeview.insert('', i, iid="I00{0}".format(i + 1), values=content[i])
        newb.place(x=30, y=(len(content) - 1) * 20 + 45)
        return_to_last.place(x=460, y=(len(content) - 1) * 20 + 45)
        deleteb.place(x=160, y=(len(content) - 1) * 20 + 45)
        searchb.place(x=300, y=(len(content) - 1) * 20 + 45)
        treeview.update()

    if names == "库存基本数据":
        temp = (0,0, 0, 0, 0, 0, 0)
        updata_list(temp)
    elif names == "入库管理":
        temp = (0,0, 0,0, 0, 0, 0, 0)
        updata_list(temp)
    elif names == "出库管理":
        temp = (0,0, 0, 0, 0, 0, 0, 0)
        updata_list(temp)
    elif names == "盘点管理":
        temp = (0,0, 0,0, 0, 0, 0, 0, 0, 0, 0)
        updata_list(temp)

if __name__ == '__main__':
    pass

'''
1.遍历表格
t = treeview.get_children()
for i in t:
    print(treeview.item(i,'values'))
2.绑定单击离开事件
def treeviewClick(event):  # 单击
    for item in tree.selection():
        item_text = tree.item(item, "values")
        print(item_text[0:2])  # 输出所选行的第一列的值
tree.bind('<ButtonRelease-1>', treeviewClick)  
------------------------------
鼠标左键单击按下1/Button-1/ButtonPress-1 
鼠标左键单击松开ButtonRelease-1 
鼠标右键单击3 
鼠标左键双击Double-1/Double-Button-1 
鼠标右键双击Double-3 
鼠标滚轮单击2 
鼠标滚轮双击Double-2 
鼠标移动B1-Motion 
鼠标移动到区域Enter 
鼠标离开区域Leave 
获得键盘焦点FocusIn 
失去键盘焦点FocusOut 
键盘事件Key 
回车键Return 
控件尺寸变Configure
------------------------------
'''



