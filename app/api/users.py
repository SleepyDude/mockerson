from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from deta import Record, Deta
import bcrypt
import jwt

# from ..db import users_db, deta
# from app import db

from ..config import JWT_SECRET, DETA_USER_DB_TABLE
from ..models import User, UserOut, UserIn

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

router = APIRouter()


"""
    HELPERS
"""
async def authentificate_user(username: str, password: str):
    # users_db = await get_users_db()
    async with Deta() as d:
        base = d.base(DETA_USER_DB_TABLE)
        users = await base.get(username.lower()) # lower username is my key
        if users is None:
            return False
        user = users[0]
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return False
        return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # So long as the oauth2_scheme somewhere in the dependency chain
    # We have a lock here
    # Need to decode the token
    user = None
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        # users_db = await get_users_db()
        async with Deta() as d:
            base = d.base(DETA_USER_DB_TABLE)
            # print('base:', base)
            # print('username:', payload.get('username').lower())
            user = await base.get(payload.get('username').lower())
            
        if user is None:
            print('cant found user in database', user)
        else:
            user = user[0]
    except Exception as e:
        print('ERROR:', e)
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail='Invalid username or password'
        # )
    return User(**user)

"""
    ROUTES
"""

@router.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print('Got form data in /token:', form_data)
    # verify that the from_data is correct
    # form_data is gonna be the username and password
    user = await authentificate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid creditnails'
        )

    token = jwt.encode(user, JWT_SECRET)
    return {'access_token': token, 'token_type': 'bearer'}

@router.post('/user')
async def register_user(input_user: UserIn):
    print(input_user, 'tryin to register')
    async with Deta() as d:
        base = d.base(DETA_USER_DB_TABLE)
        users = await base.get(input_user.username.lower())

    if users is None:
        print('not found user in db')
        hash_pass = bcrypt.hashpw(input_user.password.encode('utf-8'), bcrypt.gensalt())
        u = User(
            username=input_user.username,
            password_hash=hash_pass
        )
        async with Deta() as d:
            base = d.base(DETA_USER_DB_TABLE)
            resp = await base.put(
                Record(u.dict(), key=u.username.lower())
            )
        return {'Message': 'Registration success. Welcome, {}!'\
            .format(resp['processed']['items'][0]['username'])}
    print('before exception rising')
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='Registration Failed. The user {} is already exists.'\
            .format(input_user.username)
    )

@router.get('/user', response_model=UserOut)
async def get_me(user: User = Depends(get_current_user)):
    return user

@router.delete(
    '/user',
    status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(user: User = Depends(get_current_user)):
    async with Deta() as d:
        base = d.base(DETA_USER_DB_TABLE)
        await base.delete(user.username.lower())
    return None