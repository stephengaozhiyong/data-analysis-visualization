import pandas as pd

indexs_table1 = ["类型", "数值", "日期"]
map1_table1 = {
"多年平均年降水量": 14,	
"多年平均最大日降水量": 14,	
"最大一日降水量": 14,
"多年极大风速": -9,	
"最大一日极大风速极值": -9,
"最大一日极大风速风向": -8	
}
map1_table1_mean_mean = {
"多年平均气压": 7,	
"多年平均水汽压": -1,	
"多年平均相对湿度": 10,	
"多年平均气温": 4,	
"多年平均风速": 15,
}       #每日的平均值
map1_table1.update(map1_table1_mean_mean)


class ProcesserTable1:
    def __init__(self, df: pd.DataFrame) -> None:
        self.data = df
        self.table_content = self.get_table1_data()

    def get_dates(self, i, value):
        df = self.data
        _raw = df[df.iloc[:, i] == value]
        dates = []
        for i in range(len(_raw.index)):
            year, mon, day = _raw.iloc[i, 1], _raw.iloc[i, 2], _raw.iloc[i, 3]
            date = "{}年{}月{}日".format(year, mon, day)
            dates.append(date)
        if len(dates) > 1:
            return dates
        elif len(dates) == 1:
            return dates.pop()
        else:
            return None

    def get_table1_data(self):
        cols = self.data.columns
        df = self.data
        mean_by_year_mean =df.groupby(cols[1]).mean().mean()
        res = {}
        for key, value in map1_table1_mean_mean.items():
            res[key] = (mean_by_year_mean.loc[cols[value]], None)

        res["多年平均年降水量"] = (df.groupby(cols[1]).sum().mean().loc[cols[14]], None)
        res["多年平均最大日降水量"] = (df.groupby(cols[1]).max().mean().loc[cols[14]], None)
        shui_max_max = df.groupby(cols[1]).max().max().loc[cols[14]]
        dates = self.get_dates(14, shui_max_max)
        res["最大一日降水量"] = (shui_max_max, dates)
        res["多年极大风速"] = (df.groupby(cols[1]).max().mean().loc[cols[-9]], None)
        fensu_max_max = df.groupby(cols[1]).max().max().loc[cols[-9]]
        dates = self.get_dates(-9, fensu_max_max)
        res["最大一日极大风速极值"] = (fensu_max_max, dates)
        a = df[df.iloc[:, -9] == fensu_max_max]
        assert a.index.size == 1
        res["最大一日极大风速风向"] = (a.loc[a.index[0], cols[-8]], None)

        table_content = []
        for key, value in res.items():
            table_content.append((key, *value))
        return table_content
    
    def to_csv(self, to, encoding="gb18030"):
        df = pd.DataFrame(self.table_content, columns=indexs_table1)
        df.to_csv(to, encoding=encoding, index=False)