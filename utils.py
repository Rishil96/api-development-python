from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to hash the user password
def hash_password(password):
    return pwd_context.hash(password)
