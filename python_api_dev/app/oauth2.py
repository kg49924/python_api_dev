from jose import JWTError, jwt
from datetime import datetime, timedelta
#SECREY_KEY
#ALGORITHM
#Expiration time

SECRET_KEY = "4bc89y498y498qh4545434656554356546453y5yy345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() - timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

