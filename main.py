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


@app.post('/cities')
def create_city(city: City):
    db.append(city.dict())
    return db[-1]


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
