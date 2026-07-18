from pydantic import BaseModel, Field, ConfigDict

class ChangePassword(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: str = Field(..., description='User login')
    token: str = Field(..., description='Password reset token')
    oldPassword: str = Field(..., description='Old password')
    newPassword: str = Field(..., description='New password')