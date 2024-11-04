import os 
from dotenv import load_dotenv
from jwt import encode, decode

load_dotenv()
key = (os.getenv('SECRET_KEY')).encode('utf-8')



def create_token(data: dict) -> str:
    """
    Create a jwt tocken 
    """
    print(data)
    tocken = encode(payload=data, key=str(key), algorithm='HS256')
    return tocken


def validate_token(token: str) -> dict:
    """
    Validate a jwt tocken
    """
    try:
        #print(token)
        data = decode(jwt=token, key=str(key), algorithms=['HS256'])
        return data
    except Exception as e:
        raise e
