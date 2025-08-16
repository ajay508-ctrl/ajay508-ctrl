
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global variables for model and preprocessor
model = None
preprocessor = None
feature_names = None

def load_model_and_preprocessor():
    """Load the trained model and preprocessor"""
    global model, preprocessor, feature_names
    
    try:
        # Load model (you'll need to train and save this first)
        if os.path.exists('superkart_model.pkl'):
            model = joblib.load('superkart_model.pkl')
            logger.info("Model loaded successfully")
        else:
            logger.warning("Model file not found. Please train and save the model first.")
            
        # Load preprocessor
        if os.path.exists('superkart_preprocessor.pkl'):
            preprocessor = joblib.load('superkart_preprocessor.pkl')
            logger.info("Preprocessor loaded successfully")
        else:
            logger.warning("Preprocessor file not found.")
            
        # Define feature names (based on SuperKart dataset)
        feature_names = [
            'Product_Weight', 'Product_Sugar_Content', 'Product_Visibility',
            'Product_Type', 'Product_MRP', 'Store_Size', 'Store_Location_Type',
            'Store_Type'
        ]
        
        return True
    except Exception as e:
        logger.error(f"Error loading model/preprocessor: {str(e)}")
        return False

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "message": "SuperKart Sales Prediction API",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": model is not None,
        "preprocessor_loaded": preprocessor is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Make sales prediction"""
    try:
        # Check if model is loaded
        if model is None or preprocessor is None:
            return jsonify({
                "error": "Model or preprocessor not loaded. Please check server logs."
            }), 500
            
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        # Validate required features
        missing_features = [f for f in feature_names if f not in data]
        if missing_features:
            return jsonify({
                "error": f"Missing required features: {missing_features}",
                "required_features": feature_names
            }), 400
            
        # Create DataFrame from input data
        input_df = pd.DataFrame([data])
        
        # Preprocess the data
        processed_data = preprocessor.transform(input_df)
        
        # Make prediction
        prediction = model.predict(processed_data)[0]
        prediction_proba = None
        
        # Get prediction probabilities if available (for classification)
        if hasattr(model, 'predict_proba'):
            prediction_proba = model.predict_proba(processed_data)[0].tolist()
        
        # Prepare response
        response = {
            "prediction": float(prediction),
            "input_data": data,
            "timestamp": datetime.now().isoformat(),
            "model_type": str(type(model).__name__)
        }
        
        if prediction_proba:
            response["prediction_probabilities"] = prediction_proba
            
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

@app.route('/model_info')
def model_info():
    """Get model information"""
    try:
        info = {
            "model_type": str(type(model).__name__) if model else "Not loaded",
            "features": feature_names,
            "model_loaded": model is not None,
            "preprocessor_loaded": preprocessor is not None,
            "timestamp": datetime.now().isoformat()
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/features')
def get_features():
    """Get required features for prediction"""
    return jsonify({
        "required_features": feature_names,
        "feature_descriptions": {
            "Product_Weight": "Weight of the product",
            "Product_Sugar_Content": "Sugar content (Low Fat/Regular)",
            "Product_Visibility": "Product visibility in store",
            "Product_Type": "Type/category of product",
            "Product_MRP": "Maximum Retail Price",
            "Store_Size": "Size of the store (Small/Medium/High)",
            "Store_Location_Type": "Location type (Tier 1/Tier 2/Tier 3)",
            "Store_Type": "Type of store (Grocery Store/Supermarket Type1/etc)"
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Load model and preprocessor on startup
    load_model_and_preprocessor()
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
