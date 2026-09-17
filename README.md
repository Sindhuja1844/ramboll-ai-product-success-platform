AI Product Success & Usage Observability Platform

A working prototype for monitoring AI product adoption, usage trends, early-failure signals, cost efficiency, and department-level usage.

1. Problem

AI products can have good initial adoption but later experience declining usage or high costs. This platform helps a product/business leader identify these signals and investigate individual products.

2. Key Features

1) Product Overview Dashboard

Shows:

* Total products
* Active users
* Growing products
* Products at risk

2) Product Drill-down

A product can be selected to view:

* Traction
* Success score
* Cost per user
* Early-failure status
* Usage trend

3) Early-Failure Detection

The system flags a product when its latest four usage periods continuously decrease.

Example:

`70 → 65 → 40 → 23 → 15`

4) Department & Cost Analysis

Shows active users and cost per user for different departments.

Feature Priority

I prioritized the features in this order:

Overview → Drill-down → Early Failure → Cost/Department Analysis

This follows a simple business investigation flow: first understand the portfolio, then investigate a product, identify risk, and finally understand cost and organizational usage.

3. Architecture — HLD

React + Vite
     ↓
FastAPI REST APIs
     ↓
Business Logic / Analytics
     ↓
SQLite Database

The frontend handles the dashboard and visualization.
FastAPI provides the APIs and business logic.
SQLite stores product, usage, department and cost data.

LLD

For a product detail request:

GET /products/{id}
        ↓
Fetch product + usage + cost data
        ↓
Calculate traction
        ↓
Check early failure
        ↓
Calculate cost/user and success score
        ↓
Return JSON


4. Database Schema

Main tables:

Products
- id
- name
- description
- launch_date
- owning_team

Departments
- id
- name

Usage
- id
- product_id
- department_id
- date
- active_users
- sessions
- feature_events

Costs
- id
- product_id
- department_id
- date
- compute_cost
- token_cost

'Products' and 'Departments' are connected to their corresponding 'Usage' and 'Costs' records using foreign keys.


5. API Design

| Method | Endpoint         | Purpose                       |
| ------ | ---------------- | ----------------------------- |
| GET    | products         | List products                 |
| GET    | dashboards       | Platform KPIs                 |
| GET    | products{id}     | Product details and analytics |
| GET    | departments       | Department metrics            |

FastAPI Swagger documentation is available at '/docs'.



6. Business Logic

Traction

Growth > 15%       → Growing
-15% to 15%        → Stable
Growth < -15%      → Declining

Cost per User

(Compute Cost + Token Cost) / Active Users

Success Score

The prototype combines:

* Usage growth — 40%
* Engagement — 30%
* Department adoption — 30%

These are prototype assumptions for demonstrating the concept, not official Ramboll formulas.


7. Technology

Frontend: React, Vite, Recharts, CSS
Backend: Python, FastAPI, SQLAlchemy
Database: SQL 
Control: Git, GitHub

8. Running the Project

Backend

.\venv\Scripts\Activate.ps1
cd backend
uvicorn main:app --reload

Frontend

cd frontend
npm install
npm run dev


9. Git Usage

The project is maintained using Git and GitHub.

Development changes can be made through branches and reviewed using pull requests before merging into `main`.

Example:

Branch → Commit → Push → Pull Request → Merge


10. Assumptions & Future Improvements

The prototype uses mock data and prototype business rules.

Possible future improvements:

* Authentication and role-based access
* Automated telemetry ingestion
* Configurable alerts
* Production database
* Automated testing and CI/CD
* Cloud deployment
