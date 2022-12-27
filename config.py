from dotenv import load_dotenv
import os
load_dotenv()

DETA_PROJECT_KEY=os.getenv('DETA_PROJECT_KEY')
JWT_SECRET=os.getenv('JWT_SECRET')