from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials

# Import routers once created
from routers import ai, auth, dropshipping

# Load environment variables
load_dotenv()

# Initialize FastAPI App
app = FastAPI(
    title="OllamaDrop.AI Backend",
    description="Backend API for AI-powered Dropshipping Platform",
    version="1.0.0"
)

# Setup CORS (Allowing frontend cross-origin requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase Admin SDK (Commented until credentials are provided by the user)
def init_firebase():
    firebase_cert_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
    try:
        if firebase_cert_path and os.path.exists(firebase_cert_path):
            cred = credentials.Certificate(firebase_cert_path)
            firebase_admin.initialize_app(cred)
            print("🚀 Firebase Admin initialized successfully.")
        else:
            print("⚠️ Firebase Admin credentials not found. Authentication features will fail.")
    except Exception as e:
        print(f"❌ Failed to initialize Firebase: {e}")

init_firebase()

# Include Routers
app.include_router(ai.router, prefix="/api/ai", tags=["AI Integration"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(dropshipping.router, prefix="/api/dropshipping", tags=["Dropshipping Management"])

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "OllamaDrop.AI Backend",
        "firebase_active": bool(firebase_admin._apps)
    }

# Entry point for local debugging
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
