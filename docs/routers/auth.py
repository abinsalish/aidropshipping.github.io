from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
import os

router = APIRouter()
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verifies the Firebase JWT token."""
    token = credentials.credentials
    try:
        if not hasattr(auth, 'verify_id_token'):
            # Fallback if firebase is not fully loaded due to no credentials
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Firebase Admin not initialized on Server"
            )
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me")
async def get_my_profile(user: dict = Depends(get_current_user)):
    """Returns the authenticated user's profile."""
    return {"user_id": user.get("uid"), "email": user.get("email"), "name": user.get("name")}
