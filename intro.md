# ***Predicción del Precio de Cierre/Volatilidad del BitCoin***

El presente proyecto tiene como objetivo analizar y modelar la dinámica temporal del precio de cierre diario y la volatilidad del Bitcoin, utilizando herramientas  de aprendizaje automático. A partir de los datos históricos entre 2018 y 2025, se busca comprender el comportamiento de los precios, su volatilidad y la estructura de dependencia temporal, con el fin de desarrollar un modelo capaz de predecir el precio o la volatilidad futura del activo.

Bitcoin, al ser un activo financiero altamente volátil, presenta patrones complejos que dificultan la predicción directa de su precio. Por ello, este estudio aborda tanto la exploración descriptiva de la serie temporal (EDA) como el diseño de un modelo predictivo basado en técnicas de deep learning, evaluando su rendimiento mediante estrategias de validación cruzada temporal (TimeSeries Cross-Validation).

## **Objetivo**

Desarrollar un modelo predictivo para el precio de cierre diario/volatilidad del Bitcoin, empleando su histórico temporal y técnicas de ingeniería de características basadas en retardos (*lags*) y horizontes de predicción (*targets*).



## **Alcance del análisis**

El proyecto se estructura en tres grandes etapas:
1. **Análisis exploratorio de datos (EDA):** donde se examinan las propiedades estadísticas del precio del Bitcoin, los patrones de volatilidad y la estructura de correlaciones.
2. **Modelado predictivo:** en el cual se construye un modelo supervisado con validación temporal, diseñado para anticipar los movimientos futuros del precio.
3. **Análisis de Resultados:** donde se presentan los hallazgos obtenidos a partir de las simulaciones y pruebas del modelo.  
En esta etapa se muestran las **gráficas comparativas entre los valores reales y las predicciones**, tanto en los conjuntos de entrenamiento, validación y prueba, así como la **evaluación cuantitativa** del desempeño mediante métricas como **MAE, RMSE, MAPE y MSE**.  
Además, se incluye una **comparación entre diferentes configuraciones de tamaño de ventana (lags)** para determinar cuál ofrece la mejor capacidad predictiva.  

Se busca interpretar de manera visual y numérica los resultados, identificando patrones de error, estabilidad entre folds y el comportamiento del modelo frente a distintos horizontes de predicción. De esta forma, se evalúa la capacidad del modelo para generalizar y su utilidad práctica en la estimación del comportamiento futuro del precio del Bitcoin. Este enfoque busca no solo realizar una predicción puntual, sino también ofrecer una comprensión más profunda de la naturaleza no lineal del mercado de criptomonedas.

- **Periodo de análisis:** 2018–2025  
- **Activo estudiado:** Bitcoin (BTC/USD) 
- **Técnica principal:** Redes neuronales MLP con validación cruzada temporal
