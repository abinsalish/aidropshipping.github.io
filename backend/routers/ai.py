from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import httpx
import os
from typing import Optional

router = APIRouter()

# For Cloud Ollama or other Llama-compatible API (e.g., Groq, Together)
CLOUD_API_URL = os.getenv("OLLAMA_CLOUD_PREFIX", "https://api.groq.com/openai/v1/chat/completions")
API_KEY = os.getenv("CLOUD_LLM_API_KEY", "")

class InsightRequest(BaseModel):
    store_data: dict
    prompt: Optional[str] = "Analyze my store's recent performance and provide dropshipping strategies."

@router.post("/insights")
async def generate_dropshipping_insights(req: InsightRequest):
    """
    Connects to the cloud LLM using OpenAI-compatible endpoints 
    (Supported by Groq, Together, and hosted Ollama via Ollama API).
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="CLOUD_LLM_API_KEY is missing from environment.")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192", # Example model name for Groq, adjust if using raw cloud Ollama
        "messages": [
            {
                "role": "system",
                "content": "You are a senior e-commerce dropshipping expert. Analyze the provided store data and suggest data-driven optimizations for products and pricing."
            },
            {
                "role": "user",
                "content": f"{req.prompt}\n\nStore Data: {req.store_data}"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(CLOUD_API_URL, headers=headers, json=payload, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            
            # Extract content (OpenAI compatible format)
            ai_message = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            return {
                "success": True,
                "insights": ai_message,
                "model_used": payload["model"]
            }
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"LLM API Error: {e.response.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
