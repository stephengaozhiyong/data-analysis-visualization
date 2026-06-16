from enum import Enum

class Statement(Enum):
    CASH_FLOW = ("现金流量表", "cash_flow")
    BALANCE = ("资产负债表", "balance")
    INCOME = ("利润表", "income")

    def __init__(self, label, value):
        self.label = label
        self._value_ = value

    @classmethod
    def to_options(cls):
        return [
            {"label": item.label, "value": item.value}
            for item in cls
        ]
    

if __name__ == '__main__':
    print(Statement.to_options())