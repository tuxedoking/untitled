from tkinter import *
from tkinter import ttk
from stockselect.util import get_work_area
import datetime

wa_pos = get_work_area()
if wa_pos is None:
    exit(0)

root = Tk()
root.geometry(f'450x800+{wa_pos[0]}+{wa_pos[1]}')
root.title('selector')

content = ttk.Frame(root)
frame = ttk.Frame(content)

reload_button = ttk.Button(frame, text="重新载入")
left_button = ttk.Button(frame, text="<", width=1)
adjust_position_button = ttk.Button(frame, text="调整位置")
right_button = ttk.Button(frame, text=">", width=1)
from_label = ttk.Label(frame, text="开始")
from_date = StringVar()
from_date.set((datetime.datetime.today()-datetime.timedelta(100)).strftime('%Y/%m/%d'))
from_entry = ttk.Entry(frame, width=10, textvariable=from_date)
to_label = ttk.Label(frame, text="结束")
to_date = StringVar()
to_date.set(datetime.datetime.today().strftime('%Y/%m/%d'))
to_entry = ttk.Entry(frame, width=10, textvariable=to_date)


frame2 = ttk.Frame(content)


content.grid(column=0, row=0, sticky=(N, S, E, W))
frame.grid(column=0, row=0, columnspan=8, rowspan=1, sticky=(N, S, E, W))
frame2.grid(column=0, row=1, sticky=(N, S, E, W))
reload_button.grid(column=0, row=0)
left_button.grid(column=1, row=0)
adjust_position_button.grid(column=2, row=0)
right_button.grid(column=3, row=0)
from_label.grid(column=4, row=0)
from_entry.grid(column=5, row=0)
to_label.grid(column=6, row=0)
to_entry.grid(column=7, row=0)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

content.columnconfigure(0, weight=1)
content.rowconfigure(0, weight=0)
content.rowconfigure(1, weight=1)

# frame.rowconfigure(0, weight=1)
# frame.rowconfigure(1, weight=1)

notebook = ttk.Notebook(frame2)
f1 = ttk.Frame(notebook)   # first page, which would get widgets gridded into it
f2 = ttk.Frame(notebook)   # second page

columns = ("name", "tel", "email", "company")
headers = ("姓名", "电话", "邮箱", "公司")
widthes = (80, 80, 150, 150)
tv = ttk.Treeview(f1, show='headings', columns=columns)


def test():
    print(tv.identify_column(root.winfo_pointerx()-root.winfo_rootx()))
    print(tv.get_children())
    for item in tv.get_children():
        print(tv.item(item))


for (column, header, width) in zip(columns, headers, widthes):
    tv.column(column, width=width, anchor="w")
    tv.heading(column, text=header, anchor="w", command=test)

contacts =[
    ('张三', '1870591xxxx', 'zhang@qq.com', '腾讯'),
    ('李斯', '1589928xxxx', 'lisi@google.com', '谷歌'),
    ('王武', '1340752xxxx', 'wangwu@baidu.com', '微软'),
    ('麻溜儿', '1361601xxxx', 'maliur@alibaba.com', '阿里'),
    ('郑和', '1899986xxxx', 'zhenghe@163.com', '网易'),
]
for i, person in enumerate(contacts):
    tv.insert('', i, values=person)


notebook.add(f1, text='创新高')
notebook.add(f2, text='周线多头排列')
notebook.grid(column=0, row=0, sticky=(N, S, E, W))

tv.grid(column=0, row=0, sticky=(N, S, E, W))

f1.columnconfigure(0, weight=1)
f1.rowconfigure(0, weight=1)

frame2.columnconfigure(0, weight=1)
frame2.rowconfigure(0, weight=1)


# frame = ttk.Frame(content, borderwidth=5, relief="ridge", width=200, height=100)
# namelbl = ttk.Label(content, text="Name")
# name = ttk.Entry(content)
#
# onevar = BooleanVar()
# twovar = BooleanVar()
# threevar = BooleanVar()
#
# onevar.set(True)
# twovar.set(False)
# threevar.set(True)
#
# one = ttk.Checkbutton(content, text="One", variable=onevar, onvalue=True)
# two = ttk.Checkbutton(content, text="Two", variable=twovar, onvalue=True)
# three = ttk.Checkbutton(content, text="Three", variable=threevar, onvalue=True)
# ok = ttk.Button(content, text="Okay")
# cancel = ttk.Button(content, text="Cancel")
#
# content.grid(column=0, row=0, sticky=(N, S, E, W))
# frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
# namelbl.grid(column=3, row=0, columnspan=2, sticky=(N, W), padx=5)
# name.grid(column=3, row=1, columnspan=2, sticky=(N,E,W), pady=5, padx=5)
# one.grid(column=0, row=3)
# two.grid(column=1, row=3)
# three.grid(column=2, row=3)
# ok.grid(column=3, row=3)
# cancel.grid(column=4, row=3)
#
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)
# content.columnconfigure(0, weight=3)
# content.columnconfigure(1, weight=3)
# content.columnconfigure(2, weight=3)
# content.columnconfigure(3, weight=1)
# content.columnconfigure(4, weight=1)
# content.rowconfigure(1, weight=1)

root.mainloop()
