from flask_openapi3 import APIBlueprint, Tag
from data_base import get_conn
from .schemas import CadastroSchema, LoginSchema, AuthResponseSchema
from .service import gerar_token

auth_tag = Tag(name="Autenticação", description="Autenticação")
auth = APIBlueprint("auth", __name__, url_prefix="/auth", abp_tags=[auth_tag])


@auth.post(
    "/cadastro",
    tags=[auth_tag],
    responses={201: AuthResponseSchema, 409: AuthResponseSchema, 400: AuthResponseSchema},
)
def cadastro(form: CadastroSchema):
    email = form.email.lower()
    pwd = form.password
    try:
        with get_conn() as conn:
            cur = conn.cursor()

            cur.execute("SELECT 1 FROM users WHERE email = ?", (email,))
            if cur.fetchone():
                return {
                    "ok": False,
                    "message": "E-mail já cadastrado.",
                    "token": None,
                    "user": None,
                }, 409

            cur.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (form.name, email, pwd),
            )
            user_id = cur.lastrowid
            conn.commit()

        token = gerar_token(user_id=user_id)

        return {
            "ok": True,
            "message": "Usuário criado com sucesso.",
            "token": token,
            "user": {"id": user_id, "name": form.name, "email": email},
        }, 201

    except Exception:
        return {
            "ok": False,
            "message": "Erro ao criar usuário.",
            "token": None,
            "user": None,
        }, 400


@auth.post(
    "/login",
    tags=[auth_tag],
    responses={200: AuthResponseSchema, 401: AuthResponseSchema, 400: AuthResponseSchema},
)
def login(form: LoginSchema):
    email = form.email.lower()

    try:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, name, email, password FROM users WHERE email = ?",
                (email,),
            )
            row = cur.fetchone()

        if (not row) or (row["password"] != form.password):
            return {
                "ok": False,
                "message": "Credenciais inválidas.",
                "token": None,
                "user": None,
            }, 401

        token = gerar_token(row["id"])
        return {
            "ok": True,
            "message": "Login efetuado.",
            "token": token,
            "user": {
                "name": row["name"],
                "email": row["email"],
            },
        }, 200

    except Exception:
        return {
            "ok": False,
            "message": "Erro ao efetuar login.",
            "token": None,
            "user": None,
        }, 400
