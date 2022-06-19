import uuid
from typing import List

from fastapi import APIRouter
from tortoise.transactions import atomic, in_transaction

from app.models import Event, EventModel, Car, CarCreate, CarModel

router = APIRouter()


@router.get("/ping")
def pong():
    return {"ping": "pong!"}


@router.post("/event", response_model=Event, status_code=201)
async def event_create():
    event = await EventModel.create(name=f'name-{uuid.uuid4().hex[:4]}')
    return await Event.from_tortoise_orm(event)


@router.get('/event', response_model=List[Event])
async def event_list():
    event_qs = EventModel.all()
    return await Event.from_queryset(event_qs)

@atomic
@router.post('/car/create-three', response_model=List[Car], status_code=201)
async def car_create_three():
    car_data = CarCreate(model='Tesla model 3')

    async with in_transaction():
        cars = await CarModel.bulk_create([
            CarModel(**car_data.dict(exclude_unset=True)),
            CarModel(**car_data.dict(exclude_unset=True))
        ])
        car = await CarModel.create(**car_data.dict(exclude_unset=True))
        cars.append(car)
    return cars

