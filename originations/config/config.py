from pydantic import BaseSettings


class Settings(BaseSettings):
    project_id: str
    client_id: str
    client_x509_cert_url: str

    class Config:
        env_file = ".env"


settings = Settings()
