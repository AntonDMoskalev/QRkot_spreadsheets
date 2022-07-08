from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    The default values are set to demonstrate the project,
    in case of deployment, write the value of the variables in .env.
    """
    app_title: str = 'Кошачий благотворительный фонд'
    app_description: str = 'Сервис для поддержки котиков!'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'CheshireСat'
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()