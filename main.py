import uvicorn
import requests
from fastapi import FastAPI
from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

app = FastAPI()


class City(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50, unique=True)
    timezone = fields.CharField(50)

    def current_time(self) -> str:
        r = requests.get(f'http://worldclockapi.com/api/json/{self.timezone}/now')
        current_time = r.json()['currentDateTime']
        return current_time

    class PydanticMeta:
        computed = ('current_time',)


City_Pydantic = pydantic_model_creator(City, name='City')
CityIn_Pydantic = pydantic_model_creator(City, name='CityIn', exclude_readonly=True)


@app.get('/')
def index():
    return {'key': 'value'}


@app.get('/cities')
async def get_cities():
    return await City_Pydantic.from_queryset(City.all())


@app.get('/cities/{city_id')
async def get_city(city_id: int):
    return await City_Pydantic.from_queryset_single(City.get(id=city_id))


@app.post('/cities')
async def create_city(city: CityIn_Pydantic):
    city_obj = await City.create(**city.dict(exclude_unset=True))
    return await City_Pydantic.from_tortoise_orm(city_obj)


@app.delete('/cities/{city_id}')
async def delete_city(city_id: int):
    await City.filter(id=city_id).delete()
    return {'msg': 'Success'}


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
