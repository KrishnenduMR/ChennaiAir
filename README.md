# ChennaiAir: AQI Forecasting System
An automated air quality forecasting system for
Chennai is developed by integrating time series modeling with
real-time data acquisition. Historical pollutant concentrations—
PM2.5, PM10, CO, NO2, and SO2—obtained from the Central
The Pollution Control Board (CPCB) serves as the foundation for
model training. A Seasonal Autoregressive Integrated Moving Average
model (SARIMA) is employed, selected after extensive hyperparameter
tuning for its superior performance over baseline
models. The model is trained on Air Quality Index (AQI) values
computed using CPCB’s sub-index methodology and is retrained
daily to adapt to evolving pollution trends. After optimization,
the SARIMA model achieves a Mean Absolute Percentage Error
(MAPE) of 13.57%, demonstrating strong predictive accuracy.
The system features real-time API integration for continuous data
ingestion and automated scheduling for data collection, model
retraining, and forecast generation, thereby requiring minimal
manual intervention. This scalable and adaptive framework
supports short-term air quality forecasting, enabling proactive
environmental management and informed public health decision-making.
