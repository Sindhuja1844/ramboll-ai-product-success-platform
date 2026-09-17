from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Product
from analytics import (
    get_product_usage,
    calculate_traction,
    detect_early_failure,
    calculate_cost_per_user,
    calculate_success_score,
    get_department_metrics
)


app = FastAPI(
    title="AI Product Success & Usage Observability Platform"
)


# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# DATABASE DEPENDENCY
# -----------------------------

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# -----------------------------
# ROOT
# -----------------------------

@app.get("/")
def root():
    return {
        "message": "AI Product Success Platform API is running"
    }


# -----------------------------
# PRODUCTS
# -----------------------------

@app.get("/products")
def get_products(db: Session = Depends(get_db)):

    products = db.query(Product).all()

    return [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "launch_date": product.launch_date,
            "owning_team": product.owning_team
        }
        for product in products
    ]


# -----------------------------
# DASHBOARD
# -----------------------------

@app.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):

    products = db.query(Product).all()

    total_active_users = 0
    growing_products = 0
    at_risk_products = 0

    for product in products:

        usage_data = get_product_usage(
            db,
            product.id
        )

        if usage_data:
            latest_users = usage_data[-1].active_users
            total_active_users += latest_users

        traction = calculate_traction(
            usage_data
        )

        if traction == "Growing":
            growing_products += 1

        if detect_early_failure(
            usage_data
        ):
            at_risk_products += 1

    return {
        "total_products": len(products),
        "total_active_users": total_active_users,
        "growing_products": growing_products,
        "at_risk_products": at_risk_products
    }


# -----------------------------
# PRODUCT DETAILS
# -----------------------------

@app.get("/products/{product_id}")
def get_product_details(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        return {
            "error": "Product not found"
        }

    usage_data = get_product_usage(
        db,
        product_id
    )

    usage_trend = [
        {
            "date": item.date,
            "active_users": item.active_users,
            "sessions": item.sessions,
            "feature_events": item.feature_events
        }
        for item in usage_data
    ]

    traction = calculate_traction(
        usage_data
    )

    early_failure = detect_early_failure(
        usage_data
    )

    cost_per_user = calculate_cost_per_user(
        db,
        product_id
    )

    success_score = calculate_success_score(
        db,
        product_id
    )

    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "launch_date": product.launch_date,
        "owning_team": product.owning_team,
        "traction": traction,
        "early_failure": early_failure,
        "cost_per_user": cost_per_user,
        "success_score": success_score,
        "usage_trend": usage_trend
    }


# -----------------------------
# DEPARTMENTS
# -----------------------------

@app.get("/departments")
def get_departments(
    db: Session = Depends(get_db)
):

    return get_department_metrics(db)