# SuperKart Frontend Deployment Instructions

## Files in this folder:
- `app.py` - Streamlit web application
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation

## Step-by-Step Deployment to Hugging Face Spaces

### 1. Deploy Backend First
**IMPORTANT:** Deploy the backend API first before deploying the frontend!
- Follow the instructions in `../superkart-backend/DEPLOYMENT_INSTRUCTIONS.md`
- Get your backend URL: `https://YOUR_USERNAME-superkart-sales-api.hf.space`

### 2. Update API URL
Before deploying, update the API URL in `app.py`:
- Open `app.py`
- Find line 20: `API_BASE_URL = "https://YOUR_USERNAME-superkart-sales-api.hf.space"`
- Replace `YOUR_USERNAME` with your actual Hugging Face username

### 3. Create Frontend Space
- Go to https://huggingface.co/spaces
- Click "Create new Space"
- Space name: `superkart-sales-dashboard`
- License: Apache 2.0
- Space SDK: **Streamlit**
- Visibility: Public
- Click "Create Space"

### 4. Upload Files
**Option A: Using Git (Recommended)**
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/superkart-sales-dashboard
cd superkart-sales-dashboard

# Copy all files from this folder
copy * .

git add .
git commit -m "Add SuperKart sales prediction dashboard"
git push
```

**Option B: Using Web Interface**
- Upload all files from this folder to your space
- Make sure the main file is named `app.py`

### 5. Monitor Deployment
- Check the "Logs" tab in your space
- Wait 3-5 minutes for build completion
- Your dashboard will be available at: `https://YOUR_USERNAME-superkart-sales-dashboard.hf.space`

### 6. Test Your Dashboard
1. Visit your dashboard URL
2. Try the "Single Prediction" tab
3. Enter sample data and make a prediction
4. Check the "Batch Predictions" tab
5. Verify all visualizations work

## Features of the Dashboard:
- **🏠 Home**: Overview and key metrics
- **🔮 Single Prediction**: Individual sales predictions
- **📊 Batch Predictions**: Upload CSV for multiple predictions
- **📈 Analytics**: Data visualization and insights
- **ℹ️ About**: Model information and documentation

## Troubleshooting:
- **API connection fails**: Check if backend is deployed and URL is correct
- **CORS errors**: Backend has CORS enabled, should work
- **Streamlit errors**: Check requirements.txt has all dependencies
- **Slow loading**: Backend model is large (61MB), first load may be slow

## Sample Input Data:
```json
{
  "Product_Weight": 15.0,
  "Product_Visibility": 0.05,
  "Product_MRP": 100.0,
  "Store_Establishment_Year": 2000,
  "Product_Sugar_Content": "Low Fat",
  "Product_Type": "Dairy",
  "Store_Size": "Medium",
  "Store_Location_City_Type": "Tier 1",
  "Store_Type": "Supermarket Type1"
}
``` 