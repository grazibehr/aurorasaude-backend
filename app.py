from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info
from flask_openapi3.models import SecurityScheme

from data_base import init_database
from modules.auth import auth
from modules.sintomas import sintomas
from modules.usuario.sintomas import usuario_sintomas

info = Info(title="Aurora Saúde – API", version="1.0.0")
app = OpenAPI(
     __name__, 
     info=info,
      security_schemes={
        "BearerAuth": SecurityScheme(
            type="http",
            scheme="bearer",
            bearerFormat="JWT"
        )
    })

CORS(app)

app.register_api(auth)
app.register_api(sintomas)
app.register_api(usuario_sintomas)