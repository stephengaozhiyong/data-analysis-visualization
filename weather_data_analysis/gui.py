import os
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import askokcancel, showinfo
from prepare_data import PreResolver
from process_table1 import ProcesserTable1
from process_table2 import ProcesserTable2
from plot import MyPlot

class Quitter:
    def __init__(self) -> None:
        self.top = tk.Frame()
        self.top.pack()
        widget = tk.Button(self.top, text="Quit", command=self.quit)
        widget.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
    
    def quit(self):
        # ans = askokcancel("Verify exit", "Really quit?")
        if True:
            self.top.quit()

class RowFile:
    def __init__(self, parent=None, label="", butt=""):
        self.butt = butt
        self.label = label
        self.top = tk.Frame(parent)
        self.top.pack(side=tk.TOP, fill=tk.X)
        self.path = tk.StringVar()
        self.make_widgets()
        
    def _select_path(self):
        path_ = askopenfilename()
        self.path.set(path_)

    def _select_dir_path(self):
        _path = askdirectory()
        self.path.set(_path)

    def make_widgets(self):
        tk.Label(self.top, text=self.label, width=20).pack(side=tk.LEFT)
        tk.Entry(self.top, textvariable=self.path).pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
        tk.Button(self.top, text=self.butt, command=self._select_path).pack(side=tk.RIGHT)

class RowDir(RowFile):
    def __init__(self, parent=None, label="", butt=""):
        super().__init__(parent, label, butt)
    
    def _select_path(self):
        _path = askdirectory()
        self.path.set(_path)


class Window:
    def __init__(self, title="Weather Data Analizer") -> None:
        self.root = tk.Tk()
        self.root.title = title
        self.row_src = RowFile(self.root, label="origin data path:", butt="select file path")
        self.row_dst = RowDir(self.root, label="dest path:", butt="select dir path")
        self.make_widgets()

    def check_rows(self, src, dst):
        src_ext = os.path.exists(src)
        dst_ext = os.path.exists(dst)
        src_info = "src path:{}, exists?: {}".format(src, src_ext)
        dst_info = "dst path:{}, exists?: {}".format(dst, dst_ext)
        if not src_ext or not dst_ext:
            showinfo("path not valid!!!", "{}\n{}".format(src_info, dst_info))

    def one(self, src, dst):
        self.check_rows(src, dst)
        prsr = PreResolver(src)
        for station, df in prsr.datas.items():
            pt = ProcesserTable1(df)
            f = os.path.join(dst, "table1_{}.csv".format(station))
            pt.to_csv(f)
        print("write table one successfuly!")
        
        
    def two(self, src, dst):
        self.check_rows(src, dst)
        prsr = PreResolver(src)
        for station, df in prsr.datas.items():
            pt = ProcesserTable2(df)
            df = pt.get_table2_year_df()
            f = os.path.join(dst, "table2_year_{}.csv".format(station))
            pt.to_csv(df, f)
            df = pt.get_table2_year_mon_df()
            f = os.path.join(dst, "table2_year_mon_{}.csv".format(station))
            pt.to_csv(df, f)
        print("write two tables successfuly!")

    def three(self, src, dst):
        self.check_rows(src, dst)
        prsr = PreResolver(src)
        for station, df in prsr.datas.items():
            to = os.path.join(dst, str(station))
            if not os.path.exists(to):
                os.mkdir(to)
            pt2 = ProcesserTable2(df)
            mp = MyPlot(pt2)
            mp.save_all_mon_bar_picture(to_dir=to)
            mp.save_all_year_line_picture(to_dir=to)
        print("plot picture three successfuly!")

    def make_widgets(self):
        tk.Button(self.root, text="One", command= 
                (lambda: self.one(self.row_src.path.get(), self.row_dst.path.get()))).pack(side=tk.LEFT)
        tk.Button(self.root, text="Two", command=
                  (lambda: self.two(self.row_src.path.get(), self.row_dst.path.get()))).pack(side=tk.LEFT)
        tk.Button(self.root, text="Three", command=
                  (lambda: self.three(self.row_src.path.get(), self.row_dst.path.get()))).pack(side=tk.LEFT)
        Quitter().top.pack(side=tk.RIGHT)





Window().root.mainloop()
