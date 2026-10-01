from dotenv import load_dotenv
import os

<<<<<<< HEAD
=======

>>>>>>> 79752a4 (chain)
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_LIFETIME = 30
<<<<<<< HEAD
REFRESH_TOKEN_LIFETIME = 3
=======
REFRESH_TOKEN_LIFETIME = 7
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = os.getenv('OPENROUTER_URL')
>>>>>>> 79752a4 (chain)
