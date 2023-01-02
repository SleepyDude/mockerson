from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import ValidationError
from faker import Faker
from typing import Optional
import random

router = APIRouter()

async def gen_row(fake: Faker) -> dict:
    return {
        'id': fake.unique.random_number(),
        'name': fake.name(),
        'address': fake.address(),
        'email': str(fake.email()),
        'phone': str(fake.phone_number()),
        'birthday': fake.date()
    }

@router.get('/fake_users/')
async def fake_users(request: Request):
    '''Get random user data based on query parameters if any
    --> {'detail' : [{'msg'},] , 'data' : [...]}
    You will get [1, 50) rows of fake user data
    '''
    params = request.query_params
    params_string = str(params)
    size = random.randint(1, 50)

    faker = Faker() 
    if params is not None:
        Faker.seed(params_string)

    data = [await gen_row(faker) for _ in range(size)]
    return {
        'detail': {
            'data-length': len(data),
            'msg' : 'success'
        },
        'data': data
    }
