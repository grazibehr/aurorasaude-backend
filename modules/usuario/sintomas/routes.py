# modules/user_symptoms/routes.py
from flask import jsonify
from flask_openapi3 import APIBlueprint, Tag
from data_base import get_conn
from modules.auth.service import get_user_id
from .schemas import (
    CriarSintomasSchema, AtualizaSintomasSchema,
    SintomasSaidaSchema, ListaSintomasUsuSchema, ListaQuery, DeletaSintomaPath
)
from . import service

usuario_sintomas_tag = Tag(
    name="Sintomas do Usuário",
    description="Registros de sintomas do usuário autenticado"
)

usuario_sintomas = APIBlueprint(
    "usuario_sintomas",
    __name__,
    url_prefix="/usuario/sintoma",
    abp_tags=[usuario_sintomas_tag],
)

# -------- Create --------
@usuario_sintomas.post(
    "/user",
    summary="Adiciona um registro de sintoma do usuário",
    tags=[usuario_sintomas_tag],
    security=[{"BearerAuth": []}],
    responses={201: SintomasSaidaSchema, 401: {"description": "Unauthorized"}, 422: {"description": "Unprocessable Entity"}}
)
def cria_sintoma(body: CriarSintomasSchema):
    user_id = get_user_id()
    if not user_id:
        return {"ok": False, "message": "Unauthorized"}, 401

    try:
        with get_conn() as conn:
            out = service.cria_usuario_sintoma(conn, user_id, body)

        if hasattr(out, "model_dump"):
            out = out.model_dump()

        return out, 201

    except ValueError as e:
        return {"ok": False, "message": str(e)}, 422


# -------- List --------
@usuario_sintomas.get(
    "/lista",
    summary="Lista registros de sintomas do usuário",
    tags=[usuario_sintomas_tag],
    security=[{"BearerAuth": []}],
    responses={200: ListaSintomasUsuSchema, 401: {"description": "Unauthorized"}}
)
def lista_sintomas(query: ListaQuery):
    user_id = get_user_id()
    if not user_id:
        return {"ok": False, "message": "Unauthorized"}, 401

    with get_conn() as conn:
        wrapper = service.lista_usuario_sintomas(conn, user_id, query)
        total = service.conta_usuario_sintomas(conn, user_id, query)

    lst = wrapper.items if hasattr(wrapper, "items") else wrapper

    if lst and hasattr(lst[0], "model_dump"):
        lst = [x.model_dump() for x in lst]
        
    payload = {"items": lst}

    resp = jsonify(payload)
    resp.headers["X-Total-Count"] = str(total)
    return resp, 200


# -------- Delete --------
@usuario_sintomas.delete(
    "/<int:symptom_id>",
    summary="Remove um registro de sintoma do usuário",
    tags=[usuario_sintomas_tag],
    security=[{"BearerAuth": []}],
    responses={
        204: {"description": "Removido"},
        401: {"description": "Unauthorized"},
        404: {"description": "Não encontrado"},
    },
)
def delete_sintomas(path: DeletaSintomaPath):
    user_id = get_user_id()
    if not user_id:
        return {"ok": False, "message": "Unauthorized"}, 401

    symptom_id = path.symptom_id

    try:
        with get_conn() as conn:
            ok = service.deleta_usuario_sintoma(conn, user_id, symptom_id)

        return ("", 204) if ok else ({"ok": False, "message": "Não encontrado"}, 404)

    except LookupError as e:
        return {"ok": False, "message": str(e)}, 404