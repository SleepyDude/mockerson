from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from faker import Faker
from typing import Optional, Union, Tuple
from dataclasses import dataclass

from app import constants as cons
from ..models.fake_data import QueryParams
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

# async def gen_row(fake: Faker) -> dict:
#     return {
#         'id': fake.unique.random_number(),
#         'name': fake.name(),
#         'address': fake.address(),
#         'email': str(fake.email()),
#         'phone': str(fake.phone_number()),
#         'birthday': fake.date()
#     }

async def gen_row(fake: Faker) -> dict:
    return {
        'id': fake.unique.random_number()
    }

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

# class DispenserIntervalSeed(DispenserBase):
#     '''
#     Generates data with given seed on given interval
#     '''
#     def __init__(self, seed, begin, end):
#         self.size = size
    
#     async def generate_data(self):
#         fake = Faker()
#         return [await gen_row(fake) for _ in range(self.size)]


VALID_COMBINATIONS = [
#    size page begin end
    [1,   0,   0,    0], # 0 # custom size
    [1,   0,   0,    1], # 1 # interval [ end-(size+1) ; end )
    [1,   0,   1,    0], # 2 # interval [ begin ; begin+size )
    [1,   1,   0,    0], # 3 # custom size with pagination
    [0,   0,   1,    1], # 4 # interval [ begin : end )
    [0,   0,   0,    0], # 5 # default 20 elements
]

async def query_data_validate(size, page, begin, end, seed) -> Tuple[bool, str]:
    # create combination shape for the given params
    params = [size, page, begin, end]
    comb = [1 if i is not None else 0 for i in params]

    print('get the comb:', comb)
    # check if comb is valid
    if comb not in VALID_COMBINATIONS:
        return False, cons.WRONG_COMB.format(comb)
    
    if size is not None:
        ...

    
    
    return True, 'Success params'


async def get_despenser(size, page, begin, end, seed)\
        -> Optional[Union[DispenserRNG, None]]:
    params = [size, page, begin, end]
    comb = [1 if i is not None else 0 for i in params]
    
    # let's take care about cases with RNG
    if seed is None:
        if comb == VALID_COMBINATIONS[5]:
            return DispenserRNG(20)
        if comb == VALID_COMBINATIONS[0] or\
           comb == VALID_COMBINATIONS[1] or\
           comb == VALID_COMBINATIONS[2] or\
           comb == VALID_COMBINATIONS[3]:
            return DispenserRNG(size)
        if comb == VALID_COMBINATIONS[4]:
            return DispenserRNG(end-begin)
    # it's harder if it's seeded
    if comb == VALID_COMBINATIONS[0]:
        ...

@router.get('/fake_users/')
async def fake_users(query_params: QueryParams = Depends(make_dependable(QueryParams))):
    '''Get random user data --> {'meta' : '...' , 'data' : [...]}

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
    print(f'got {query_params} params in /fake_users endpoint')
    return {'message': f'got {query_params} params in /fake_users endpoint'}
    res, message = await query_data_validate(size, page, begin, end, seed)
    print(message)
    return {}
    dsp = await get_despenser(size, page, begin, end, seed)
    if dsp is None:
        return {'Message': 'Incorrect data combination'}
    return await dsp.generate_data()
    # print(data)
    # fake = Faker()
    # if seed is not None:
    #     real_seed = seed + page
    #     Faker.seed(real_seed)
    #     if skip is not None:
    #         for _ in range(skip):
    #             await gen_row(fake)
    # return [await gen_row(fake) for _ in range(6)]