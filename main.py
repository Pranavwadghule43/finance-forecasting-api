from fastapi import FastAPI, HTTPException
from queries import (
    get_departments,
    get_budget_by_department,
    get_forecast_by_department,
    get_variance_by_department
)

app = FastAPI(title="Finance Forecasting API")


# ------------------------
# Health Check
# ------------------------
@app.get("/health")
def health():
    return {"status": "API is running"}


# ------------------------
# Get all departments (REAL SQL)
# ------------------------
@app.get("/departments")
def departments():
    return get_departments()


# ------------------------
# Get historical budget (REAL SQL)
# ------------------------
@app.get("/budget/{dept}")
def budget(dept: str):
    data = get_budget_by_department(dept)
    if not data:
        raise HTTPException(status_code=404, detail="Department not found")
    return [{"month": row["month"], "amount": row["amount"]} for row in data]


# ------------------------
# Get forecast data (REAL SQL)
# ------------------------
@app.get("/forecast/{dept}")
def forecast(dept: str):
    data = get_forecast_by_department(dept)
    if not data:
        raise HTTPException(status_code=404, detail="Department forecast not found")
    return [{"month": row["month"], "predicted": row["predicted_amount"]} for row in data]


# ------------------------
# Get variance (REAL SQL)
# ------------------------
@app.get("/variance/{dept}")
def variance(dept: str):
    data = get_variance_by_department(dept)
    if not data:
        raise HTTPException(status_code=404, detail="Variance data not found")

    return [
        {
            "forecast_month": row["forecast_month"],
            "actual_month": row["actual_month"],
            "actual": row["actual"],
            "forecast": row["forecast"],
            "variance": row["variance"],
            "variance_percent": row["variance_percent"]
        }
        for row in data
    ]

