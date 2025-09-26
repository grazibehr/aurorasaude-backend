from pydantic import BaseModel, Field
from typing import List

class SintomaSaidaSchema(BaseModel):
    id: int = Field(..., description="ID do sintoma")
    type: str = Field(..., description="Nome do sintoma")

class SintomasListaSchema(BaseModel):
    items: List[SintomaSaidaSchema] = Field(..., description="Lista de sintomas disponíveis")
