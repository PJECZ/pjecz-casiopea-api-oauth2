"""
PJECZ Casiopea API OAuth2
"""

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import add_pagination

from .dependencies.authentications import TOKEN_EXPIRES_SECONDS, authenticate_user, encode_token
from .dependencies.database import Session, get_db
from .dependencies.exceptions import MyAnyError
from .schemas.cit_clientes import Token
from .settings import Settings, get_settings

# FastAPI
app = FastAPI(
    title="PJECZ Citas Cliente API OAuth2",
    description="API del sistema de citas para la interfaz del cliente.",
    docs_url="/docs",
    redoc_url=None,
)

# CORSMiddleware
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins.split(","),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Paginación
add_pagination(app)


# Mensaje de Bienvenida
@app.get("/")
async def root():
    """Mensaje de Bienvenida"""
    return {"message": "API con autentificación para realizar operaciones con la base de datos del sistema de citas."}


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
        expires_in=TOKEN_EXPIRES_SECONDS,
        token_type="bearer",
        username=cit_cliente.username,
    )
