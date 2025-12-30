from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from qr_model import classify_url

app = FastAPI()

# 🔐 UPDATE THIS BEFORE DEPLOY
origins = [
    "https://quishingdetector.xyz/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UrlRequest(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Quishing backend running"}

@app.post("/predict")
def predict_url(req: UrlRequest):
    url = req.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="URL is empty")

    label_str, raw_pred, proba = classify_url(url)
    backend_label = "phishing" if raw_pred == 1 else "safe"

    return {
        "url": url,
        "label": backend_label,
        "model_label": label_str,
        "score": proba,
    }
