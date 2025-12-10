from collections import namedtuple
import pandas as pd
import numpy as np
import copy
import sys

Vrange = namedtuple("Vrange", ["lo", "hi"])
ColIndex = namedtuple("ColIndex", ["icol", "col_name"])


class PreResolver:
    def __init__(self, data_file) -> None:
        self.data_fromcsv = pd.read_csv(data_file, encoding="gb18030")
        self.titles = self.data_fromcsv.columns
        self.station_nums = self.data_fromcsv.loc[:, self.titles[0]].unique()
        self.indexs_all, self.icol_indexs, self.indexs_range = self.get_indexs()
        data_all = copy.deepcopy(self.data_fromcsv)
        self.datas = {}
        for station_num in self.station_nums:
            raw_data = data_all[(data_all.iloc[:, 0]==station_num)]
            self.datas[station_num] = self.get_processed_pass_data(raw_data)

    def value_change(self, x:int):
        if 32000 <= x < 33000:
            return (x - 32000) * 0.1
        elif 31000 <= x < 32000:
            return (x - 31000) * 0.1
        elif 30000 <= x < 31000:
            return (x - 30000) * 0.1
        else:
            return x

    def get_indexs(self):
        self.indexs_all = dict(
        temperature_indexs = {i: col for i, col in enumerate(self.titles) if "温" in col},
        air_pressure_indexs = {i: col for i, col in enumerate(self.titles) if "气压" in col},
        wate_pressure_indexs = {i: col for i, col in enumerate(self.titles) if "水汽压" in col},
        relative_indexs = {i: col for i, col in enumerate(self.titles) if "相对" in col},
        rain_indexs = {i: col for i, col in enumerate(self.titles) if "降水量" in col},
        wind_ve_indexs = {i: col for i, col in enumerate(self.titles) if "风速" in col and "风向" not in col},
        wind_dir_indexs = {i: col for i, col in enumerate(self.titles) if "风向" in col},
        day_hours_indexs = {i: col for i, col in enumerate(self.titles) if "时数" in col},
        vaper_indexs = {i: col for i, col in enumerate(self.titles) if "蒸发量" in col},
        )
        self.icol_indexs = dict()
        for name, _map in self.indexs_all.items():
            self.icol_indexs.update({key: name for key in _map.keys()})

        self.indexs_range = dict(
        temperature_indexs = Vrange(-100, 100),
        air_pressure_indexs = Vrange(0, 2000),
        wate_pressure_indexs = Vrange(0, 100),
        relative_indexs = Vrange(0, 100),
        rain_indexs = Vrange(0, 1000),
        wind_ve_indexs = Vrange(0, 100),
        wind_dir_indexs = Vrange(1, 16),
        day_hours_indexs = Vrange(0, 24),
        vaper_indexs = Vrange(0, 1000),
        )
        return self.indexs_all, self.icol_indexs, self.indexs_range


    def is_col_value_in_range(self, i, raw_data):
        col = raw_data.iloc[:, i]
        desc = col.describe()
        vrange = self.indexs_range[self.icol_indexs[i]]
        if vrange.lo <= desc["min"] and desc["max"] <= vrange.hi:
            return True
        else:
            False
    
    def check_data_valid(self, raw_data):
        passes = []
        faileds = []
        for _, d in self.indexs_all.items():
            for i, col_name in d.items():
                if self.is_col_value_in_range(i, raw_data):
                    passes.append(ColIndex(i, col_name))
                else:
                    faileds.append(ColIndex(i, col_name))
        return passes, faileds

    def replace_invalid_by_nan(self, raw_data):
        for i in range(4, self.titles.size):
            col = raw_data.iloc[:, i]
            col.replace([32744, 32766], np.nan, inplace=True)
            col.replace(32700, 0, inplace=True)
            new = col.map(self.value_change, 'ignore')
            raw_data.iloc[:, i] = new
        return raw_data
    
    def get_processed_pass_data(self, raw_data: pd.DataFrame):
        p, f = self.check_data_valid(raw_data)
        print("before clean:")
        print(f)
        data = self.replace_invalid_by_nan(raw_data)
        p, f = self.check_data_valid(raw_data)
        assert not f
        print("after clean:")
        print(f)
        return data


if __name__ == "__main__":
    prsr = PreResolver(sys.argv[1])
