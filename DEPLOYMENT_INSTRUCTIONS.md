# SuperKart Backend Deployment Instructions

## Files in this folder:
- `flask_app.py` - Flask API application
- `best_superkart_model.pkl` - Trained Random Forest model (61MB)
- `superkart_preprocessor.pkl` - Data preprocessing pipeline
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker configuration for Hugging Face
- `README.md` - Project documentation

## Step-by-Step Deployment to Hugging Face Spaces

### 1. Create Hugging Face Account
- Go to https://huggingface.co and sign up/login
- Go to Settings → Access Tokens
- Create a new token with "Write" permissions
- Save this token securely

### 2. Create New Space
- Go to https://huggingface.co/spaces
- Click "Create new Space"
- Space name: `superkart-sales-api`
- License: Apache 2.0
- Space SDK: **Docker**
- Visibility: Public
- Click "Create Space"

### 3. Upload Files
**Option A: Using Git (Recommended)**
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/superkart-sales-api
cd superkart-sales-api

# Copy all files from this folder
copy * .

git add .
git commit -m "Add SuperKart sales prediction API"
git push
```

**Option B: Using Web Interface**
- Upload all files from this folder to your space
- Use the web interface at your space URL

### 4. Monitor Deployment
- Check the "Logs" tab in your space
- Wait 5-10 minutes for build completion
- Your API will be available at: `https://YOUR_USERNAME-superkart-sales-api.hf.space`

### 5. Test Your API
```bash
curl -X GET https://YOUR_USERNAME-superkart-sales-api.hf.space/health

curl -X POST https://YOUR_USERNAME-superkart-sales-api.hf.space/predict \
  -H "Content-Type: application/json" \
  -d '{"Product_Weight": 15.0, "Product_Visibility": 0.05, "Product_MRP": 100.0, "Store_Establishment_Year": 2000, "Product_Sugar_Content": "Low Fat", "Product_Type": "Dairy", "Store_Size": "Medium", "Store_Location_City_Type": "Tier 1", "Store_Type": "Supermarket Type1"}'
```

## Important Notes:
- The model file is 61MB, so upload may take time
- Hugging Face uses port 7860 (configured in Dockerfile)
- CORS is enabled for frontend integration
- API endpoints: `/health`, `/predict`, `/model_info` 