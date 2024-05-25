from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.security.api_key import APIKeyHeader

from src.system.fastapi_server import FastApiServer
from src.system.middleware.authorization import AuthMiddleware
from src.system.middleware.exception_handler import (
    error_handler,
    http_exception_handler,
    request_validation_exception_handler,
)
from src.system.middleware.process_time import ProcessTimeMiddleware


class FastApiServerFactory:
    def __init__(self, config, title="Template API"):
        self.app = FastAPI(title=title, root_path="", openapi_url="/openapi.json")
        self.config = config

        self.api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=True)

        self.add_middleware()

    def add_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE"],
            allow_headers=["Content-Type", "X-Process-Time"],
        )

        self.app.add_middleware(AuthMiddleware, api_key_header=self.api_key_header)
        self.app.add_middleware(ProcessTimeMiddleware)

        self.app.add_exception_handler(
            RequestValidationError, request_validation_exception_handler
        )
        self.app.add_exception_handler(HTTPException, http_exception_handler)
        self.app.add_exception_handler(Exception, error_handler)

    def create_openapi_schema(self):
        openapi_schema = get_openapi(
            title=self.app.title,
            version=self.app.version,
            description=self.app.description,
            routes=self.app.routes,
        )
        openapi_schema["components"]["securitySchemes"] = {
            self.api_key_header.model.name: {
                "type": "apiKey",
                "in": "header",
                "name": self.api_key_header.model.name,
            }
        }
        openapi_schema["security"] = [{"X-API-KEY": []}]

        return openapi_schema

    def build(self, routers):
        for router in routers:
            self.app.include_router(router)

        self.app.openapi_schema = self.create_openapi_schema()

        return FastApiServer(self.app, self.config)
