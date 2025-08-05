from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from utils.jwt import decode_access_token  # ✅ Corrected import

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)  # ✅ Use correct function
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload.get("sub")  # or return payload if you want full user info
