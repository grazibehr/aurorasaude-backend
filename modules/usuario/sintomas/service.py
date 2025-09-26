from datetime import date as _date
from . import repository as repo
from .schemas import (
    CriarSintomasSchema, AtualizaSintomasSchema,
    SintomasSaidaSchema, ListaSintomasUsuSchema, ListaQuery
)

# -------- Create --------
def cria_usuario_sintoma(conn, user_id: int, body: CriarSintomasSchema) -> SintomasSaidaSchema:
    if not user_id:
        raise PermissionError("Unauthorized")

    if not repo.existe_sintoma(conn, body.symptom_id):
        raise ValueError("symptom_id inválido")

    d = body.date or _date.today().isoformat()

    new_id = repo.insere_usuario_sintoma(
        conn, user_id, body.symptom_id, int(body.pain_level), d, body.notes
    )

    row = repo.busca_usuario_sintoma_por_id(conn, user_id, new_id)  # -> dict esperado
    if not row:
        raise LookupError("Falha ao recuperar o registro recém-criado.")

    return SintomasSaidaSchema(**row)

# -------- List --------
def lista_usuario_sintomas(conn, user_id: int, query: ListaQuery) -> ListaSintomasUsuSchema:
    rows = repo.lista_usuario_sintomas(conn, user_id, query)  # -> list[dict]
    items = [SintomasSaidaSchema(**r) for r in rows]
    return ListaSintomasUsuSchema(items=items)

def conta_usuario_sintomas(conn, user_id: int, query: ListaQuery) -> int:
    return repo.conta_usuario_sintomas(conn, user_id, query)

# -------- Update --------
def atualiza_usuario_sintoma(conn, user_id: int, record_id: int, body: AtualizaSintomasSchema) -> SintomasSaidaSchema:
    if not user_id:
        raise PermissionError("Unauthorized")

    sets = {}
    if body.pain_level is not None:
        sets["pain_level"] = int(body.pain_level)
    if body.date is not None:
        sets["date"] = body.date
    if body.notes is not None:
        sets["notes"] = body.notes

    ok = repo.update_user_symptom(conn, user_id, record_id, sets)
    if not ok:
        raise LookupError("Registro não encontrado ou não pertence ao usuário")

    row = repo.get_user_symptom_by_id(conn, user_id, record_id)  # -> dict
    return SintomasSaidaSchema(**row)
    
def deleta_usuario_sintoma(conn, user_id: int, symptom_id: int) -> bool:
    if not user_id:
        raise PermissionError("Unauthorized")

    ok = repo.deleta_usuario_sintoma(conn, user_id, symptom_id)
    if not ok:
        raise LookupError("Registro não encontrado ou não pertence ao usuário")

    return ok