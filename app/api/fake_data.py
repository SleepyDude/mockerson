from fastapi import APIRouter
from faker import Faker
from typing import Optional, Union
from dataclasses import dataclass

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
#    size page begin end seed
    [1,   0,   0,    0], # 0 # custom size
    [1,   0,   0,    1], # 1 # interval [ end-(size+1) ; end )
    [1,   0,   1,    0], # 2 # interval [ begin ; begin+size )
    [1,   1,   0,    0], # 3 # custom size with pagination
    [0,   0,   1,    1], # 4 # interval [ begin : end )
    [0,   0,   0,    0], # 5 # default 20 elements
]

async def get_despenser(size, page, begin, end, seed)\
        -> Optional[Union[DispenserRNG, None]]:
    params = [size, page, begin, end]
    comb = [1 if i is not None else 0 for i in params]
    print('get the comb:', comb)
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
async def fake_users(
    size: Optional[int] = None,
    seed: Optional[int] = None,
    page: Optional[int] = None,
    begin: Optional[int] = None,
    end: Optional[int] = None,
    skip: Optional[int] = None,
):
    '''Get random user data --> {'meta' : '...' , 'data' : [...]}

        Supported the following query parameters:

        `size`: int -- rows of data
        `seed`: int -- RNG seed
        `page`: int -- page number
        `begin`: int -- first element index
        `end`: int -- last element index

        Valid combinations:
            Pages -- standart pagination interface
            - `size`
            - `page`

            Interval -- getting elements from a given range [from, to)
            - `begin` - element index
            - `end` - element index

            Bottom -> up
            - `begin` - element index
            - `size` - number of items from element with specific index

            Top -> down
            - `end` - element index
            - `size` - number of items from element with specific index
    '''
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