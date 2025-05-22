import os
import json
from fastapi.testclient import TestClient
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.api import app

client = TestClient(app)

def load_payload(name):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "example_payloads", name)
    with open(path) as f:
        return json.load(f)

def test_api_ok():
    payload = load_payload("payload1.json")
    response = client.post("/productionplan", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert all("name" in p and "p" in p for p in body)

def test_api_invalid_input():
    response = client.post("/productionplan", json={"load": 50})
    assert response.status_code == 422  # error de validación FastAPI

def test_api_infeasible_load():
    payload = {
        "load": 9999,
        "fuels": {
            "gas(euro/MWh)": 10,
            "wind(%)": 0
        },
        "powerplants": [
            {"name": "g1", "type": "gasfired", "efficiency": 0.5, "pmin": 10, "pmax": 50}
        ]
    }
    response = client.post("/productionplan", json=payload)
    assert response.status_code == 400
    assert "No se pudo satisfacer exactamente la carga" in response.text
