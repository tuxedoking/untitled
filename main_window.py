from tkinter import *
from tkinter import ttk
from stockselect.util import get_work_area

wapos = get_work_area()
if wapos is None:
    exit(0)

root = Tk()
root.geometry(f'450x800+{wapos[0]}+{wapos[1]}')
root.title('selector')

content = ttk.Frame(root)
frame = ttk.Frame(content)

reload_button = ttk.Button(frame, text="重新载入")
left_button = ttk.Button(frame, text="<", width=1)
adjust_position_button = ttk.Button(frame, text="调整位置")
right_button = ttk.Button(frame, text=">", width=1)
from_label = ttk.Label(frame, text="开始")
from_entry = ttk.Entry(frame, width=10)
to_label = ttk.Label(frame, text="结束")
to_entry = ttk.Entry(frame, width=10)

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
#
# frame.rowconfigure(0, weight=1)
# frame.rowconfigure(1, weight=1)

notebook = ttk.Notebook(frame2)
f1 = ttk.Frame(notebook)   # first page, which would get widgets gridded into it
f2 = ttk.Frame(notebook)   # second page
notebook.add(f1, text='One')
notebook.add(f2, text='Two')
notebook.grid(column=0, row=0, sticky=(N, S, E, W))

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
