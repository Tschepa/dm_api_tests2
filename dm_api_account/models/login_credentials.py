from pydantic import BaseModel, Field, ConfigDict


class LoginCredentials(BaseModel):
    model_config = ConfigDict(extra='forbid')

    login: str = Field(..., description='Логин')
    password: str = Field(..., description='пароль')
    rememberMe: bool = Field(..., description='Запомнить меня', serialization_alias='rememberMe')