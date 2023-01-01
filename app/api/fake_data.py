from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from faker import Faker
from typing import Optional, Union, Tuple
from dataclasses import dataclass

from app import constants as cons
from ..models.fake_data import QueryParams, VALID_SHAPES
from ..models.utils import make_dependable

router = APIRouter()

'''static scheme
 id,
 name,
 address,
 email,
 phone,
 birthday,
'''

MAX_ITEMS = 300

async def gen_row(fake: Faker) -> dict:
    return {
        'id': fake.unique.random_number(),
        'name': fake.name(),
        'address': fake.address(),
        'email': str(fake.email()),
        'phone': str(fake.phone_number()),
        'birthday': fake.date()
    }

# async def gen_row(fake: Faker) -> dict:
#     return {
#         'id': fake.unique.random_number()
#     }

class DispenserBase:
    def __init__(self):
        ...

    async def generate_data(self):
        raise NotImplementedError('You should implement `generate_data` method in child')

class DispenserRNG(DispenserBase):
    '''
    Generates random data of given size
    '''
    def __init__(self, size):
        self.size = size
    
    async def generate_data(self):
        fake = Faker()
        return [await gen_row(fake) for _ in range(self.size)]

async def query_data_validate(size, page, begin, end, seed) -> Tuple[bool, str]:
    # create combination shape for the given params
    params = [size, page, begin, end]
    comb = [1 if i is not None else 0 for i in params]

    print('get the comb:', comb)
    # check if comb is valid
    if comb not in VALID_SHAPES:
        return False, cons.WRONG_COMB.format(comb)
    
    if size is not None:
        ...

    return True, 'Success params'


# async def get_despenser(size, page, begin, end, seed)\
#         -> Optional[Union[DispenserRNG, None]]:
async def get_despenser(q: QueryParams)\
        -> Optional[Union[DispenserRNG, None]]:
    params = [q.size, q.page, q.begin, q.end]
    comb = [1 if i is not None else 0 for i in params]
    
    # let's take care about cases with RNG
    if q.seed is None:
        if comb == VALID_SHAPES[5] or\
           comb == VALID_SHAPES[6]:
            return DispenserRNG(20)
        if comb == VALID_SHAPES[0] or\
           comb == VALID_SHAPES[1] or\
           comb == VALID_SHAPES[2] or\
           comb == VALID_SHAPES[3]:
            return DispenserRNG(q.size)
        if comb == VALID_SHAPES[4]:
            return DispenserRNG(q.end-q.begin)
    # it's harder if it's seeded
    raise Exception('Seeds not working for now')
    if comb == VALID_SHAPES[0]:
        ...

@router.get('/fake_users/')
async def fake_users(query_params: QueryParams = Depends(make_dependable(QueryParams))):
    '''Get random user data --> {'detail' : [{'msg'},] , 'data' : [...]}

        Supported the following query parameters:

        `size`: int -- rows of data
        `seed`: int -- RNG seed
        `page`: int -- page number
        `begin`: int -- first element index
        `end`: int -- last element index

        Valid combinations:
            Pages -- standart pagination interface
            - `size` - data per page
            - `page` - page number

            Interval -- getting elements from a given half-open interval `[begin, end)`
            - `begin` - start fake element index
            - `end` - next to finish element index

            LIMITATION -- both `begin` and `end` should be in `[0; 201)` half-open interval
            
            Bottom-up -- getting elements from a half-open interval `[begin, begin+size)`
            - `begin` - start fake element index
            - `size` - number of items from element with specific index

            LIMITATION -- `begin` and `size` should be in `[0; 201)` half-open interval

            Top-down -- getting elements from a half-open interval `(end-size-1, end]`
            - `end` - finish element index
            - `size` - number of items from element with specific index

            LIMITATION -- `end` and `size` should be in [0; 201) half-open interval
    '''
    # print(f'got {query_params} params in /fake_users endpoint')
    # return {'message': f'got {query_params} params in /fake_users endpoint'}
    msg = f'Got query params: {query_params}'
    desp = await get_despenser(query_params)
    if desp is not None:
        data = await desp.generate_data()
    return {
        'detail': {
            'status': 'success',
            'data-length': len(data),
            'msg' : msg
        },
        'data': data
    }
