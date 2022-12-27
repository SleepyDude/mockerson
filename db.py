from deta import Deta
from config import DETA_PROJECT_KEY

deta = Deta(DETA_PROJECT_KEY)

# deta = Deta()
users_db = deta.Base('UsersDB')

# from models import User

# user = User(
#     user_id=1,
#     username='LesnikJo',
#     password_hash='wertdcvgtfcv3456'
# )

# u = users_db.put(
#     data=user.dict(exclude={'user_id'}),
#     key=user.user_id,
#     expire_at=100
# )

# u = users_db.put(
#     data={'username': 'LesnikJo', 'endpoints': 'aaa bbb ccc ddd'},
#     key='lesnikjo',
#     expire_in=100
# )
# print(u)

# u = users_db.get('lesnikjo')
# print(u)