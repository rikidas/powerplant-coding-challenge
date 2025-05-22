from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Union
import main.production_plan as production_plan

app = FastAPI(title="Production Plan API", version="1.0")

class PowerPlant(BaseModel):
    name: str
    type: str
    efficiency: float
    pmin: float
    pmax: float

class Payload(BaseModel):
    load: float
    fuels: Dict[str, Union[float, int]]
    powerplants: List[PowerPlant]

@app.post("/productionplan")
async def production_core(payload: Payload):
    try:
        # Convertimos Pydantic -> dict
        payload_dict = payload.model_dump()
        config = production_plan.load_config()
        plan = production_plan.build_production_plan(payload_dict, config)
        return plan
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
