from dotenv import load_dotenv
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security.api_key import APIKeyHeader
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED
import os
import secrets

load_dotenv()

API_KEY = os.getenv("API_KEY")
exlcude_paths = ["/", "/openapi.json", "/docs"]


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, api_key_header: APIKeyHeader):
        super().__init__(app)
        self.api_key_header = api_key_header

    async def dispatch(self, request: Request, call_next):
        api_key_value = request.headers.get(self.api_key_header.model.name)

        if request.url.path not in exlcude_paths:
            if not api_key_value:
                return JSONResponse(
                    status_code=HTTP_401_UNAUTHORIZED,
                    content={"error": "API key header is missing"},
                )

            elif api_key_value != API_KEY:
                return JSONResponse(
                    status_code=HTTP_401_UNAUTHORIZED,
                    content={"error": "Invalid API key"},
                )

        response = await call_next(request)
        return response


def generate_secret_key():
    return secrets.token_urlsafe(32)
