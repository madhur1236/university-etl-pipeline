from fastapi import FastAPI, HTTPException
from etl import run_etl
import pandas as pd
from sqlalchemy import create_engine

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "University ETL API"
    }


@app.post("/run-etl")
def execute_etl():
    try:
        return run_etl()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/universities")
def get_universities():
    engine = create_engine(
        "sqlite:///data/universities.db"
    )
    df = pd.read_sql(
        "SELECT * FROM universities",
        engine
    )

    return df.to_dict(
        orient="records"
    )