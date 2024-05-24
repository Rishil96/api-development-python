from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to hash the user password
def hash_password(password):
    return pwd_context.hash(password)


# Function to verify the password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
