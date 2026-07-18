from pydantic import BaseModel, Field, ConfigDict

class Registration(BaseModel):
    model_config = ConfigDict(extra='forbid')
    # упадем на валидации алиаса, тк поле передается с другим ключом login: str = Field(..., description='Логин', alias='username')
    login: str = Field(..., description='Логин')
    password: str = Field(..., description='Пароль')
    email: str = Field(..., description='Имейл')