
import jwt 
from datetime import datetime , timedelta



headers ={
    'secret_key':'django-insecure-1a#=uqpcils-ga0)@398w5syzauh&24ku@*bx1xnn0-x$+j8h+',
    'algorithm':'HS256'
}


# to encode login data and create jwtToken
def encode_data(payload_data):
    
    jwtToken = jwt.encode(
        payload= payload_data, 
        key=headers["secret_key"], 
        algorithm=headers["algorithm"]
        )
    return jwtToken 

# to decode token to get payload data to check authentication
def decode_data(jwtToken):
    '''
    - Expiration time is automatically verified in jwt.decode() 
    - and raises jwt.ExpiredSignatureError if the expiration time is in the past .
    
    except jwt.exceptions.ExpiredSignatureError as expired_error:
              return expired_error
   
    except jwt.exceptions.InvalidSignatureError as Invalid_signature_error:
              return Invalid_signature_error
    
    '''
    payload_data = jwt.decode(
        jwt=jwtToken,
        key=headers["secret_key"], 
        algorithms=headers["algorithm"]
    )
    
    return payload_data

def create_token(username):
        
        # generate token
        token = encode_data(
            payload_data={'username': username,'exp': datetime.utcnow() + timedelta(days=90)}
        )
        
        return token    

#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjc0NDU2NDI5fQ.Hu8PXHmczZPR05oNW-c-VGxCdTMn9LgSDVoV_n8GUXI