from typing import Any, Dict, List, Optional
import secrets


from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # SERVER_NAME: str
    # SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:8080"
        ]

    MYSQL_SERVER: str = "localhost:3307"
    MYSQL_USER: str = "dev"
    MYSQL_PASSWRORD: str = "Passw0rd10!"
    MYSQL_DB: str = "fastapi"
    MYSQL_SCHEMA: str = "mysql+pymysql"
    SQLALCHEMY_DATABASE_URL = f"{MYSQL_SCHEMA}://{MYSQL_USER}:{MYSQL_PASSWRORD}@{MYSQL_SERVER}/{MYSQL_DB}"
    # SQLALCHEMY_DATABASE_URL = "mysql+pymysql://dev:Passw0rd10!@localhost:3307/fastapi?charset=utf8mb4"

    # POSTGRES_SERVER: str
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str
    # POSTGRES_DB: str
    # SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    # "postgresql://user:password@postgresserver/db"
    # "mysql+pymysql://test:test123!!@db.database.com/db_name"
    # @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    # def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
    #     if isinstance(v, str):
    #         return v
    #     return PostgresDsn.build(
    #         scheme="postgresql",
    #         user=values.get("POSTGRES_USER"),
    #         password=values.get("POSTGRES_PASSWORD"),
    #         host=values.get("POSTGRES_SERVER"),
    #         path=f"/{values.get('POSTGRES_DB') or ''}",
    #     )

    class Config:
        case_sensitive = True

settings = Settings()