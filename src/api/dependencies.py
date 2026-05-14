import os
from fastapi import Header, HTTPException, status

API_TOKEN = os.getenv("API_TOKEN")


def require_api_token(
    authorization: str | None = Header(
        default=None,
        description="Use: Bearer <API_TOKEN>",
        examples=["Bearer your-secret-token"],
    )
) -> None:
    if not API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API_TOKEN is not configured",
        )

    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )