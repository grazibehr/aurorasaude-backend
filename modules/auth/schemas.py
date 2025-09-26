# modules/auth/schemas.py
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class CadastroSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=80, description="Nome completo")
    email: EmailStr = Field(..., description="E-mail válido")
    password: str = Field(..., min_length=6, max_length=128, description="Senha")


class LoginSchema(BaseModel):
    email: EmailStr = Field(..., description="E-mail")
    password: str = Field(..., min_length=6, max_length=128, description="Senha")

class AuthResponseSchema(BaseModel):
    ok: bool = Field(..., description="Status da operação")
    message: str = Field(..., description="Mensagem de retorno")
    token: Optional[str] = Field(description="JWT se houver login/cadastro")