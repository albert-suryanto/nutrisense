import os
import dotenv

dotenv.load_dotenv()


def get_int_env(key: str, default: int) -> int:
    value = os.getenv(key)
    if value is None or value == "":
        return default

    try:
        return int(value)
    except Exception:
        return default


def get_float_env(key: str, default: float) -> float:
    value = os.getenv(key)
    if value is None or value == "":
        return default

    try:
        return float(value)
    except Exception:
        return default


NUTRISENSE_DATABASES__DATABASE = os.getenv("NUTRISENSE_DATABASES__DATABASE")
NUTRISENSE_DATABASES__HOST = os.getenv("NUTRISENSE_DATABASES__HOST")
NUTRISENSE_DATABASES__PASSWORD = os.getenv("NUTRISENSE_DATABASES__PASSWORD")
NUTRISENSE_DATABASES__PORT = os.getenv("NUTRISENSE_DATABASES__PORT")
NUTRISENSE_DATABASES__USER = os.getenv("NUTRISENSE_DATABASES__USER")

DATABASE_URL = "postgresql://{}:{}@{}:{}/{}?sslmode=require".format(
    NUTRISENSE_DATABASES__USER,
    NUTRISENSE_DATABASES__PASSWORD,
    NUTRISENSE_DATABASES__HOST,
    NUTRISENSE_DATABASES__PORT,
    NUTRISENSE_DATABASES__DATABASE,
)
