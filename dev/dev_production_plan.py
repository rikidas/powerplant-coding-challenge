import json
import os


CONFIG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "config", "energy_resources.json")
)

def load_config(path):
    with open(path, "r") as f:
        return json.load(f)

def calculate_cost(plant, fuels, energy_config):
    config = energy_config.get(plant["type"])
    if not config:
        raise ValueError(f"Tipo de planta desconocido: {plant['type']}")

    if config["fuel"] is None:
        return 0.0

    fuel_price = fuels[config["fuel"]]
    co2_per_mwh = config.get("co2_emission_per_mwh", 0.0)
    co2_price = fuels.get("co2(euro/ton)", 0.0)

    return (fuel_price / plant["efficiency"]) + (co2_per_mwh * co2_price)

def calculate_available_power(plant, fuels, energy_config):
    config = energy_config.get(plant["type"])
    if not config:
        raise ValueError(f"Tipo de planta desconocido: {plant['type']}")

    if config.get("is_variable", False):
        factor = fuels.get(config["availability_key"], 100) / 100
        return plant["pmax"] * factor
    else:
        return plant["pmax"]

def distribute_load_between_plants(load, plants):
    total_pmin = sum(p['pmin'] for p in plants)
    total_pmax = sum(p['available_power'] for p in plants)

    if load < total_pmin or load > total_pmax:
        return None  # No se puede cubrir la carga con esos límites

    assigned = [p['pmin'] for p in plants]
    remaining = load - total_pmin

    for i, plant in enumerate(plants):
        available = plant['available_power'] - plant['pmin']
        add = min(available, remaining)
        assigned[i] += add
        remaining -= add
        if remaining <= 0:
            break

    if remaining > 0:
        return None

    return assigned

def build_production_plan(payload, energy_config):
    load = payload["load"]
    fuels = payload["fuels"]
    powerplants = payload["powerplants"]

    # Calculamos coste y potencia disponible
    for plant in powerplants:
        plant["cost"] = calculate_cost(plant, fuels, energy_config)
        plant["available_power"] = round(calculate_available_power(plant, fuels, energy_config), 1)

    # Ordenamos por coste ascendente
    sorted_plants = sorted(powerplants, key=lambda x: x["cost"])

    # Intentamos asignar carga sólo a las plantas necesarias (desde más baratas hacia arriba)
    for i in range(1, len(sorted_plants) + 1):
        subset = sorted_plants[:i]
        assigned_powers = distribute_load_between_plants(load, subset)
        if assigned_powers is not None:
            # Asignamos potencia y 0 para las que no se usan
            result = []
            for j, plant in enumerate(subset):
                p = round(assigned_powers[j], 1)
                result.append({"name": plant["name"], "p": p})
            # Para las plantas no usadas
            for plant in sorted_plants[i:]:
                result.append({"name": plant["name"], "p": 0.0})

            # Verificamos carga exacta
            total_assigned = sum(p["p"] for p in result)
            if abs(total_assigned - load) <= 0.1:
                return result

    # Si no pudo asignar exacto
    raise ValueError("No se pudo satisfacer exactamente la carga.")


if __name__ == "__main__":
    with open("./example_payloads/payload2.json", "r") as f:
        payload = json.load(f)

    energy_config = load_config(CONFIG_PATH)
    plan = build_production_plan(payload, energy_config)
    print(json.dumps(plan, indent=2))
