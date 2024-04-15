from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models
from . import schemas
from passlib.context import CryptContext


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)  # Verwende direkt db.add()
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Item).offset(skip).limit(limit))
    return result.scalars().all()

async def create_user_item(db: AsyncSession, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)  # Verwende direkt db.add()
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def get_events(db: AsyncSession, country: str = None, start_date: str = None, end_date: str = None, skip: int = 0, limit: int = 30):
    query = select(models.Event)

    if country:
        query = query.filter(models.Event.country == country)
    if start_date and end_date:
        query = query.filter(models.Event.date.between(start_date, end_date))

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_events(db: AsyncSession, skip: int = 0, limit: int = 25):
    result = await db.execute(select(models.Event).offset(skip).limit(limit))
    return result.scalars().all()


async def create_event(db: AsyncSession, event: schemas.EventCreate):
    db_event = models.Event(
        name=event.name,
        date=event.date,
        venue=event.venue,
        country=event.country
    )
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)  # Passwort hashen
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

