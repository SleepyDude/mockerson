from deta import Deta
from config import DETA_PROJECT_KEY

deta = Deta(DETA_PROJECT_KEY)

# deta = Deta()
users_db = deta.Base('UsersDB')