# from rest_framework import serializers
# from .models import *
# from datetime import datetime
# import re
# #Token
# from rest_framework.authtoken.models import Token
# from rest_framework.permissions import IsAuthenticated

# class UsuarioLoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, data):
#         username = data.get('username')
#         password = data.get('password')

#         # Comprobacion de errores
#         # Busca si existe el usuario, si no existe guarda None en user
#         user = Usuario.objects.filter(username=username).first() or None

#         if user == None:
#             raise serializers.ValidationError({'username': 'Usuario invalido'})
#         else:
#             if not user.check_password(password):
#                  raise serializers.ValidationError({'password': 'Contraseña invalida'})
    
#         token, _ = Token.objects.get_or_create(user=user)

#         return {'token': token.key}








# class UsuarioRegistrarSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
#     confirm_password = serializers.CharField()
#     fecha_nac = serializers.CharField()
#     correo = serializers.EmailField()
#     telefono = serializers.CharField()

#     def validate(self, data):
#         errors = {}
#         # Check the username
#         if Usuario.objects.filter(username=data['username']).exists():
#             errors['username'] = 'El usuario ya existe'
        
#         # Check the password
#         if len(data['password']) < 8:
#             errors['password'] = 'Contraseña inferior a 8 carácteres'
#         elif data['password'] != data['confirm_password']:
#             errors['password'] = 'Contraseñas diferentes'

        
#         # Check the email
#         regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
#         if not data['correo']:
#             errors['correo'] = 'El correo no puede estar vacio'
#         elif not re.search(regex,data['correo']):
#             errors['correo'] = 'El correo no es valido'
#         elif Usuario.objects.filter(correo=data['correo']).exists():
#             errors['correo'] = 'El correo ya esta en uso'
        
#         # Check the phone number
#         if len(data['telefono']) < 9:
#             errors['telefono'] = 'Teléfono inferior a 9 números'
        
#         # Check the date format
#         try:
#             datetime.strptime(data['fecha_nac'], '%Y-%m-%d')
#         except ValueError:
#             errors['fecha_nac'] = 'Formato fecha nacimiento invalido (YY-MM-DD)'
        
#         if errors:
#             raise serializers.ValidationError(errors)
#         return data