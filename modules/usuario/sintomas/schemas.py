from typing import Optional, List, Literal
from typing_extensions import Annotated
from pydantic import BaseModel, Field, conint

PainLevel = conint(ge=1, le=10)
DateStr = Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}$", description="YYYY-MM-DD")]
OrderOpt = Literal["date_desc", "date_asc", "id_desc", "id_asc"]

class CriarSintomasSchema(BaseModel):
    symptom_id: int = Field(..., description="ID do sintoma (catálogo)")
    pain_level: PainLevel = Field(..., description="Nível de dor (1-10)")
    date: Optional[DateStr] = Field(
        default=None,
        description="YYYY-MM-DD; se ausente, usa a data de hoje"
    )
    notes: Optional[str] = Field(default=None, description="Observações livres")

class AtualizaSintomasSchema(BaseModel):
    pain_level: Optional[PainLevel] = Field(None, description="Nível de dor (1-10)")
    date: Optional[DateStr] = Field(None, description="YYYY-MM-DD")
    notes: Optional[str] = Field(None, description="Observações livres")

class DeletaSintomaPath(BaseModel):
    symptom_id: int = Field(..., ge=1, description="ID do registro de sintoma do usuário")
    
class SintomasSaidaSchema(BaseModel):
    id: int = Field(..., description="ID do registro do usuário")
    user_id: int = Field(..., description="ID do usuário dono do registro")
    symptom_id: int = Field(..., description="ID do sintoma (catálogo)")
    symptom_name: str = Field(..., description="Nome do sintoma (usado no front)")
    pain_level: PainLevel = Field(..., description="Nível de dor (1-10)")
    date: DateStr
    notes: Optional[str] = Field(None, description="Observações")

class ListaSintomasUsuSchema(BaseModel):
    items: List[SintomasSaidaSchema] = Field(..., description="Lista de registros")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "items": [
                        {
                            "id": 101,
                            "user_id": 1,
                            "symptom_id": 2,
                            "symptom_name": "Dor de cabeça",
                            "pain_level": 7,
                            "date": "2025-09-22",
                            "notes": "Piorou de noite"
                        }
                    ]
                }
            ]
        }
    }

class ListaQuery(BaseModel):
    date_from: Optional[DateStr] = Field(None, alias="date_ini", description="Início (YYYY-MM-DD)")
    date_to:   Optional[DateStr] = Field(None, alias="date_fim", description="Fim (YYYY-MM-DD)")
    symptom_id: Optional[int] = Field(None, description="Filtra por sintoma específico")
    min_pain: Optional[PainLevel] = Field(None, description="Filtra por dor mínima (>=)")
    max_pain: Optional[PainLevel] = Field(None, description="Filtra por dor máxima (<=)")
    order: OrderOpt = Field("date_desc", description="date_desc|date_asc|id_desc|id_asc")
    page: int = Field(1, ge=1, description="Página (>=1)")
    page_size: int = Field(20, ge=1, le=100, description="Itens por página (1-100)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "date_ini": "2025-09-01",
                    "date_fim": "2025-09-22",
                    "symptom_id": 2,
                    "min_pain": 3,
                    "max_pain": 9,
                    "order": "date_desc",
                    "page": 1,
                    "page_size": 20
                }
            ]
        }
    }