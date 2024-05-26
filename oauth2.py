from jose import JWTError, jwt
from datetime import datetime, timedelta
import schema
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret Key
# Command => openssl rand -hex 32
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
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=[ALGORITHM])
    return encoded_jwt


# Verify access token
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        uid: str = payload.get("user_id")

        if uid is None:
            raise credentials_exception

        token_data = schema.TokenData(id=uid)

    except JWTError:
        raise credentials_exception

    return token_data


# Get current user
# This function will be passed as a dependency in any of our path operations which will grab the token from our request
# automatically, extract the id for us, verify that the token is correct by calling the verify_access_token and fetch
# the user from the database and pass it on as parameter into our path operations
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
