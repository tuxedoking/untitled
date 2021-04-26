from tkinter import *
from tkinter import ttk
from stockselect.util import get_work_area
from stockselect.util import find_ths_wnd
import datetime
import win32con
import win32gui
from stockselect import util
from stockselect.selector import selector
from stockselect.chuang_xin_gao import chuang_xin_gao
from stockselect.zhang_ting import zhang_ting
from stockselect.ri_xian_duo_tou_pai_lie import ri_xian_duo_tou_pai_lie
from stockselect.zhou_xian_duo_tou_pai_lie import zhou_xian_duo_tou_pai_lie
from stockselect.yue_xian_duo_tou_pai_lie import yue_xian_duo_tou_pai_lie
from stockselect.up_down import up_down
from stockselect.yue_xian_lian_yang import yue_xian_lian_yang


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

        self.reload_button = ttk.Button(self.frame, text="重新载入", width=7)
        self.left_button = ttk.Button(self.frame, text="<", width=1, command=self.on_adjust_left)
        self.adjust_position_button = ttk.Button(self.frame, text="调整位置", width=7, command=self.on_adjust_position_button)
        self.right_button = ttk.Button(self.frame, text=">", width=1, command=self.on_adjust_right)
        self.from_label = ttk.Label(self.frame, text="开始(日)")
        self.from_date = StringVar()
        self.from_entry = ttk.Entry(self.frame, width=8, textvariable=self.from_date)
        self.from_date.set((datetime.datetime.today() - datetime.timedelta(100)).strftime('%Y%m%d'))
        self.from_label_week = ttk.Label(self.frame, text="开始(周)")
        self.from_date_week = StringVar()
        self.from_date_week_entry = ttk.Entry(self.frame, width=8, textvariable=self.from_date_week)
        self.from_date_week.set((datetime.datetime.today() - datetime.timedelta(300)).strftime('%Y%m%d'))
        self.from_label_month = ttk.Label(self.frame, text="开始(月)")
        self.from_date_month = StringVar()
        self.from_date_month_entry = ttk.Entry(self.frame, width=8, textvariable=self.from_date_month)
        self.from_date_month.set((datetime.datetime.today() - datetime.timedelta(500)).strftime('%Y%m%d'))

        self.frame2 = ttk.Frame(self.content)

        self.content.grid(column=0, row=0, sticky=(N, S, E, W))
        self.frame.grid(column=0, row=0, columnspan=10, rowspan=1, sticky=(N, S, E, W))
        self.frame2.grid(column=0, row=1, sticky=(N, S, E, W))
        self.reload_button.grid(column=0, row=0)
        self.left_button.grid(column=1, row=0)
        self.adjust_position_button.grid(column=2, row=0)
        self.right_button.grid(column=3, row=0)
        self.from_label.grid(column=4, row=0)
        self.from_entry.grid(column=5, row=0)
        self.from_label_week.grid(column=6, row=0)
        self.from_date_week_entry.grid(column=7, row=0)
        self.from_label_month.grid(column=8, row=0)
        self.from_date_month_entry.grid(column=9, row=0)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=0)
        self.content.rowconfigure(1, weight=1)

        self.notebook = ttk.Notebook(self.frame2)

        self.f1 = ttk.Frame(self.notebook)  # first page, which would get widgets gridded into it
        self.f2 = ttk.Frame(self.notebook)  # second page
        self.f3 = ttk.Frame(self.notebook)  # second page
        self.f4 = ttk.Frame(self.notebook)
        self.f5 = ttk.Frame(self.notebook)
        self.f6 = ttk.Frame(self.notebook)
        self.f7 = ttk.Frame(self.notebook)

        self.notebook.add(self.f1, text='涨停')
        self.notebook.add(self.f2, text='创新高')
        self.notebook.add(self.f3, text='日线多头排列')
        self.notebook.add(self.f4, text='周线多头排列')
        self.notebook.add(self.f5, text='月线多头排列')
        self.notebook.add(self.f6, text='月线连阳')
        self.notebook.add(self.f7, text='上涨回调')

        self.notebook.grid(column=0, row=0, sticky=(N, S, E, W))

        # self.add_tree_view_notebook(self.f1)

        self.f1.columnconfigure(0, weight=1)
        self.f1.rowconfigure(0, weight=1)

        self.f2.columnconfigure(0, weight=1)
        self.f2.rowconfigure(0, weight=1)

        self.f3.columnconfigure(0, weight=1)
        self.f3.rowconfigure(0, weight=1)

        self.f4.columnconfigure(0, weight=1)
        self.f4.rowconfigure(0, weight=1)

        self.f5.columnconfigure(0, weight=1)
        self.f5.rowconfigure(0, weight=1)

        self.f6.columnconfigure(0, weight=1)
        self.f6.rowconfigure(0, weight=1)

        self.f7.columnconfigure(0, weight=1)
        self.f7.rowconfigure(0, weight=1)

        self.frame2.columnconfigure(0, weight=1)
        self.frame2.rowconfigure(0, weight=1)

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

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
        l = [(tv.item(item)['values'][column_index], item) for item in tv.get_children('')]
        l.sort(key=lambda s: self.columns[column_index][4](s[0]), reverse=self.columns[column_index][3])
        # print(l)
        # l.sort(key=lambda s: s[0][4](s[0]), reverse=self.columns[column_index][3])
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
            self.columns = [['date', '日期', 60, False, str], ['code', '代码', 60, False, str],
                            ['name', '名称', 80, False, str], ['count', '连续天数', 60, False, int]]
            self.create_tv(frame)
            haha = zhang_ting()
            results = haha.select(start_date=self.from_date.get())
            if results is None:
                return
            for i, result in enumerate(results):
                self.tv.insert('', i, values=result)
        elif index == 1:
            self.columns = [['date', '日期', 60, False, str], ['code', '代码', 60, False, str], ['name', '名称', 80, False, str],
                            ['count', '天数', 60, False, int]]
            self.create_tv(frame)

            haha = chuang_xin_gao()
            results = haha.select(start_date=self.from_date.get())
            # results = cxg.select(start_date='20210101')
            if results is None:
                return
            for i, result in enumerate(results):
                self.tv.insert('', i, values=result)
        elif index == 2:
            self.columns = [['date', '日期', 50, False, str], ['code', '代码', 50, False, str],
                            ['name', '名称', 60, False, str], ['count', '天数', 50, False, int],
                            ['fu_du', '幅度', 50, False, float]]
            self.create_tv(frame)

            haha = ri_xian_duo_tou_pai_lie()
            results = haha.select(start_date=self.from_date.get())
            if results is None:
                return
            for i, result in enumerate(results):
                self.tv.insert('', i, values=result)
        elif index == 3:
            self.columns = [['date', '日期', 50, False, str], ['code', '代码', 50, False, str],
                            ['name', '名称', 60, False, str], ['count', '周数', 50, False, int],
                            ['fu_du', '幅度', 50, False, float]]
            self.create_tv(frame)

            haha = zhou_xian_duo_tou_pai_lie()
            results = haha.select(start_date=self.from_date_week.get())
            if results is None:
                return
            for i, result in enumerate(results):
                self.tv.insert('', i, values=result)
        elif index == 4:
            self.columns = [['date', '日期', 50, False, str], ['code', '代码', 50, False, str],
                            ['name', '名称', 60, False, str], ['count', '月数', 50, False, int],
                            ['fu_du', '幅度', 50, False, float]]
            self.create_tv(frame)

            haha = yue_xian_duo_tou_pai_lie()
            results = haha.select(start_date=self.from_date_month.get())
            if results is None:
                return
            for i, result in enumerate(results):
                self.tv.insert('', i, values=result)
        elif index == 5:
            self.columns = [['date', '日期', 50, False, str], ['code', '代码', 50, False, str],
                            ['name', '名称', 60, False, str], ['fu_du', '幅度', 50, False, float],
                            ['count', '连阳月数', 50, False, int]]

            self.create_tv(frame)

            haha = yue_xian_lian_yang()
            results = haha.select(start_date=self.from_date_month.get())
            if results is None:
                return
            for i, result in enumerate(results):
                self.tv.insert('', i, values=result)
        elif index == 6:
            self.columns = [['date', '日期', 50, False, str], ['code', '代码', 50, False, str],
                            ['name', '名称', 60, False, str], ['fu_du', '上涨幅度', 50, False, float],
                            ['fu_du2', '回调幅度', 50, False, float]]
            self.create_tv(frame)

            haha = up_down()
            results = haha.select(start_date=self.from_date_month.get())
            if results is None:
                return
            for i, result in enumerate(results):
                self.tv.insert('', i, values=result)

    def create_tv(self, frame):
        self.tv = ttk.Treeview(frame, show='headings', columns=[x[0] for x in self.columns])

        for (column, header, width, reverse, sort_type) in self.columns:
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


    # def add_tree_view_notebook(self, frame, tab_index=0):
    #     if tab_index == 0:
    #         columns = ('date', 'code', 'name', 'count')
    #         headers = ('日期', '代码', '名称', '天数')
    #         widths = (80, 60, 80, 60)
    #     self.tv = ttk.Treeview(frame, show='headings', columns=columns)
    #
    #     def test():
    #         print(self.tv.identify_column(self.root.winfo_pointerx() - self.root.winfo_rootx()))
    #         print(self.tv.get_children())
    #         for item in self.tv.get_children():
    #             print(self.tv.item(item))
    #
    #     for (column, header, width) in zip(columns, headers, widths):
    #         self.tv.column(column, width=width, anchor="w")
    #         self.tv.heading(column, text=header, anchor="w", command=test
    #
    #     self.tv.grid(column=0, row=0, sticky=(N, S, E, W))