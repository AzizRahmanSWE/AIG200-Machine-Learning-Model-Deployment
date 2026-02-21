# AIG 200: Machine Learning Model Deployment

## Final Project Report: Music Genre Classifier API

**Name:** Aziz  
**Live API Endpoint:** `[YOUR_API_BASE_URL]/predict`  
**API Key:** `[SET VIA ENVIRONMENT VARIABLE]`  
**GitHub Repository:** [Insert link to your repository]

---

## 1. Executive Summary

This project delivers a scalable machine learning REST API that predicts the musical genre of an audio track from extracted sonic features. The objective was to operationalize an end-to-end machine learning lifecycle from data analysis to live cloud deployment. Using Scikit-Learn, FastAPI, Docker, and AWS, the final API serves real-time predictions securely and reliably, while strictly avoiding model training during inference.

---

## 2. Machine Learning Problem and Dataset

### The Problem

The task is a **multi-class classification** problem: assigning an audio track to one of **10 genre classes** using numerical features (tempo, pitch-related signals, timbre descriptors, and spectral characteristics).

### The Dataset

The model is trained on the **GTZAN Genre Collection** (`features_3_sec.csv` variant), which provides pre-extracted features for 3-second audio slices. Features include:

- MFCC statistics
- Chroma features
- Spectral bandwidth
- Spectral centroid
- Other frequency-domain descriptors

String identifiers such as filename are excluded so the model learns from the **57 numerical input features** only.

---

## 3. Model Development Process

### Preprocessing

Preprocessing is encapsulated in a Scikit-Learn pipeline so transformations are persisted and consistently applied during inference:

- `StandardScaler` for feature normalization
- `LabelEncoder` for mapping genre strings to integer class labels

### Training and Evaluation

Two candidate models were evaluated on an 80/20 train-test split:

1. **Random Forest Classifier** (robust with nonlinear relationships, resistant to overfitting)
2. **Support Vector Machine (RBF kernel)** (effective in high-dimensional spaces)

### Results

- Random Forest Accuracy: **[Insert Colab RF Accuracy]**
- SVM Accuracy: **[Insert Colab SVM Accuracy]**

The best-performing model was serialized as:

- `music_classifier_pipeline.joblib` (model + preprocessing pipeline)
- `label_encoder.joblib` (class label mapping)

---

## 4. Deployment Architecture

The API is deployed using a lightweight containerized AWS architecture:

- **Application Layer (FastAPI):** `main.py` exposes a `POST /predict` endpoint. Model artifacts are loaded once at startup for fast inference-only serving. Access is protected with the `X-API-Key` header.
- **Containerization (Docker):** App code, artifacts, and dependencies are packaged with a minimal `python:3.9-slim` base image.
- **Cloud Registry (Amazon ECR):** Docker image is pushed to a private ECR repository.
- **Compute Host (AWS EC2):** A `t3.micro` Amazon Linux 2023 instance pulls and runs the container, exposing port `8080` via a Security Group.

---

## 5. Challenges Faced

The most significant challenge was cloud infrastructure provisioning tied to billing authorization checks.

- **Challenge:** Early deployment attempts on Google Cloud Run and AWS App Runner were blocked due to billing profile restrictions and authorization hold behavior.
- **Solution:** Deployment architecture pivoted to a manually managed AWS EC2 path. By configuring Docker, IAM permissions for ECR pull, and security rules for port `8080`, the project achieved a stable live endpoint.

---

## 6. Conclusion and Future Improvements

This project successfully bridges local model development and production API serving. The deployed FastAPI container provides secure, low-latency inference from numerical audio descriptors to human-readable genre labels.

### Future Improvements

The current API expects pre-extracted feature vectors. A next iteration will integrate audio feature extraction (e.g., `librosa`) inside the container so users can submit raw `.wav` or `.mp3` files directly. Future responses could include predicted genre, BPM, and key for producer-facing workflows.

---

## API Usage

### Endpoint

- **Method:** `POST`
- **URL:** `[YOUR_API_BASE_URL]/predict`
- **Header:** `X-API-Key: <YOUR_API_KEY>`
- **Body:** JSON with exactly 57 numeric values

```json
{
  "features": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
}
```

### Example cURL Request

```bash
export API_BASE_URL="http://localhost:8080"
export API_KEY="your_api_key_here"

curl -X POST "$API_BASE_URL/predict" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"features":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}'
```

Security note: never commit real API keys, cloud credentials, or private endpoints to source control.

---

## Repository Structure

- `main.py` - FastAPI application and inference endpoint
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container build instructions
- `music_classifier_pipeline.joblib` - Trained pipeline artifact
- `label_encoder.joblib` - Genre label encoder

---

## Assignment Compliance Notes

- No training occurs inside the inference endpoint.
- Artifacts are loaded on startup using `joblib`.
- API is protected with an API key header.
- Deployed as a Dockerized backend service on AWS infrastructure.

---

## Appendix: Deployment Screenshots

Insert the required evidence screenshots here:

1. **FastAPI Swagger UI / Postman Prediction** showing a successful `200 OK` response from `[YOUR_API_BASE_URL]/docs`
2. **AWS ECR Repository** showing the pushed Docker image
3. **AWS EC2 Instance** dashboard showing the running `music-classifier-server`