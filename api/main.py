import httpx
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from typing import AsyncGenerator

from .src import crud, models
from .src import schemas
from .src.database import Base
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .src.crud import verify_password, get_password_hash, pwd_context, get_user_by_email
from .src.schemas import UserAuthenticate

# Ersetze die folgende URL mit deiner tatsächlichen Datenbank-URL
ASYNC_DB_URL = "sqlite+aiosqlite:///./sql_app.db"
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
AsyncSessionLocal = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

# Konfiguriere die CORS-Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],  # Liste der Ursprünge, die erlaubt sind
    allow_credentials=True,
    allow_methods=["*"],  # Erlaube alle Methoden
    allow_headers=["*"],  # Erlaube alle Header
)

# Asynchrone Dependency für Datenbanksessions
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup_event():
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
async def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: AsyncSession = Depends(get_async_db)):
    return await crud.create_user_item(db=db, item=item, user_id=user_id)

@app.get("/items/", response_model=list[schemas.Item])
async def read_items(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_db)):
    items = await crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/events/", response_model=list[schemas.Event])
async def fetch_and_store_events(country: str = Query(None, description="Country code, e.g., 'US', 'DE'"), db: AsyncSession = Depends(get_async_db)):
    if not country:
        return []  # oder eine andere angemessene Antwort
    current_date = datetime.now()
    end_date = current_date + timedelta(days=180)

    url = "https://app.ticketmaster.com/discovery/v2/events"
    params = {
        "apikey": "HYWrCxXKy1pGN4Z5ToGZ6cGmkFAqq2Xh",
        "size": 30,
        "countryCode": country,
        "startDateTime": current_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "endDateTime": end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    events_data = response.json()
    print(events_data)  # Log the response data

    stored_events = []
    if "_embedded" in events_data:
        for event_data in events_data["_embedded"]["events"]:
            event_create = schemas.EventCreate(
                name=event_data["name"],
                date=event_data["dates"]["start"]["localDate"],
                venue=event_data["_embedded"]["venues"][0].get("name", "Unknown Venue"),
                country=country,
                url=event_data["url"]  # URL des Events hinzufügen
            )
            stored_event = await crud.create_event(db=db, event=event_create)
            stored_events.append(stored_event)
    return stored_events




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(user_credentials: UserAuthenticate, db: AsyncSession = Depends(get_async_db)):
    db_user = await get_user_by_email(db, email=user_credentials.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user_credentials.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return {"access_token": db_user.email, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_db)):
    user = await crud.get_user_by_email(db, email=current_user)
    return user

@app.post("/users/")
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_async_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.hashed_password = get_password_hash(user.password)
    return await crud.create_user(db=db, user=user)


@app.post("/login/")
async def login(user: schemas.UserAuthenticate, db: AsyncSession = Depends(get_async_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    return {"message": "User authenticated successfully"}