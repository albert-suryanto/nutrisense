from dotenv import load_dotenv
import os
from src.container import Application
from src.system.fastapi_server_factory import FastApiServerFactory
from src.routers.v1.endpoints import router as router_v1

load_dotenv()

config = {
    "env": os.getenv("APP_ENV"),
    "host": os.getenv("APP_HOST"),
    "port": os.getenv("APP_PORT"),
    "timeout_keep_alive": 60,
}


routers = [router_v1]

server = FastApiServerFactory(config).build(routers)
app = server.get()


application = Application()
application.config.from_yaml("src/config.yml")


@app.get("/")
def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    server.start()
