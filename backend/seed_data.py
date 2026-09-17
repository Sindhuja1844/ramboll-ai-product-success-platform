from datetime import date, timedelta

from database import engine, SessionLocal, Base
from models import Product, Department, Usage, Cost


Base.metadata.create_all(bind=engine)

db = SessionLocal()


# -----------------------------
# PRODUCTS
# -----------------------------

products = [
    Product(
        name="AI Design Assistant",
        description="AI assistant for engineering design support",
        launch_date=date(2026, 1, 10),
        owning_team="Engineering AI"
    ),
    Product(
        name="Document Copilot",
        description="AI assistant for searching internal documents",
        launch_date=date(2026, 2, 15),
        owning_team="Digital Solutions"
    ),
    Product(
        name="Energy Insights",
        description="AI-powered energy analysis tool",
        launch_date=date(2026, 3, 1),
        owning_team="Energy AI"
    ),
    Product(
        name="Project Risk AI",
        description="AI tool for identifying project risks",
        launch_date=date(2026, 4, 20),
        owning_team="Project Intelligence"
    )
]

db.add_all(products)
db.commit()


# -----------------------------
# DEPARTMENTS
# -----------------------------

departments = [
    Department(name="Engineering"),
    Department(name="Energy"),
    Department(name="Architecture"),
    Department(name="Digital Solutions")
]

db.add_all(departments)
db.commit()


# Get generated IDs
products = db.query(Product).all()
departments = db.query(Department).all()


# -----------------------------
# USAGE PATTERNS
# -----------------------------

usage_patterns = {
    "AI Design Assistant": [20, 27, 35, 44, 53, 67],
    "Document Copilot": [70, 82, 65, 40, 23, 15],
    "Energy Insights": [40, 42, 41, 43, 44, 45],
    "Project Risk AI": [12, 10, 14, 11, 9, 8]
}


# -----------------------------
# CREATE USAGE + COST DATA
# -----------------------------

start_date = date(2026, 8, 1)

for product in products:

    pattern = usage_patterns[product.name]

    for week, users in enumerate(pattern):

        current_date = start_date + timedelta(days=week * 7)

        # Distribute users between departments
        for index, department in enumerate(departments):

            department_users = max(
                1,
                int(users * [0.40, 0.25, 0.20, 0.15][index])
            )

            sessions = department_users * 3
            feature_events = department_users * 8

            usage = Usage(
                product_id=product.id,
                department_id=department.id,
                date=current_date,
                active_users=department_users,
                sessions=sessions,
                feature_events=feature_events
            )

            db.add(usage)

            # Mock compute + token cost
            compute_cost = department_users * 40
            token_cost = department_users * 20

            cost = Cost(
                product_id=product.id,
                department_id=department.id,
                date=current_date,
                compute_cost=compute_cost,
                token_cost=token_cost
            )

            db.add(cost)


db.commit()

print("Database created successfully!")
print("Mock data inserted successfully!")

db.close()