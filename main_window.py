from tkinter import *
from tkinter import ttk
from stockselect.util import get_work_area
from stockselect.util import find_ths_wnd
import datetime
import win32con
import win32gui
from stockselect import util
from stockselect.chuang_xin_gao import chuang_xin_gao
from stockselect.zhang_ting import zhang_ting
from stockselect.ri_xian_duo_tou_pai_lie import ri_xian_duo_tou_pai_lie
from stockselect.selector import selector


class main_window:
    def __init__(self):
        self.tv = None
        self.vbar = None
        self.m_pos = 0
        self.columns = None

        wa_pos = get_work_area()
        if wa_pos is None:
            exit(0)

        self.root = Tk()
        self.root.geometry(f'450x800+{wa_pos[0]}+{wa_pos[1]}')
        self.root.title('selector')

        self.content = ttk.Frame(self.root)
        self.frame = ttk.Frame(self.content)

        self.reload_button = ttk.Button(self.frame, text="重新载入")
        self.left_button = ttk.Button(self.frame, text="<", width=1, command=self.on_adjust_left)
        self.adjust_position_button = ttk.Button(self.frame, text="调整位置", command=self.on_adjust_position_button)
        self.right_button = ttk.Button(self.frame, text=">", width=1, command=self.on_adjust_right)
        self.from_label = ttk.Label(self.frame, text="开始")
        self.from_date = StringVar()
        self.from_entry = ttk.Entry(self.frame, width=10, textvariable=self.from_date)
        self.from_date.set((datetime.datetime.today() - datetime.timedelta(100)).strftime('%Y%m%d'))
        self.to_label = ttk.Label(self.frame, text="结束")
        self.to_date = StringVar()
        self.to_entry = ttk.Entry(self.frame, width=10, textvariable=self.to_date)
        self.to_date.set(datetime.datetime.today().strftime('%Y%m%d'))

        self.frame2 = ttk.Frame(self.content)

        self.content.grid(column=0, row=0, sticky=(N, S, E, W))
        self.frame.grid(column=0, row=0, columnspan=8, rowspan=1, sticky=(N, S, E, W))
        self.frame2.grid(column=0, row=1, sticky=(N, S, E, W))
        self.reload_button.grid(column=0, row=0)
        self.left_button.grid(column=1, row=0)
        self.adjust_position_button.grid(column=2, row=0)
        self.right_button.grid(column=3, row=0)
        self.from_label.grid(column=4, row=0)
        self.from_entry.grid(column=5, row=0)
        self.to_label.grid(column=6, row=0)
        self.to_entry.grid(column=7, row=0)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=0)
        self.content.rowconfigure(1, weight=1)

        # frame.rowconfigure(0, weight=1)
        # frame.rowconfigure(1, weight=1)

        self.notebook = ttk.Notebook(self.frame2)

        self.f1 = ttk.Frame(self.notebook)  # first page, which would get widgets gridded into it
        self.f2 = ttk.Frame(self.notebook)  # second page
        self.f3 = ttk.Frame(self.notebook)  # second page

        self.notebook.add(self.f1, text='涨停')
        self.notebook.add(self.f2, text='创新高')
        self.notebook.add(self.f3, text='日线多头排列')

        self.notebook.grid(column=0, row=0, sticky=(N, S, E, W))

        # self.add_tree_view_notebook(self.f1)

        self.f1.columnconfigure(0, weight=1)
        self.f1.rowconfigure(0, weight=1)

        self.f2.columnconfigure(0, weight=1)
        self.f2.rowconfigure(0, weight=1)

        self.f3.columnconfigure(0, weight=1)
        self.f3.rowconfigure(0, weight=1)

        self.frame2.columnconfigure(0, weight=1)
        self.frame2.rowconfigure(0, weight=1)

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def add_tree_view_notebook(self, frame, tab_index=0):
        if tab_index == 0:
            columns = ('date', 'code', 'name', 'count')
            headers = ('日期', '代码', '名称', '天数')
            widths = (80, 60, 80, 60)
        self.tv = ttk.Treeview(frame, show='headings', columns=columns)

        def test():
            print(self.tv.identify_column(self.root.winfo_pointerx() - self.root.winfo_rootx()))
            print(self.tv.get_children())
            for item in self.tv.get_children():
                print(self.tv.item(item))

        for (column, header, width) in zip(columns, headers, widths):
            self.tv.column(column, width=width, anchor="w")
            self.tv.heading(column, text=header, anchor="w", command=test)

        # contacts = [
        #     ('张三', '1870591xxxx', 'zhang@qq.com', '腾讯'),
        #     ('李斯', '1589928xxxx', 'lisi@google.com', '谷歌'),
        #     ('王武', '1340752xxxx', 'wangwu@baidu.com', '微软'),
        #     ('麻溜儿', '1361601xxxx', 'maliur@alibaba.com', '阿里'),
        #     ('郑和', '1899986xxxx', 'zhenghe@163.com', '网易'),
        # ]
        # for i, person in enumerate(contacts):
        #     self.tv.insert('', i, values=person)

        self.tv.grid(column=0, row=0, sticky=(N, S, E, W))

    def adjust_window(self):
        wa_pos2 = get_work_area()
        width = int((wa_pos2[2] - wa_pos2[0]) * self.m_pos / 24)
        self.root.geometry(f'{width}x{wa_pos2[3] - wa_pos2[1]}+{wa_pos2[0]}+{wa_pos2[1]}')
        hwnd = find_ths_wnd()
        if not hwnd:
            return
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
        win32gui.SetWindowPos(hwnd, None, wa_pos2[0] + self.root.winfo_width(), wa_pos2[1],
                              wa_pos2[2] - wa_pos2[0] - self.root.winfo_width(),
                              wa_pos2[3] - wa_pos2[1], win32con.SWP_SHOWWINDOW)

    def on_adjust_position_button(self):
        self.m_pos = 7
        self.adjust_window()

    def on_adjust_left(self):
        if self.m_pos > 7:
            self.m_pos -= 1
        self.adjust_window()

    def on_adjust_right(self):
        if self.m_pos < 15:
            self.m_pos += 1
        self.adjust_window()

    def tb(self, event):
        tree = event.widget
        d = tree.item(tree.selection())
        code = d['values'][1][0:6]
        hwnd = find_ths_wnd()
        if not hwnd:
            return
        util.press_code_on_ths(hwnd, code)

        # for item in tree.selection():
        #    print(item, ' =>', tree.item(item))

    def tv_sort_column(self):
        tv = self.tv
        column_index = int(tv.identify_column(self.root.winfo_pointerx() - self.root.winfo_rootx())[1:])-1
        l = [(tv.item(item)['values'], item) for item in tv.get_children('')]
        l.sort(key=lambda s: s[0][column_index], reverse=self.columns[column_index][3])
        self.columns[column_index][3] = not self.columns[column_index][3]
        # print(l)
        for i, (val, k) in enumerate(l):
            tv.move(k, '', i)
        # tv.heading(self.columns[column_index][0], text=self.columns[column_index][1], anchor="w",
        #           command=self.tv_sort_column)

    def on_tab_changed(self, event):
        print(event.widget)
        tab_id = event.widget.select()
        index = event.widget.index(tab_id)
        print(index)
        frame = event.widget.children[tab_id.split(".")[len(tab_id.split(".")) - 1]]
        if self.tv is not None:
            self.tv.destroy()
        if self.vbar is not None:
            self.vbar.destroy()
        # self.add_tree_view_notebook(frame)
        if index == 0:
            self.columns = [['date', '日期', 60, False], ['code', '代码', 60, False], ['name', '名称', 80, False],
                            ['count', '连续天数', 60, False]]
            self.create_tv(frame)
            haha = zhang_ting()
            results = haha.select(start_date=self.from_date.get())
            if results is None:
                return
            for i, result in enumerate(results):
                self.tv.insert('', i, values=result)
        elif index == 1:
            self.columns = [['date', '日期', 60, False], ['code', '代码', 60, False], ['name', '名称', 80, False],
                            ['count', '天数', 60, False]]
            self.create_tv(frame)

            haha = chuang_xin_gao()
            results = haha.select(start_date=self.from_date.get())
            # results = cxg.select(start_date='20210101')
            if results is None:
                return
            for i, result in enumerate(results):
                self.tv.insert('', i, values=result)
        elif index == 2:
            self.columns = [['date', '日期', 50, False], ['code', '代码', 50, False], ['name', '名称', 60, False],
                            ['count', '天数', 50, False], ['count', '幅度', 50, False]]
            self.create_tv(frame)

            haha = ri_xian_duo_tou_pai_lie()
            results = haha.select(start_date=self.from_date.get())
            # results = cxg.select(start_date='20210101')
            if results is None:
                return
            for i, result in enumerate(results):
                self.tv.insert('', i, values=result)

    def create_tv(self, frame):
        self.tv = ttk.Treeview(frame, show='headings', columns=[x[0] for x in self.columns])

        for (column, header, width, reverse) in self.columns:
            self.tv.column(column, width=width, anchor="w")
            self.tv.heading(column, text=header, anchor="w",
                            command=self.tv_sort_column)

        self.tv.bind('<<TreeviewSelect>>', self.tb)
        self.tv.grid(column=0, row=0, sticky=(N, S, E, W))

        self.vbar = ttk.Scrollbar(frame, orient=VERTICAL, command=self.tv.yview)
        self.tv.configure(yscrollcommand=self.vbar.set)
        self.vbar.grid(row=0, column=1, sticky=(N, S, E))

    def main_loop(self):
        self.root.mainloop()


if __name__ == '__main__':
    selector.init_dbs()
    mw = main_window()
    mw.main_loop()
    selector.close_dbs()
