"""
PJECZ Casiopea API OAuth2
"""

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import add_pagination

from .config.settings import Settings, get_settings
from .dependencies.authentications import authenticate_user, encode_token
from .dependencies.database import Session, get_db
from .dependencies.exceptions import MyAnyError
from .routers.autoridades import autoridades
from .routers.cit_categorias import cit_categorias
from .routers.cit_citas import cit_citas
from .routers.cit_clientes import cit_clientes
from .routers.cit_clientes_recuperaciones import cit_clientes_recuperaciones
from .routers.cit_clientes_registros import cit_clientes_registros
from .routers.cit_dias_inhabiles import cit_dias_inhabiles
from .routers.cit_horas_bloqueadas import cit_horas_bloqueadas
from .routers.cit_oficinas_servicios import cit_oficinas_servicios
from .routers.cit_servicios import cit_servicios
from .routers.distritos import distritos
from .routers.domicilios import domicilios
from .routers.materias import materias
from .routers.oficinas import oficinas
from .schemas.cit_clientes import Token

# FastAPI
app = FastAPI(
    title="PJECZ Casiopea API OAuth2",
    description="API OAuth2 del sistema de citas.",
    docs_url="/docs",
    redoc_url=None,
)

# CORSMiddleware
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS.split(","),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Rutas
app.include_router(autoridades, tags=["autoridades"])
app.include_router(cit_categorias, tags=["citas"])
app.include_router(cit_citas, tags=["citas"])
app.include_router(cit_clientes, tags=["citas"])
app.include_router(cit_clientes_recuperaciones, tags=["citas"])
app.include_router(cit_clientes_registros, tags=["citas"])
app.include_router(cit_dias_inhabiles, tags=["citas"])
app.include_router(cit_horas_bloqueadas, tags=["citas"])
app.include_router(cit_oficinas_servicios, tags=["citas"])
app.include_router(cit_servicios, tags=["citas"])
app.include_router(distritos, tags=["autoridades"])
app.include_router(oficinas, tags=["oficinas"])
app.include_router(materias, tags=["autoridades"])
app.include_router(oficinas, tags=["oficinas"])

# Paginación
add_pagination(app)


# Mensaje de Bienvenida
@app.get("/")
async def root():
    """Mensaje de Bienvenida"""
    return {"message": "API OAuth2 del sistema de citas."}


@app.post("/token", response_model=Token)
async def login(
    database: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Login para recibir el formulario OAuth2PasswordRequestForm y entregar el token"""
    try:
        cit_cliente = authenticate_user(username=form_data.username, password=form_data.password, database=database)
    except MyAnyError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(
        access_token=encode_token(settings=settings, cit_cliente=cit_cliente),
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        token_type="bearer",
        username=cit_cliente.username,
    )
