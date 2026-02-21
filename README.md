# Machine Learning Model Deployment Assignment

## Project Overview
This project deploys a pre-trained music genre classifier as a secure REST API.

- Framework: FastAPI
- Artifacts: `music_classifier_pipeline.joblib`, `label_encoder.joblib`
- Inference rule: model is loaded at app startup (no training during requests)
- Security: API key required in `X-API-Key` header

## Repository Files
- `main.py` - API service with model loading and prediction endpoint
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container build definition
- `music_classifier_pipeline.joblib` - Trained model pipeline
- `label_encoder.joblib` - Label encoder for class names

## API Contract

### Health Check
- Method: `GET`
- Path: `/health`
- Response:

```json
{
  "status": "ok"
}
```

### Prediction
- Method: `POST`
- Path: `/predict`
- Header: `X-API-Key: <your_api_key>`
- Body (JSON):

```json
{
  "features": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
}
```

The request must include exactly `57` numeric features.

## Local Run (without Docker)

```bash
pip install -r requirements.txt
```

Set API key environment variable:

PowerShell:

```powershell
$env:API_KEY = "music-producer-key-2026"
uvicorn main:app --host 0.0.0.0 --port 8080
```

Test request:

```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8080/predict" `
  -Headers @{"X-API-Key"="music-producer-key-2026"} `
  -ContentType "application/json" `
  -Body '{"features":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}'
```

## Docker Run

Build image:

```bash
docker build -t music-genre-api .
```

Run container:

```bash
docker run -p 8080:8080 -e API_KEY="music-producer-key-2026" music-genre-api
```

## Cloud Deployment (Google Cloud Run Example)

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/music-genre-api
gcloud run deploy music-genre-api \
  --image gcr.io/YOUR_PROJECT_ID/music-genre-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars API_KEY=music-producer-key-2026
```

Use the returned service URL as your **Live API Endpoint**.

## Evidence for Report (Screenshots Required)
Capture screenshots of:

1. Local API test success (`/predict` response).
2. Docker container running (`docker ps` and logs).
3. Cloud Run deployed service details page.
4. Successful cloud endpoint prediction request.
5. Cloud logs showing received requests.

## Notes for Assignment Compliance
- No model training occurs inside `/predict`.
- Model artifacts are loaded at startup using `joblib.load`.
- Direct API access is used (no Streamlit/Gradio).
- Endpoint secured using API key in request headers.