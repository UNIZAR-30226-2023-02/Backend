from trivial_api.models import *
from trivial_api.serializers import *

#Token
from rest_framework.authtoken.models import Token


# Hay que pasar el header
def get_username(list_headers):
    token = None
    username = None
    for header_key, header_value in list_headers:
        if header_key.decode("utf-8").lower() == "token":
            token = header_value.decode("utf-8")
            break
    try: 
        usuario = Token.objects.filter(key=token).first() or None
        if(usuario):
            user = Usuario.objects.filter(username=usuario.user_id).first() or None
            username = user.username
        return username
    except:
        return None