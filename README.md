# ⚡ Power Plant Production Plan API

This project is an API built with **FastAPI** that calculates an optimal electric production plan for a set of power plants given load and fuel conditions.

---

## 🚀 How to run the API

> **Important:** You must be in the project root directory to run these commands.

### 📦 Prerequisites

- Python 3.11+
- `pip`
- (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/MacOS
```

### 📥 Install dependencies

```bash
pip install -r requirements.txt
```

### ▶️ Run the API locally

```bash
uvicorn api.api:app --reload --port 8888
```

This will start the API at `http://localhost:8888`.

You can test the API with curl: 

```bash
curl -X POST http://localhost:8888/productionplan -H "Content-Type: application/json" -d "@example_payloads/payload2.json"
```

Or access the interactive Swagger docs at:

```
http://localhost:8888/docs
```

---

## 🧪 Running tests

This project uses `pytest`. To run tests:

```bash
pytest tests/
```


---

## 🐳 Deployment with Docker

### 📄 Dockerfile

A Dockerfile is included to build a container image for this API.

### 🚀 Build and run with Docker

```bash
docker build -t production-plan-api .
docker run -p 8888:8888 production-plan-api
```

---


## ⚙️ Customizing Energy Resource Configuration

The production logic reads powerplant characteristics from the file:

```
config/energy_resources.json
```

Default configuration:

```json
{
  "gasfired": {
    "fuel": "gas(euro/MWh)",
    "co2_emission_per_mwh": 0.3,
    "is_variable": false
  },
  "turbojet": {
    "fuel": "kerosine(euro/MWh)",
    "co2_emission_per_mwh": 0.3,
    "is_variable": false
  },
  "windturbine": {
    "fuel": null,
    "co2_emission_per_mwh": 0.0,
    "is_variable": true,
    "availability_key": "wind(%)"
  }
}
```

You can change fuel costs, CO₂ emissions, or availability logic as needed. If you want to add a new type of powerplant (e.g., solar), you can easily do so by editing this configuration file—**no need to modify the core code**.
## 📂 Project structure

```
Prueba_Engie/
├── api/
│   └── api.py
├── main/
│   └── production_plan.py
├── config/
│   └── energy_resources.json
├── example_payloads/
├── tests/
│   ├── test_api.py
│   └── test_core.py
├── requirements.txt
├── Dockerfile
└── README.md
```
