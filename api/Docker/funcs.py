from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext

from sklearn.model_selection import train_test_split

# Init security
security = HTTPBasic()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated=['auto'])


# Users database
users = {

	'alice': {
		'username': 'alice',
		'name': 'Alice',
		'hashed_password': pwd_context.hash('wonderland'),
	},

	'bob': {
		'username': 'bob',
		'name': 'Bob',
		'hashed_password': pwd_context.hash('builder'),
	},

	'clementine': {
		'username': 'clementine',
		'name': 'Clementine',
		'hashed_password': pwd_context.hash('mandarine'),
	}

}


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
	"""
	Get the current user
	Raise an error if not authenticated
	"""
	username = credentials.username
	if not(users.get(username)) or not(pwd_context.verify(credentials.password, users[username]['hashed_password'])):
		raise HTTPException(
		status_code = status.HTTP_401_UNAUTHORIZED,
		detail = 'Incorrect username or password',
		headers = { 'WWW-Authenticate': 'Basic' }
	)

	return credentials.username


def get_weather(w):
        """
        Get weather numeric value
        """
        weather = ''

        if w == 'Clear':
                weather = 1
        elif w == 'Cloudy':
                weather = 2
        elif w == 'Rainy':
                weather = 3
        elif w == 'Snowy':
                weather = 4

        return weather

