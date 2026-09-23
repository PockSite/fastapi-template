# PockSite FastAPI Template

Plantilla base para microservicios FastAPI de PockSite. Trae una arquitectura por
capas (router → service → repository → model), un repositorio genérico con manejo de
errores, CORS, logging y soporte tanto para SQLite (desarrollo) como Postgres/Supabase
(producción). Incluye un CRUD de `users` completo como ejemplo de referencia.

## Arquitectura

```
app/
├── main.py                 # App FastAPI: lifespan, CORS, logging, exception handlers
├── api/v1/
│   ├── router.py           # Agrega todos los routers bajo /api/v1
│   └── users.py            # Endpoints del recurso (ejemplo CRUD)
├── core/
│   ├── config.py           # Carga y valida variables de entorno
│   ├── database.py         # Engine SQLAlchemy, SessionLocal, Base, get_db()
│   ├── dependencies.py     # Inyección de dependencias (arma service + repository)
│   └── security.py         # Utilidad opcional para verificar JWT
├── client/
│   └── client.py           # BaseExternalClient (httpx) para llamar otras APIs
├── models/user.py          # Modelos SQLAlchemy
├── schemas/user.py         # Esquemas Pydantic (request/response)
├── repository/
│   ├── repository.py       # Repository[T, K] genérico (CRUD + IntegrityError → 409)
│   └── users_repository.py # Repositorio concreto del recurso
└── service/user_service.py # Lógica de negocio
```

**Flujo de una petición:** `router` recibe la request y valida con el *schema* →
inyecta el *service* vía `Depends` → el *service* aplica la lógica de negocio →
delega la persistencia en el *repository* → el *repository* opera sobre el *model*.

## Configuración

Copia `.env.example` a `.env` y ajusta los valores:

```bash
cp .env.example .env
```

| Variable | Descripción |
|---|---|
| `APP_NAME` | Título de la API (aparece en Swagger). |
| `PRODUCTION` | `true` \| `false`. En `true` se oculta `/api/docs` y el logging sube a `INFO`. |
| `DB_URL` | **Requerida.** `sqlite:///:memory:` para dev, o URL Postgres/Supabase. |
| `CORS_ORIGINS` | Orígenes permitidos separados por coma, sin espacios. |
| `SECRET_KEY`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS` | Opcionales; solo si usas `app/core/security.py`. |

> `DB_URL` es obligatoria: la app falla al arrancar si no está definida.
> Con SQLite se usa `StaticPool`; con Postgres se usa `NullPool` + `pool_pre_ping`
> (recomendado detrás de pgbouncer/Supabase).

## Ejecutar

```bash
python -m venv venv
venv\Scripts\activate        # Windows  (source venv/bin/activate en Linux/Mac)
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

- API: http://localhost:8001/api/v1
- Swagger: http://localhost:8001/api/docs  (deshabilitado si `PRODUCTION=true`)

## Docker

```bash
docker build -t pocksite-api .
docker run --env-file .env -p 8001:8000 pocksite-api
```

El contenedor expone el puerto **8000**.

## Cómo agregar un recurso nuevo

Replica el patrón del recurso `users` (por ejemplo, para `products`):

1. **Model** — `app/models/product.py`: define la tabla heredando de `Base`.
2. **Schema** — `app/schemas/product.py`: `ProductRequest` (entrada) y
   `ProductResponse` (salida, con `class Config: from_attributes = True`).
3. **Repository** — `app/repository/products_repository.py`:
   `class ProductsRepository(Repository[Product, int])` y añade consultas propias.
4. **Service** — `app/service/product_service.py`: lógica de negocio sobre el repo.
5. **Dependency** — en `app/core/dependencies.py`: `get_product_service(db=Depends(get_db))`.
6. **Router** — `app/api/v1/products.py`: los endpoints, y regístralo en
   `app/api/v1/router.py` con `router.include_router(products.router, prefix="/products", tags=["Products"])`.
7. **Registro del modelo** — importa el módulo del modelo en `app/main.py`
   (`import app.models.product`) para que `Base.metadata.create_all` lo cree.

## Repositorio genérico

`Repository[T, K]` (`T` = modelo, `K` = tipo de la PK) ofrece `create`, `read_all`,
`read_by_id`, `update` y `delete`. Las violaciones de integridad (`IntegrityError`)
se traducen automáticamente a un `409 Conflict`, y el `get_db` traduce fallos de
conexión a `503 Service Unavailable`.

## Llamar a otras APIs

`app/client/client.py` expone `BaseExternalClient` (httpx asíncrono) que agrega el
header `Authorization: Bearer <api_key>` y traduce errores del servicio externo a
`HTTPException`. Extiéndelo por cada servicio destino y pásale su URL base desde
`config.py`.

## Seguridad (opcional)

`app/core/security.py` provee `verify_access_token(token)` para validar JWT firmados
con `SECRET_KEY`/`JWT_ALGORITHM`. Úsalo con `OAuth2PasswordBearer` en los endpoints
que requieran autenticación.
