from fastapi import FastAPI, HTTPException
import pandas as pd

# Load the cleaned CSV file
df = pd.read_csv("data/startups_clean.csv")

# Initialize FastAPI app
app = FastAPI(title="Startup Profiler API")

# ----------- API Endpoints -----------

@app.get("/")
def home():
    return {"message": "Welcome to the Startup Profiler API"}

@app.get("/summary")
def get_summary():
    return {
        "total_companies": len(df),
        "average_revenue": round(df["Revenue"].mean(), 2),
        "average_growth": round(df["Growth %"].mean(), 2)
    }

@app.get("/industry-distribution")
def get_industry_distribution():
    return df["Industry"].value_counts().to_dict()

@app.get("/company/{name}")
def get_company(name: str):
    company = df[df["Company Name"].str.lower() == name.lower()]
    if company.empty:
        raise HTTPException(status_code=404, detail="Company not found")
    return company.to_dict(orient="records")[0]

@app.get("/top-growth")
def get_top_growth():
    top_companies = df.sort_values(by="Growth %", ascending=False).head(5)
    return top_companies.to_dict(orient="records")
