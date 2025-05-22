
# ⚡ Power Plant Production Plan API

Este proyecto es una API desarrollada con **FastAPI** que calcula un plan óptimo de producción eléctrica para un conjunto de plantas energéticas dadas unas condiciones de carga y combustibles.

---

## 🚀 Cómo levantar la API

### 📦 Requisitos previos

- Python 3.11+
- `pip`
- (Opcional) Crear y activar un entorno virtual:

```bash
python -m venv .venv
source .venv\Scripts\activate
```

### 📥 Instalación de dependencias

```bash
pip install -r requirements.txt
```

### ▶️ Ejecutar la API localmente

```bash
uvicorn api.api:app --reload --port 8888
```

Esto levantará la API en `http://localhost:8888`.

Puedes probarla accediendo a la documentación interactiva de Swagger en:

```
http://localhost:8888/docs
```

O bien con curl

```
curl -X POST http://localhost:8000/productionplan -H "Content-Type: application/json" -d "@example_payloads/payload2.json"
```


---

## 🧪 Ejecutar los tests

Este proyecto utiliza `pytest`. Para lanzar los tests:

```bash
pytest tests/
```

Asegúrate de tener instaladas las dependencias de desarrollo en `requirements.txt` o ejecuta:

```bash
pip install pytest
```

---

## 🐳 Despliegue con Docker

### 📄 Dockerfile

```

### 🚀 Construir y ejecutar

```bash
docker build -t production-plan-api .
docker run -p 8888:8888 production-plan-api
```

---

## 📂 Estructura del proyecto

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


