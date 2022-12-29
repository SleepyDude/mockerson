from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from deta import Record, Deta
import bcrypt
import jwt

# from ..db import users_db, deta
# from app import db

from ..config import JWT_SECRET, DETA_USER_DB_TABLE
from ..models import User, UserOut, UserReg

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

router = APIRouter()


"""
    HELPERS
"""
async def authentificate_user(username: str, password: str):
    # users_db = await get_users_db()
    async with Deta() as d:
        base = d.base(DETA_USER_DB_TABLE)
        user = await base.get(username.lower()) # lower username is my key
        if user is None:
            return False
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return False
        return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # So long as the oauth2_scheme somewhere in the dependency chain
    # We habe a lock here
    # Need to decode the token
    user = None
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        # users_db = await get_users_db()
        async with Deta() as d:
            base = d.base(DETA_USER_DB_TABLE)
            user = await base.get(key=payload.get('username').lower())
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    return User(**user)

"""
    ROUTES
"""

@router.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
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
    
@router.post('/register_user')
async def register_user(input_user: UserReg):
    async with Deta() as d:
        base = d.base(DETA_USER_DB_TABLE)
        user = await base.get(input_user.username.lower())

    if user is None:
        hash_pass = bcrypt.hashpw(input_user.password.encode('utf-8'), bcrypt.gensalt())
        u = User(
            username=input_user.username,
            password_hash=hash_pass
        )
        resp = None
        async with Deta() as d:
            base = d.base(DETA_USER_DB_TABLE)
            resp = await base.put(
                Record(u.dict(), key=u.username.lower())
            )
        return {'Message': 'Registration success. Welcome, {}!'\
            .format(resp['processed']['items'][0]['username'])}
    else:
        return {'Message': 'Registration Failed. The user {} is already exists.'\
            .format(input_user.username)}

@router.get('/users/me', response_model=UserOut)
async def get_my_info(user: User = Depends(get_current_user)):
    return user
