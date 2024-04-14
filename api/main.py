import httpx
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from . import crud, models, schemas
from .database import Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ersetze die folgende URL mit deiner tatsächlichen Datenbank-URL
ASYNC_DB_URL = "sqlite+aiosqlite:///./sql_app.db"
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
AsyncSessionLocal = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

app = FastAPI()

origins = [
    "http://localhost:8080",  # Erlaube CORS-Anfragen von diesem Ursprung
    "http://127.0.0.1:8080"   # Wenn dein Browser 127.0.0.1 verwendet, füge auch dies hinzu
]

# Konfiguriere die CORS-Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Erlaube allen Ursprüngen in der Liste
    allow_credentials=True,
    allow_methods=["*"],    # Erlaube alle Methoden
    allow_headers=["*"],    # Erlaube alle Headers
)

# Asynchrone Dependency für Datenbanksessions
async def get_async_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup_event():
    # Erstelle Tabellen asynchron
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_async_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_db)):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/items/", response_model=schemas.Item)
async def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: AsyncSession = Depends(get_async_db)
):
    return await crud.create_user_item(db=db, item=item, user_id=user_id)

@app.get("/items/", response_model=list[schemas.Item])
async def read_items(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_db)):
    items = await crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/events/", response_model=list[schemas.Event])
async def fetch_and_store_events(db: AsyncSession = Depends(get_async_db)):
    url = "https://app.ticketmaster.com/discovery/v2/events"
    params = {
        "apikey": "HYWrCxXKy1pGN4Z5ToGZ6cGmkFAqq2Xh",
        "size": 10,  # Begrenzung auf 10 Events
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    events_data = response.json()
    
    stored_events = []
    for event_data in events_data["_embedded"]["events"]:  # Stelle sicher, dass du den richtigen Pfad verwendest
        event_create = schemas.EventCreate(
            name=event_data["name"],
            date=event_data["dates"]["start"]["localDate"],
            venue=event_data["_embedded"]["venues"][0]["name"],
        )
        stored_event = await crud.create_event(db=db, event=event_create)
        stored_events.append(stored_event)
    return stored_events
