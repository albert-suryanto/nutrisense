from fastapi import FastAPI
from typing import TypedDict
from typing_extensions import NotRequired
import uvicorn


class Config(TypedDict):
    host: NotRequired[str]
    port: NotRequired[int]
    env: str


class FastApiServer:
    def __init__(self, app: FastAPI, config: Config):
        self.app = app
        self.config = config

    def start(self):
        if self.config.get("host"):
            host = self.config["host"]
        else:
            if self.config["env"] == "staging":
                # Staging Kubernetes cluster is using IPv6
                host = "::"
            else:
                host = "127.0.0.1"

        port = int(self.config["port"]) if self.config.get("port") is not None else 8080
        log_level = (
            "debug"
            if (self.config["env"] == "development" or self.config["env"] == "test")
            else "info"
        )

        timeout_keep_alive = self.config.get("timeout_keep_alive") or 60

        uvicorn.run(
            self.app,
            host=host,
            port=port,
            log_level=log_level,
            timeout_keep_alive=timeout_keep_alive,
        )

    def get(self):
        return self.app
