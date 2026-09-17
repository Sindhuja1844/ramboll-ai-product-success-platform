import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

import "./App.css";

const API = "http://127.0.0.1:8000";

function prepareChartData(data) {
  const grouped = {};

  data.forEach((item) => {
    if (!grouped[item.date]) {
      grouped[item.date] = {
        date: item.date,
        active_users: 0
      };
    }

    grouped[item.date].active_users += item.active_users;
  });

  return Object.values(grouped);
}

function App() {
  const [dashboard, setDashboard] = useState(null);
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [departments, setDepartments] = useState([]);

  useEffect(() => {
    loadDashboard();
    loadProducts();
    loadDepartments();
  }, []);

  async function loadDashboard() {
    const response = await fetch(`${API}/dashboard`);
    const data = await response.json();
    setDashboard(data);
  }

  async function loadProducts() {
    const response = await fetch(`${API}/products`);
    const data = await response.json();

    setProducts(data);

    if (data.length > 0) {
      loadProductDetails(data[0].id);
    }
  }

  async function loadProductDetails(id) {
    const response = await fetch(`${API}/products/${id}`);
    const data = await response.json();
    setSelectedProduct(data);
  }

  async function loadDepartments() {
    const response = await fetch(`${API}/departments`);
    const data = await response.json();
    setDepartments(data);
  }

  if (!dashboard || !selectedProduct) {
    return <div className="loading">Loading platform...</div>;
  }

  return (
    <div className="app">

      <header className="header">
        <div>
          <h1>AI Product Success Platform</h1>
          <p>Usage observability and product performance intelligence</p>
        </div>
      </header>

      <main>

        <section className="metrics">

          <div className="metric-card">
            <span>Total Products</span>
            <strong>{dashboard.total_products}</strong>
          </div>

          <div className="metric-card">
            <span>Active Users</span>
            <strong>{dashboard.total_active_users}</strong>
          </div>

          <div className="metric-card">
            <span>Growing Products</span>
            <strong>{dashboard.growing_products}</strong>
          </div>

          <div className="metric-card">
            <span>Products At Risk</span>
            <strong>{dashboard.at_risk_products}</strong>
          </div>

        </section>

        <section className="section">

          <div className="section-header">
            <div>
              <h2>Product Performance</h2>
              <p>Select a product to inspect its performance.</p>
            </div>

            <select
              value={selectedProduct.id}
              onChange={(e) =>
                loadProductDetails(e.target.value)
              }
            >
              {products.map((product) => (
                <option
                  key={product.id}
                  value={product.id}
                >
                  {product.name}
                </option>
              ))}
            </select>
          </div>

          <div className="product-info">

            <div>
              <h2>{selectedProduct.name}</h2>
              <p>{selectedProduct.description}</p>
              <p>
                Owning team: <strong>
                  {selectedProduct.owning_team}
                </strong>
              </p>
            </div>

            <div className="status">
              <span>Traction</span>
              <strong>{selectedProduct.traction}</strong>
            </div>

            <div className="status">
              <span>Success Score</span>
              <strong>{selectedProduct.success_score}</strong>
            </div>

            <div className="status">
              <span>Cost / User</span>
              <strong>₹{selectedProduct.cost_per_user}</strong>
            </div>

            <div className="status">
               <span>Early Failure</span>
               <strong>
               {selectedProduct.early_failure ? "At Risk" : "Healthy"}
               </strong>
               </div>

          </div>

        </section>

        <section className="section">

          <h2>Usage Trend</h2>

          <div className="chart">

            <ResponsiveContainer width="100%" height={320}>

              <LineChart data={prepareChartData(selectedProduct.usage_trend)}>

                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="date" />

                <YAxis />

                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="active_users"
                  name="Active Users"
                  stroke="#2563eb"
                  strokeWidth={3}
                  dot={{ r: 5 }}
                  activeDot={{ r: 7 }}
                />

              </LineChart>

            </ResponsiveContainer>

          </div>

        </section>

        <section className="section">

          <h2>Department Analysis</h2>

          <div className="department-grid">

            {departments.map((department) => (

              <div
                className="department-card"
                key={department.department}
              >

                <h3>{department.department}</h3>

                <p>
                  Active Users:
                  <strong> {department.active_users}</strong>
                </p>

                <p>
                  Cost / User:
                  <strong> ₹{department.cost_per_user}</strong>
                </p>

              </div>

            ))}

          </div>

        </section>

        <section className="section insight">

           <h2>Business Insight</h2>

          <p>
            {selectedProduct.traction === "Growing"
            ? `${selectedProduct.name} is showing positive adoption growth. The product can be monitored for continued usage and expansion across departments.`
            : selectedProduct.traction === "Declining"
            ? `${selectedProduct.name} is showing declining adoption. The business should investigate recent usage patterns and identify possible causes of reduced engagement.`
            : `${selectedProduct.name} has relatively stable adoption. Continued monitoring can help identify future growth or decline.`
            }
          </p>
  
        </section>

      </main>

    </div>
  );
}

export default App;