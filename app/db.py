# from deta import Deta

# from .config import (
#     DETA_PROJECT_KEY,
#     DETA_USER_DB_TABLE,
#     FASTAPI_TESTING,
# )

# deta = None
# users_db = None

# async def init_deta():
#     global deta
#     global users_db
#     deta = Deta(DETA_PROJECT_KEY)
#     users_db = deta.base(DETA_USER_DB_TABLE)
#     print('INIT DETA ', deta, users_db)

# async def shutdown_deta():
#     global deta
#     deta.close()

# singletone-like piece of code

# async def get_users_db():
#     global deta
#     global users_db
#     print('deta and users_db:', deta, users_db)
#     if (deta is None and users_db is None):
#         db_name = DETA_USER_DB_TABLE
#         if FASTAPI_TESTING:
#             db_name = DETA_USER_DB_TABLE + "_test"
#         print("DEBUG: INITIALIZING DATABASE {}".format(db_name))
#         deta = Deta(DETA_PROJECT_KEY)
#         users_db = deta.base(db_name)
#     return users_db
