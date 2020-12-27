import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

db = []


class City(BaseModel):
    name: str
    timezone: str


@app.get('/')
def index():
    return {'key': 'value'}


@app.get('/cities')
def get_cities():
    return db


@app.get('/cities/{city_id')
def get_city(city_id: int):
    return db[city_id - 1]


@app.post('/cities')
def create_city(city: City):
    db.append(city.dict())
    return db[-1]


@app.delete('/cities/{city_id}')
def delete_city(city_id: int):
    db.pop(city_id - 1)
    return {}


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
