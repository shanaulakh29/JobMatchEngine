from fastapi import Header, HTTPException, status

def get_user_id(user_id: str = Header(...)) -> str:
    """Extracts the user_ID from header. Used as a dependency"""
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID required")
    return user_id