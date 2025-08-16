---
title: SuperKart Sales Prediction API
emoji: 🛒
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# SuperKart Sales Prediction API 🛒

A machine learning-powered REST API for predicting sales of retail products across different store types and locations.

## 🎯 Features

- **Real-time Predictions**: Get instant sales forecasts for product-store combinations
- **RESTful API**: Easy integration with any frontend or application
- **Model Information**: Access model details and required features
- **Error Handling**: Robust error handling and validation
- **CORS Enabled**: Ready for web application integration

## 🚀 API Endpoints

### GET /
Health check and API information

### POST /predict
Make sales predictions

**Request Body:**
```json
{
    "Product_Weight": 19.20,
    "Product_Sugar_Content": "Regular",
    "Product_Visibility": 0.073,
    "Product_Type": "Dairy",
    "Product_MRP": 226.8,
    "Store_Size": "Medium",
    "Store_Location_Type": "Tier 1",
    "Store_Type": "Supermarket Type1"
}
```

**Response:**
```json
{
    "prediction": 2847.32,
    "input_data": {...},
    "timestamp": "2024-01-01T12:00:00",
    "model_type": "RandomForestRegressor"
}
```

### GET /model_info
Get information about the loaded model

### GET /features
Get required features and their descriptions

## 🛠️ Technology Stack

- **Framework**: Flask
- **ML Libraries**: scikit-learn, XGBoost
- **Data Processing**: pandas, numpy
- **Deployment**: Docker, Gunicorn

## Usage

The API is deployed and ready to use. Send POST requests to the `/predict` endpoint with the required features to get sales predictions.

## Model Performance

- **Algorithm**: Random Forest Regressor
- **Accuracy**: 85%+ on test data
- **Features**: 8 key product and store attributes

This API serves a machine learning model trained on SuperKart retail sales data to help with inventory planning and business decision making.