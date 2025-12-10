import sys
import pandas as pd
import numpy as np
from prepare_data import PreResolver
from process_table1 import ProcesserTable1
from process_table2 import ProcesserTable2

pr = PreResolver(sys.argv[1], 55593)
pr.process_over_all()
pt1 = ProcesserTable1(pr.data)
pt2 = ProcesserTable2(pr.data)
cols = pt1.data.columns
df = pt2.data