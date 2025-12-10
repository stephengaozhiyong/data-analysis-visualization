from IPython import get_ipython
import sys, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from prepare_data import PreResolver
from process_table2 import ProcesserTable2

WRYH = FontProperties(fname="fonts/SimHei.ttf")
# get_ipython().run_line_magic("load_ext", "autoreload")
# get_ipython().run_line_magic("autoreload", "2")

unit_map = {
    "气温": "(℃)",
    "降水量": "(mm)",
    "日照时数": "(h)",
    "风速": "(m/s)",
    "相对湿度": "(%)",
}

class MyPlot:
    def __init__(self, pt2: ProcesserTable2) -> None:
        self.mon_xlable = "月份"
        self.year_xlable = "年份"
        self.pt2 = pt2

    def get_unit(self, name):
        for k, v in unit_map.items():
            if k in name:
                return v

    def get_line_figure(self, x, y):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(x, y, marker="o", linewidth=3)
        label, xlabel = "年{}变化".format(y.name), "{}份".format(x.name)
        ylabel = "年{}{}".format(y.name, self.get_unit(y.name))
        ax.set_title(label=label, fontproperties=WRYH)
        ax.set_xlabel(xlabel=xlabel, fontproperties=WRYH)
        ax.set_ylabel(ylabel=ylabel, fontproperties=WRYH)
        # ax.set_ylim(bottom=0)
        # ax.set_ylim(top=3.5)
        for a, b in zip(x, y):
            ax.text(a, b, "{:.2f}".format(b), ha='center', va='bottom')
        ax.grid(visible=True, axis='y')
        return fig

    def get_bar_figure(self, x, y):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.bar(x, y, width=0.5)
        label, xlabel = "{}变化".format(y.name), "{}份".format(x.name)
        ylabel = "{}{}".format(y.name, self.get_unit(y.name))
        ax.set_title(label=label, fontproperties=WRYH)
        ax.set_xlabel(xlabel=xlabel, fontproperties=WRYH)
        ax.set_ylabel(ylabel=ylabel, fontproperties=WRYH)
        for a, b in zip(x, y):
            ax.text(a, b, "{:.2f}".format(b), ha='center', va='bottom')
        ax.grid(visible=True, axis='y')
        return fig
    
    def save_all_year_line_picture(self, to_dir="."):
        to_dir = os.path.join(to_dir, "数据随年变化图")
        if not os.path.exists(to_dir):
            os.mkdir(to_dir)
        df = self.pt2.get_table2_year_df()
        x = df.loc[:, "年"]
        table_year_cols = ["平均气温", "平均风速", "降水量", "日照和", "平均相对湿度"]
        for col in table_year_cols:
            y = df.loc[:, col]
            if col == "日照和":
                y.name = "总日照时数"
            fig = self.get_line_figure(x, y)
            fig_name = "{}.png".format(y.name)
            to = os.path.join(to_dir, fig_name)
            fig.savefig(to)
            # plt.show()

    def save_all_mon_bar_picture(self, to_dir="."):
        to_dir = os.path.join(to_dir, "累年数据随月变化图")
        if not os.path.exists(to_dir):
            os.mkdir(to_dir)
        df = self.pt2.get_table2_year_mon_mon_df()
        x = df.pop("月")
        for col in df.columns:
            y = df.loc[:, col]
            fig = self.get_bar_figure(x, y)
            fig_name = "{}.png".format(y.name)
            to = os.path.join(to_dir, fig_name)
            fig.savefig(to)
            # plt.show()

if __name__ == "__main__":
    pr = PreResolver(sys.argv[1], 55593)
    pr.process_over_all()
    pt2 = ProcesserTable2(pr.data)
    m = MyPlot(pt2)
    m.save_all_mon_bar_picture()
    m.save_all_year_line_picture()