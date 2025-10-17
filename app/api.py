from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from tensorflow.keras.models import load_model
import os

app = FastAPI(title="API de Predicción de Volatilidad")

# 📁 Ruta base donde están los modelos (ajustable con variable de entorno)
BASE_MODELS_DIR = os.getenv("MODELS_PATH", "models")

class LagInput(BaseModel):
    lag: int  # Ejemplo: 7, 14, 21, 28

def cargar_modelo(lag: int):
    """Carga el modelo correspondiente al lag dado."""
    model_path = os.path.join(BASE_MODELS_DIR, f"lag_{lag}", f"mejor_fold_lag_{lag}.keras")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"No se encontró el modelo para lag {lag} en {model_path}")
    return load_model(model_path)

@app.get("/")
def root():
    return {"message": "API de predicción de volatilidad lista 🚀"}

@app.post("/predict")
def predict_volatilidad(input_data: LagInput):
    lag = input_data.lag
    try:
        model = cargar_modelo(lag)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    # Generar features de ejemplo (debes reemplazarlas con tus datos reales)
    X = np.random.rand(1, lag)

    preds = model.predict(X)[0]
    preds = [float(x) for x in preds]

    return {"lag": lag, "predictions": preds}

@app.get("/predict/{lag}")
def predict_volatilidad_get(lag: int):
    try:
        model = cargar_modelo(lag)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    X = np.random.rand(1, lag)
    preds = model.predict(X)[0]
    preds = [float(x) for x in preds]

    return {"lag": lag, "predictions": preds}
