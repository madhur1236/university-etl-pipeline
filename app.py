from fastapi import FastAPI, HTTPException
from etl import run_etl
import pandas as pd
from sqlalchemy import create_engine
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
        <html>
        <head>
            <title>University ETL App</title>
            <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🎓</text></svg>">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin-top: 100px;
                    background-color: #f4f4f4;
                }
                h1 {
                    color: #2c3e50;
                }
                p {
                    color: #555;
                }
                a {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 20px;
                    background: #007bff;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <h1>🎓 University ETL App</h1>
            <p>Extract, Transform, and Load university data from a public API.</p>

            <a href="/docs">Open API Documentation</a>
        </body>
    </html>
    """


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