# AI Analytics Service

FastAPI-based AI analytics microservice for Jewellery Work Order and Inventory Optimization.

---

# Features

- Inventory Recommendation System
- Top Selling Product Analysis
- Dead Stock Detection
- Demand Forecasting
- Smart Alerts System
- Purchase Pattern Analysis
- Trend Analysis
- Category Performance Analysis
- Seasonal Insights
- AI Auto Insights

---

# Tech Stack

- FastAPI
- SQLAlchemy
- SQL Server
- PyODBC
- Python

---

# Project Structure

ai-service/

├── app/

│ ├── api/

│ ├── services/

│ ├── repository/

│ ├── core/

│ ├── utils/

│ ├── constants/

│ └── models/

├── main.py

├── requirements.txt

├── .env.example

└── README.md

---

## Setup

### Create venv

python -m venv venv

### Activate

venv\Scripts\activate


## Install dependencies

pip install -r requirements.txt

---

# Run Server

uvicorn main:app --reload

---

# API Documentation

Swagger UI:

http://127.0.0.1:8000/docs

---

# Environment Variables

Create `.env` file:

DB_URL=your_database_connection_string

---

# Notes

- This service is designed as a standalone AI analytics microservice.
- Intended for integration with existing .NET backend systems.
- Supports scalable future AI/ML upgrades.