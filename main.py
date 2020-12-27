import uvicorn
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

app = FastAPI()


class City(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50, unique=True)
    timezone = fields.CharField(50)


City_Pydantic = pydantic_model_creator(City, name='City')
CityIn_Pydantic = pydantic_model_creator(City, name='CityIn', exclude_readonly=True)


@app.get('/')
def index():
    return {'key': 'value'}


@app.get('/cities')
def get_cities():
    results = []
    for city in db:
        r = requests.get(f'http://worldclockapi.com/api/json/{city["timezone"]}/now')
        current_time = r.json()['currentDateTime']
        results.append({'name': city['name'], 'timezone': city['timezone'], 'current_time': current_time})
    return results


@app.get('/cities/{city_id')
def get_city(city_id: int):
    city = db[city_id - 1]
    r = requests.get(f'http://worldclockapi.com/api/json/{city["timezone"]}/now')
    current_time = r.json()['currentDateTime']
    return {'name': city['name'], 'timezone': city['timezone'], 'current_time': current_time}


@app.post('/cities')
async def create_city(city: CityIn_Pydantic):
    city_obj = await City.create(**city.dict(exclude_unset=True))
    return await City_Pydantic.from_tortoise_orm(city_obj)


@app.delete('/cities/{city_id}')
def delete_city(city_id: int):
    db.pop(city_id - 1)
    return {}


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
