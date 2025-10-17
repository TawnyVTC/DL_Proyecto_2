from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
from pathlib import Path
from functools import lru_cache
from fastapi.responses import JSONResponse

app = FastAPI(title="API de Predicción de Volatilidad")

# Base dir donde están los modelos (relativo al root del repo)
BASE_MODELS_DIR = Path(__file__).resolve().parents[1] / "models"

# Lags permitidos
ALLOWED_LAGS = {7, 14, 21, 28}


class LagInput(BaseModel):
    lag: int
    # Optional: si prefieres pasar las últimas 'lag' observaciones, envíalas aquí.
    features: Optional[List[float]] = None


class PredictionResponse(BaseModel):
    predictions: List[float]


# Cargador de modelos con cache simple (por lag)
@lru_cache(maxsize=16)
def load_model_for_lag(lag: int):
    """Carga y devuelve un modelo keras para el lag solicitado."""
    model_dir = BASE_MODELS_DIR / f"lag_{lag}"
    model_path = model_dir / f"mejor_fold_lag_{lag}.keras"

    if not model_path.exists():
        raise FileNotFoundError(f"No se encuentra el modelo para lag={lag} en {model_path}")

    try:
        from tensorflow.keras.models import load_model
    except Exception as e:
        raise RuntimeError("Error importando tensorflow.keras. Asegúrate de tener tensorflow instalado.") from e

    return load_model(str(model_path))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(input: LagInput):
    """
    Request example:
    {
      "lag": 7
    }
    Response:
    {
      "predictions": [0.1, 0.2, ...]  # 7 floats
    }
    """
    lag = input.lag
    if lag not in ALLOWED_LAGS:
        raise HTTPException(
            status_code=400,
            detail=f"El parámetro 'lag' debe ser uno de {sorted(ALLOWED_LAGS)}."
        )

    # Cargar modelo
    try:
        model = load_model_for_lag(lag)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cargando el modelo: {e}")

    # Preparar input
    if input.features is not None:
        features = np.asarray(input.features, dtype=float)
        if features.ndim != 1:
            raise HTTPException(status_code=400, detail="El campo 'features' debe ser una lista (vector).")
        if len(features) != lag:
            raise HTTPException(
                status_code=400,
                detail=f"Si envías 'features', su longitud debe ser igual a 'lag' ({lag})."
            )
        X = features.reshape(1, -1)
    else:
        input_size = model.input_shape[-1]
        X = np.zeros((1, input_size), dtype=float)

    # Predicción
    try:
        pred = model.predict(X)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error durante la predicción: {e}")

    pred = np.asarray(pred).reshape(-1)
    if pred.size < 7:
        padded = np.zeros(7, dtype=float)
        padded[:pred.size] = pred
        out = padded.tolist()
    else:
        out = pred[:7].astype(float).tolist()

    return PredictionResponse(predictions=out)


@app.get("/predict/{lag}", response_model=PredictionResponse)
def predict_from_url(lag: int):
    """
    Permite hacer predicciones directamente desde el navegador:
    Ejemplo:
    http://127.0.0.1:8000/predict/7
    """
    if lag not in ALLOWED_LAGS:
        raise HTTPException(
            status_code=400,
            detail=f"Solo se permiten los siguientes lags: {sorted(ALLOWED_LAGS)}."
        )

    try:
        model = load_model_for_lag(lag)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cargando el modelo: {e}")

    input_size = model.input_shape[-1]
    X = np.zeros((1, input_size), dtype=float)

    try:
        pred = model.predict(X)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error durante la predicción: {e}")

    pred = np.asarray(pred).reshape(-1)
    if pred.size < 7:
        padded = np.zeros(7, dtype=float)
        padded[:pred.size] = pred
        out = padded.tolist()
    else:
        out = pred[:7].astype(float).tolist()

    return JSONResponse(content={"predictions": out})
