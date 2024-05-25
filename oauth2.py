from jose import JWTError, jwt
from datetime import datetime, timedelta

# Secret Key
SECRET_KEY = "0f17cd56f1d45c4c984c230424f2fa8c14b59a3f4fac4df031961c7bc7a9a2e8"

# Algorithm
ALGORITHM = "HS256"

# Expiration Time
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Function to create a token
def create_access_token(data: dict):
    # Create a copy of data to not overwrite the original data
    to_encode = data.copy()

    # Create the expiration time for the token
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
