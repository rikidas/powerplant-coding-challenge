import pytest
import os
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main.production_plan import build_production_plan

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "energy_resources.json")

@pytest.fixture
def config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def test_exact_load(config):
    payload = {
        "load": 300,
        "fuels": {
            "gas(euro/MWh)": 13.0,
            "kerosine(euro/MWh)": 50.0,
            "co2(euro/ton)": 20,
            "wind(%)": 100
        },
        "powerplants": [
            {
                "name": "wind1",
                "type": "windturbine",
                "efficiency": 1.0,
                "pmin": 0,
                "pmax": 100
            },
            {
                "name": "gas1",
                "type": "gasfired",
                "efficiency": 0.5,
                "pmin": 50,
                "pmax": 150
            },
            {
                "name": "tj1",
                "type": "turbojet",
                "efficiency": 0.3,
                "pmin": 0,
                "pmax": 200
            }
        ]
    }
    result = build_production_plan(payload, config)
    total = round(sum(p["p"] for p in result), 1)
    assert total == 300
    assert all(int(round(p["p"] * 10)) == round(p["p"] * 10) for p in result)  # múltiplos de 0.1

def test_pmin_respected(config):
    payload = {
        "load": 200,
        "fuels": {
            "gas(euro/MWh)": 10,
            "kerosine(euro/MWh)": 50,
            "co2(euro/ton)": 0,
            "wind(%)": 0
        },
        "powerplants": [
            {
                "name": "gas1",
                "type": "gasfired",
                "efficiency": 0.5,
                "pmin": 100,
                "pmax": 200
            },
            {
                "name": "tj1",
                "type": "turbojet",
                "efficiency": 0.3,
                "pmin": 0,
                "pmax": 50
            }
        ]
    }
    result = build_production_plan(payload, config)
    for plant in payload["powerplants"]:
        plan = next(p for p in result if p["name"] == plant["name"])
        if plan["p"] > 0:
            assert plan["p"] >= plant["pmin"]
        assert plan["p"] <= plant["pmax"]


def test_unreachable_load(config):
    payload = {
        "load": 1000,
        "fuels": {
            "gas(euro/MWh)": 10,
            "kerosine(euro/MWh)": 60,
            "co2(euro/ton)": 0,
            "wind(%)": 0
        },
        "powerplants": [
            {
                "name": "gas1",
                "type": "gasfired",
                "efficiency": 0.5,
                "pmin": 100,
                "pmax": 200
            }
        ]
    }

    with pytest.raises(ValueError, match="No se pudo satisfacer exactamente la carga"):
        build_production_plan(payload, config)

def test_unknown_type(config):
    payload = {
        "load": 100,
        "fuels": {
            "gas(euro/MWh)": 10,
            "wind(%)": 0
        },
        "powerplants": [
            {
                "name": "fusion1",
                "type": "coldfusion",
                "efficiency": 1.0,
                "pmin": 0,
                "pmax": 1000
            }
        ]
    }

    with pytest.raises(ValueError, match="Tipo de planta desconocido"):
        build_production_plan(payload, config)
