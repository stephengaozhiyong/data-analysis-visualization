from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from enums import Statement
from models import QueryForm, QueryForm1
from service import get_finance_data, build_chart, json_to_dataframe, get_indicator_dict

app = FastAPI(title="金融分析系统")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # ✅ 所有来源都允许（开发用）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def index():
    return FileResponse("static/index.html")


@app.get("/api/symbols")
def get_symbols():
    return [
        {"label": "茅台", "value": "SH600519"},
        {"label": "五粮液", "value": "SZ000858"}
    ]

@app.get("/api/statements")
def get_statements():
    return Statement.to_options()

@app.post("/api/indicators")
def get_indicators(form: QueryForm):
    df = json_to_dataframe(form.symbol, form.statement)
    column_map = get_indicator_dict()
    res = []
    for col in df.columns.to_list():
        res.append({
            "label": column_map.get(col, col),
            "value": col,
        })
    return res

@app.post("/api/chart")
def get_chart(form: QueryForm1):
    data = get_finance_data(form.symbol, form.statement, form.indicator)
    chart = build_chart(data)
    return chart