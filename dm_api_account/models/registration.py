from pydantic import BaseModel, Field, ConfigDict


class Registration(BaseModel):
    #нет лишних полей
    model_config = ConfigDict(extra='forbid')

    #троеточие в скобках=обязательность поля, далее просто описание что за поле if needed
    login: str = Field(..., description='Логин')
    email: str = Field(..., description='Имейл')
    password: str = Field(..., description='пароль')