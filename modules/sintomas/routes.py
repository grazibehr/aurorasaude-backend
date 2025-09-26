# modules/symptoms/routes.py
from flask import jsonify
from flask_cors import cross_origin
from flask_openapi3 import APIBlueprint, Tag
from .service import listar_sintomas
from .schemas import SintomaSaidaSchema, SintomasListaSchema

sintomas_tag = Tag(name="Sintomas", description="Lista de sintomas")

sintomas = APIBlueprint(
    "sintomas",
    __name__,
    url_prefix="/sintomas",
    abp_tags=[sintomas_tag],
)

@sintomas.get(
    "/lista",
    tags=[sintomas_tag],
    responses={200: SintomasListaSchema}
)
def catalogo_sintomas():
    items = listar_sintomas()
    return {"items": items}, 200