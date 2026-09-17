from sqlalchemy.orm import Session
from models import Product, Department, Usage, Cost


def get_product_usage(db: Session, product_id: int):
    usage_data = (
        db.query(Usage)
        .filter(Usage.product_id == product_id)
        .order_by(Usage.date)
        .all()
    )

    return usage_data


def calculate_traction(usage_data):
    if len(usage_data) < 2:
        return "Insufficient data"

    first_users = usage_data[0].active_users
    last_users = usage_data[-1].active_users

    if first_users == 0:
        return "Insufficient data"

    growth = ((last_users - first_users) / first_users) * 100

    if growth > 15:
        return "Growing"

    elif growth < -15:
        return "Declining"

    else:
        return "Stable"


def detect_early_failure(usage_data):

    if len(usage_data) < 4:
        return False

    # Group usage by date
    daily_usage = {}

    for item in usage_data:
        if item.date not in daily_usage:
            daily_usage[item.date] = 0

        daily_usage[item.date] += item.active_users

    # Sort dates chronologically
    dates = sorted(daily_usage.keys())

    if len(dates) < 4:
        return False

    # Get the latest 4 usage periods
    recent = [
        daily_usage[date]
        for date in dates[-4:]
    ]

    # Early failure = usage decreases continuously
    for i in range(1, len(recent)):
        if recent[i] >= recent[i - 1]:
            return False

    return True


def calculate_cost_per_user(db: Session, product_id: int):

    usage_data = (
        db.query(Usage)
        .filter(Usage.product_id == product_id)
        .all()
    )

    cost_data = (
        db.query(Cost)
        .filter(Cost.product_id == product_id)
        .all()
    )

    total_users = sum(item.active_users for item in usage_data)

    total_cost = sum(
        item.compute_cost + item.token_cost
        for item in cost_data
    )

    if total_users == 0:
        return 0

    return round(total_cost / total_users, 2)


def calculate_success_score(db: Session, product_id: int):

    usage_data = get_product_usage(db, product_id)

    if len(usage_data) < 2:
        return 0

    first_users = usage_data[0].active_users
    last_users = usage_data[-1].active_users

    if first_users == 0:
        growth_score = 0
    else:
        growth = ((last_users - first_users) / first_users) * 100

        growth_score = max(0, min(100, 50 + growth))

    engagement_values = [
        item.feature_events / item.active_users
        for item in usage_data
        if item.active_users > 0
    ]

    if engagement_values:
        average_engagement = sum(engagement_values) / len(engagement_values)

        engagement_score = min(
            100,
            average_engagement * 10
        )
    else:
        engagement_score = 0

    department_count = len(
        set(item.department_id for item in usage_data)
    )

    department_score = min(
        100,
        department_count * 25
    )

    success_score = (
        growth_score * 0.40
        + engagement_score * 0.30
        + department_score * 0.30
    )

    return round(success_score, 2)


def get_department_metrics(db: Session):

    departments = db.query(Department).all()

    results = []

    for department in departments:

        usage_data = (
            db.query(Usage)
            .filter(Usage.department_id == department.id)
            .all()
        )

        cost_data = (
            db.query(Cost)
            .filter(Cost.department_id == department.id)
            .all()
        )

        total_users = sum(
            item.active_users
            for item in usage_data
        )

        total_cost = sum(
            item.compute_cost + item.token_cost
            for item in cost_data
        )

        cost_per_user = (
            total_cost / total_users
            if total_users > 0
            else 0
        )

        results.append({
            "department": department.name,
            "active_users": total_users,
            "cost_per_user": round(cost_per_user, 2)
        })

    return results