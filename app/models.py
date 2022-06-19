from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class EventModel(models.Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    class Meta:
        table = "events"

    def __str__(self):
        return self.name


class CarModel(models.Model):
    id = fields.UUIDField(pk=True)
    model = fields.CharField(max_length=255)

    class Meta:
        table = "cars"


Event = pydantic_model_creator(EventModel)
EventCreate = pydantic_model_creator(EventModel, exclude_readonly=True)

Car = pydantic_model_creator(CarModel)
CarCreate = pydantic_model_creator(CarModel, exclude_readonly=True)
