from pathlib import Path
import json
import pandas as pd



def load_or_cache(p: Path):
    if p.exists():
        with p.open(encoding="utf-8") as f:
            data = json.load(f)
        return data
    raise NotImplementedError
    data = fetch_func()
    path.write_text(data)
    return data


def split_metric_column(df, indicator) -> pd.DataFrame:
    df =pd.DataFrame(df[indicator].tolist(), index=df.index).rename(columns={0: 'values', 1: 'yoy'})
    df['values'] = df['values'].where(pd.notnull(df['values']), None)
    df['yoy'] = df['yoy'].where(pd.notnull(df['yoy']), None)
    return df

def get_indicator_dict():
    with Path("data/en-cn.json").open() as f:
        return json.load(f)

def json_to_dataframe(symbol: str, statement: str):
    file_path = Path(f"data/{symbol}") / f"{statement}_Q4.json"
    data = load_or_cache(file_path)
    year_list_data = data['data']['list']
    df = pd.DataFrame(year_list_data)
    df.index = pd.Index([int(x.removesuffix("年报")) for x in df['report_name']])
    df = df.sort_index()
    return df

def get_finance_data(symbol: str, statement: str, indicator):
    df = json_to_dataframe(symbol, statement)
    df = split_metric_column(df, indicator)
    data = [
        {
            k: (None if pd.isna(v) else v)
            for k, v in row.items()
        }
        for row in df.to_dict(orient='records')
    ]
    return {
        "years": df.index.to_list(),
        "values": [d['values'] for d in data],
        "yoy": [d['yoy'] for d in data],
    }



def build_chart(data):
    return {
        "type": "line",
        "title": "财务趋势",
        "x": data["years"],
        "y1": data["values"],
        "y2": data["yoy"]
    }



if __name__ == '__main__':
    df = get_finance_data("SH600519", "income")