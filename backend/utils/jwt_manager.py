import jwt
from datetime import datetime, timedelta, timezone 
from typing import Optional
from core.config import settings 


def create_token(
    data: dict,
    expires_delta
):
    to_encode = data.copy()
    
    # print("secret key: ", settings.SECRET_KEY)
    # print("alorithm: ", settings.JWT_ALGORITHM)
    # print("to encode: ", to_encode)
    # print("exipres delta: ",expires_delta, type(expires_delta), type(int(expires_delta)))
    # print(datetime.now(tz=timezone.utc))
    print(datetime.now(tz=timezone.utc) + timedelta(minutes=int(expires_delta)))

    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=int(expires_delta))
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def create_access_token(
    data: dict,
    expires_delta = settings.ACCESS_TOKEN_EXPIRE_MINUTES
):
    # print("create access token", expires_delta, type(expires_delta))
    return create_token(data=data, expires_delta=expires_delta)


def create_refresh_token(
    data: dict,
    expires_delta = settings.REFRESH_TOKEN_EXPIRE_MINUTES
):
    return create_token(data=data, expires_delta=expires_delta)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError as e:
        print(e)
        return None
    except jwt.PyJWTError as e:
        print(e)
        return None 
    


