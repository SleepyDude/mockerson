from pydantic import BaseModel, ValidationError, validator, root_validator
from fastapi import HTTPException
from typing import Optional

from app import constants as cnst

VALID_SHAPES = [
#    size page begin end
    [1,   0,   0,    0], # 0 # custom size
    [1,   0,   0,    1], # 1 # interval [ end-(size+1) ; end )
    [1,   0,   1,    0], # 2 # interval [ begin ; begin+size )
    [1,   1,   0,    0], # 3 # custom size with pagination
    [0,   0,   1,    1], # 4 # interval [ begin : end )
    [0,   0,   0,    0], # 5 # default 20 elements
    [0,   1,   0,    0], # 6 # default 20 elements per page and page number `page`
]

class QueryParams(BaseModel):
    size: Optional[int] = None
    seed: Optional[int] = None
    page: Optional[int] = None
    begin: Optional[int] = None
    end: Optional[int] = None

    @root_validator(pre=True)
    def check_shape(cls, v):
        # print('checking combination of v: \n', v)
        # print(type(v))
        # print(v.get('size'))
        # print(v.get('page'))
        # print(v.get('begin'))
        # print(v.get('end'))
        shape = [1 if i is not None else 0\
            for i in [v.get('size'), v.get('page'), v.get('begin'), v.get('end')]]
        # print('Got the following shape:', shape)
        if shape not in VALID_SHAPES:
            raise ValueError(cnst.WRONG_SHAPE.format(shape))
        return v

    @validator('*')
    def param_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError(f'query params should be not negative, {v} got')
        return v
    
    @validator('size')
    def zero_size(cls, v):
        if v is not None and v == 0:
            raise ValueError(f'size can not be zero')
        return v

    # @validator('size')
    # def size_positive(cls, v, values):
    #     if v <= 0:
    #         raise ValueError('`size` should be positive')
    #     if v and values.get('end') is not None:
    #         if values.get('end') <= v:
    #             raise ValueError('`size` should be less than `end` element index')
    #     return v

# try:
#     print(QueryParams(size=-14, seed=42, page=3, begin=66, end=99))
# except ValueError as e:
#     print(e.errors()[0]['msg'])

# try:
#     print(QueryParams(size=-10))
# except ValueError as e:
#     print(e.errors()[0]['msg'])


# class FakeUser(BaseModel):
#     id: int

# class FakeUser(BaseModel):
#     id: int
#     name: str
#     address: str
#     email: str
#     phone: str
#     birthday: str