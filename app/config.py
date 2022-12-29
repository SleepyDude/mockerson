from dotenv import load_dotenv
import os
load_dotenv()

DETA_PROJECT_KEY=os.getenv('DETA_PROJECT_KEY')
JWT_SECRET=os.getenv('JWT_SECRET')
FASTAPI_TESTING=os.getenv('FASTAPI_TESTING')

# Deta Base constants
DETA_USER_DB_TABLE="Users"

if FASTAPI_TESTING is not None:
    DETA_USER_DB_TABLE += '_test'
