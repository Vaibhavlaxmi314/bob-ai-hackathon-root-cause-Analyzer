import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from database import init_db
from routers.api import router

app = FastAPI(
    title="Supply Chain Disruption Assistant",
    description="AI-powered supply chain disruption detection, rerouting, fleet optimisation and cold chain monitoring.",
    version="1.0.0",
)

_raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")
_allow_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allow_origins,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    allow_credentials=True,
)


app.include_router(router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok", "service": "supply-chain-disruption-assistant"}
