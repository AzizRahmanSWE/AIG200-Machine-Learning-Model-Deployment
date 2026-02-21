import os
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import numpy as np
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field


EXPECTED_FEATURE_COUNT = 57
API_KEY_ENV = "API_KEY"
MODEL_FILE = Path("music_classifier_pipeline.joblib")
ENCODER_FILE = Path("label_encoder.joblib")


class AudioFeatures(BaseModel):
    features: list[float] = Field(
        ...,
        min_length=EXPECTED_FEATURE_COUNT,
        max_length=EXPECTED_FEATURE_COUNT,
        description=f"Exactly {EXPECTED_FEATURE_COUNT} numeric audio features.",
    )


def get_api_key(api_key_header_value: str = Security(APIKeyHeader(name="X-API-Key"))) -> str:
    expected_api_key = os.getenv(API_KEY_ENV)
    if not expected_api_key:
        raise HTTPException(
            status_code=500,
            detail=f"Missing {API_KEY_ENV} environment variable on server.",
        )

    if api_key_header_value != expected_api_key:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

    return api_key_header_value


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not MODEL_FILE.exists() or not ENCODER_FILE.exists():
        raise RuntimeError(
            "Model artifacts are missing. Expected files: "
            f"{MODEL_FILE.name}, {ENCODER_FILE.name}"
        )

    app.state.pipeline = joblib.load(MODEL_FILE)
    app.state.encoder = joblib.load(ENCODER_FILE)
    yield


app = FastAPI(title="Music Genre Classifier API", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict")
def predict_genre(data: AudioFeatures, _: str = Depends(get_api_key)) -> dict[str, str]:
    try:
        input_data = np.array(data.features, dtype=float).reshape(1, -1)
        prediction_encoded = app.state.pipeline.predict(input_data)
        genre = app.state.encoder.inverse_transform(prediction_encoded)[0]
        return {"predicted_genre": str(genre)}
    except Exception as error:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {error}") from error