#  ***API de Predicción de Volatilidad***

Esta aplicación implementa una **API REST con FastAPI** que permite obtener **7 predicciones de volatilidad** a partir de modelos **MLP entrenados para distintos lags (7, 14, 21 y 38)**.

Los modelos están almacenados en la carpeta `models/` y cada uno se carga dinámicamente al recibir una solicitud.



## **Estructura del proyecto**


```bash
DL_Proyecto_2/
│
├── notebooks/              ← Notebooks del Jupyter Book
│   ├── EDA-Volatility
│   ├── Model-Training-Close
│   ├── Model-Training-Volatility
│   └── Analysis
│
├── data/              ← Datos y Resultados del Jupyter Book
│   ├── precio_cierre
│   ├── volatilidad
│
├── app/
│   └── api.py              ← Código principal de la API
│
├── models/                 ← Modelos MLP Entrenados
│   ├── lag_7/mejor_fold_lag_7.keras
│   ├── lag_14/mejor_fold_lag_14.keras
│   ├── lag_21/mejor_fold_lag_21.keras
│   └── lag_38/mejor_fold_lag_38.keras
│
├── tests/
│   └── test_api.py
│
├── requirements.txt        ← Librerías necesarias para el JBook
├── requirements_app.txt    ← Librerías necesarias para la APi
├── Dockerfile              ← Imagen para desplegar la API
└── README.md               ← Este archivo
```


##  **1. Requisitos**

Tener instalado **Docker** o **Python 3.11+**.

### *Opción A — Usar Docker*
Instala [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### *Opción B — Usar Python directamente*
Instala las dependencias:

```bash
pip install -r requirements_app.txt
```


##  **2. Ejecución con Docker**

### *Construir la imagen*

Desde la raíz del proyecto (`DL_Proyecto_2/`):

```bash
docker build -t api-volatilidad .
```

### *Correr el contenedor*

```bash
docker run -d -p 8000:8000 api-volatilidad
```

###  *Verificar que está corriendo*

Abrir en el navegador:

* Estado del servicio: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
* Documentación interactiva (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Ejemplo de predicción: [http://127.0.0.1:8000/predict/7](http://127.0.0.1:8000/predict/7)



##  **3. Uso de la API**

### *Endpoint 1 — `POST /predict`*

**Descripción:**
Devuelve 7 predicciones de volatilidad para un `lag` específico.

**Ejemplo de request:**

```json
{
  "lag": 14
}
```

**Ejemplo de response:**

```json
{
  "predictions": [0.045, 0.051, 0.063, 0.072, 0.078, 0.083, 0.089]
}
```



### *Endpoint 2 — `GET /predict/{lag}`*

**Descripción:**
Permite obtener las predicciones directamente desde el navegador sin enviar JSON.

**Ejemplo de uso:**

```
http://127.0.0.1:8000/predict/7
```

**Respuesta:**

```json
{
  "predictions": [0.045, 0.051, 0.063, 0.072, 0.078, 0.083, 0.089]
}
```

Solo se permiten los siguientes valores de lag:

> **7, 14, 21 y 38**



###  *Endpoint 3 — `GET /health`*
**Descripción:**
Verifica que la API esté en funcionamiento.

**Respuesta:**

```json
{"status": "ok"}
```


## 5. **Dependencias principales**

`requirements_app.txt` incluye:

```
fastapi
uvicorn
tensorflow
numpy
pydantic
pytest
```


## **Notas**

* Los modelos `.keras` deben estar en las rutas:

  ```
  models/lag_{lag}/mejor_fold_lag_{lag}.keras
  ```
* Si el lag solicitado no existe, la API devolverá un error `404`.
* Todas las predicciones se devuelven como una lista de **7 floats**.


