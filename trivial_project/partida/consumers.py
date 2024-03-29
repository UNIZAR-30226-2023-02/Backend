# partida/consumers.py
#
# Fichero de configuración para el Websockets de las partidas
#

import json
from trivial_api.models import *
from asgiref.sync import async_to_sync,sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from rest_framework.authtoken.models import Token
from urllib.parse import parse_qs

# Hay que poner partida.funciones_auxiliares no funciones_auxiliares
from .funciones_auxiliares import *

class GameConsumers(WebsocketConsumer):
    def connect(self):
        self.game_name = self.scope["url_route"]["kwargs"]["game_name"]
        self.game_group_name = "game_%s" % self.game_name

        # Get the query parameters from the URL
        query_params = parse_qs(self.scope["query_string"].decode())
        
        # Get the token and password parameters from the query parameters
        username = query_params.get("username", [None])[0]
        password = query_params.get("password", [None])[0]    
        self.username = username

        game = Partida.objects.filter(id =self.game_name).first() or None
        # Si no existe el juego denegamos el acceso
        if not game:
            print("Error no game")
            self.close()
            return None
        # Si se ha acabado la partida tambien denegamos el acceso
        if game.terminada == True:
            print("Error partida terminada")
            self.close()
            return None
       
        user = Usuario.objects.filter(username=username).first() or None
        # Si no existe el usuario denegamos el acceso
        if not user:
            print("Error not user")
            self.close()
            return None
        # Si el usuario estaba desconectado entonces tengo que enviarselo solo a el
        juega = Juega.objects.filter(id_partida=game,username=user).first() or None

        # Si el que estaba jugando se ha desconectado y ha vuelto a entrar, entonces solo se lo envio a el
        async_to_sync(self.channel_layer.group_add)(
                self.game_group_name, self.channel_name
            )

        self.accept()
        
        if(juega and not juega.activo):
            print("Volvemos a activar a : ", self.username)
            print("El orden de los jugadores es: " + str(game.orden_jugadores))
            juega.activo = True
            juega.save()
            datos_cargar_partida = cargar_datos_partida(self,False)
            self.send(text_data=json.dumps(datos_cargar_partida))
        else:

            # Si estan los jugadores que se necesitan para iniciar la partida, entocnes le enviamos a todos los usuarios la informacion
            if len(self.channel_layer.groups.get(self.game_group_name, {}).items()) == calcular_jugadores(self.game_name):
                datos_cargar_partida = cargar_datos_partida(self,True)
                print("Empieza la partida")
                print("El orden de los jugadores es: " + str(game.orden_jugadores))
                # Envio a todos los jugadores el mensaje 
                async_to_sync(self.channel_layer.group_send)(
                    self.game_group_name, {"type": "enviar_datos", "datos": datos_cargar_partida}
                )
        
    def enviar_datos(self, event):
        datos = event['datos']
        self.send(text_data=json.dumps(datos))


    def disconnect(self, close_code):
        # Hacemos que el usuario no este activo

        juega = Juega.objects.filter(id_partida=self.game_name,username=self.username).first() or None
        game = Partida.objects.filter(id =self.game_name).first() or None
        juega.activo = False
        juega.save()
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name, self.channel_name
        )
        # Si no hay jugadores en la partida la damos por terminada
        if len(self.channel_layer.groups.get(self.game_group_name, {}).items()) == 1:
            
            response = {
                'OK':"",
                'error': "",
                'jugador':"",
                'type':"",
                'subtype': "",
                'valor_dado': "",
                'casilla_elegida': "",
                'casillas_nuevas': "",
                'enunciado': "",
                'r1': "",
                'r2': "",
                'r3': "",
                'r4': "",
                'rc': "",
                'quesito': "",
                'tematica': "",
                'esCorrecta': "",
                'moneda_ganador': "",
                'moneda_resto': "",
                'mensage_chat': "",
            }
            response['OK'] = "true"
            response['type'] = "Fin"
            response['jugador'] = calcular_sig_jugador(self.game_name)
            response['moneda_ganador'] = "5"
            response['moneda_resto'] = "2" #Se puede hacer funcion para calcular monedas TODO
            
            if game.terminada == False:
                game.terminada = True
                game.ganador = calcular_sig_jugador(self.game_name)
                game.save()
                actualizar_estadisticas_partida(game.ganador, game.orden_jugadores)
            
            async_to_sync(self.channel_layer.group_send)(
                self.game_group_name, {"type": "enviar_datos", "datos": response}
            )

        self.close()
    
    def receive(self, text_data):
        mensaje = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name, {"type": "gestionar.mensaje", "mensaje": mensaje}
        )
        

    def gestionar_mensaje(self, event):
        
        response = {
            'OK':"",
            'error': "",
            'jugador':"",
            'type':"",
            'subtype': "",
            'valor_dado': "",
            'casilla_elegida': "",
            'casillas_nuevas': "",
            'enunciado': "",
            'r1': "",
            'r2': "",
            'r3': "",
            'r4': "",
            'rc': "",
            'quesito': "",
            'tematica': "",
            'esCorrecta': "",
            'moneda_ganador': "",
            'moneda_resto': "",
            'mensage_chat': "",
        }

        fin = False
        mensaje = event['mensaje']
        user = Usuario.objects.filter(username=self.username).first() or None

        # Hay que hacer que el mensaje del chat sea antes, ya que este se puede hacer aunque no sea el turno
        # Si no es su turno le denegamos la accion
        #print(jugador_con_turno(self.game_name))

        if mensaje['jugador'] != self.username:
            # Si el mensaje es de tipo Fin_pregunta o CHAT no quieren que le enviemos respuesta aqui, se hace abajo
            self.send(text_data=json.dumps(mensaje))
            return None
        
        if mensaje['OK'] == "true":
            if mensaje['type'] == "Peticion":
                if mensaje['subtype'] == "Tirar_dado":
                    tirada = tirar_dado()
                    print("Tirar dado: " + str(tirada))
                    casillas_posibles = calcular_siguiente_movimiento(tirada, mensaje['jugador'], self.game_name)
                    response['valor_dado'] = tirada
                    response['jugador'] = mensaje['jugador']
                    response['casillas_nuevas'] = casillas_posibles
                    response['type'] = "Respuesta"
                    response['subtype'] = "Dado_casillas"

                elif mensaje['subtype'] == "Movimiento_casilla":
                    pregunta = elegir_pregunta(mensaje['casilla_elegida'], mensaje['jugador'], self.game_name)
                    
                    # Vuelve a tirar si cae en la casilla de repetir
                    if pregunta['enunciado'] == 'repetir':
                        response['type'] = "Accion"
                        response['subtype'] = "Dados"
                        response['jugador'] = mensaje['jugador']
                    
                    else: # Cargamos la pregunta
                        response['enunciado'] = pregunta['enunciado']
                        response['r1'] = pregunta['r1']
                        response['r2'] = pregunta['r2']
                        response['r3'] = pregunta['r3']
                        response['r4'] = pregunta['r4']
                        response['rc'] = pregunta['rc']
                        response['quesito'] = pregunta['quesito']
                        response['tematica'] = pregunta['tematica']
                        response['jugador'] = mensaje['jugador']
                        response['type'] = "Respuesta"
                        response['subtype'] = "Pregunta"
                
            elif mensaje['type'] == "Actualizacion":
                if mensaje['subtype'] == "Fin_pregunta":
                    # Si el usuario acierta la pregunta
                    if mensaje['esCorrecta'] == "true":
                        print("Ha acertado la pregunta el usuario: " + self.username)
                        if mensaje['quesito'] == True:
                            fin = marcar_queso(mensaje['tematica'], mensaje['jugador'], self.game_name)
                            actualizar_estadisticas(user,mensaje['tematica'],True,True)
                        else:
                            actualizar_estadisticas(user,mensaje['tematica'],True,False)

                        response['jugador'] = mensaje['jugador']
                        if fin == True:
                            response['type'] = "Fin"
                            game = Partida.objects.filter(id =self.game_name).first() or None
                            game.terminada = True
                            game.ganador = mensaje['jugador']
                            response['moneda_ganador'] = "5"
                            response['moneda_resto'] = "2" #Se puede hacer funcion para calcular monedas TODO
                            game.save()

                            actualizar_estadisticas_partida(game.ganador, game.orden_jugadores) 
                        else:
                            response['type'] = "Accion"
                            response['subtype'] = "Dados"
                    elif mensaje['esCorrecta'] == "false":
                        actualizar_estadisticas(user,mensaje['tematica'],False,False)
                        response['jugador'] = calcular_sig_jugador(self.game_name)
                        print("El siguiete jugador a tirar es: " + response['jugador'])
                        response['type'] = "Accion"
                        response['subtype'] = "Dados"
                elif mensaje['subtype'] == "Contestar_pregunta":
                    print("Esperando el timer del front")
                    return None
                else:
                    print("Error al actualizar")
                    
            elif mensaje['type'] == "Chat":
                #response = mensaje
                print(mensaje['jugador'] + ": " + mensaje['mensage_chat'])
                return None
            else:
                #Error el backend solo recive Peticiones y Actualizaciones
                print("")
            
            response['OK'] = "true"
        else:
            response['OK'] = "false"
            response['error'] = mensaje['error']

        
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name, {"type": "enviar_datos", "datos": response}
        )

        
           
            















class GameConsumersTematica(WebsocketConsumer):   
    def connect(self):
        self.game_name = self.scope["url_route"]["kwargs"]["game_name"]
        self.game_group_name = "game_%s" % self.game_name

        # Get the query parameters from the URL
        query_params = parse_qs(self.scope["query_string"].decode())
        
        # Get the token and password parameters from the query parameters
        username = query_params.get("username", [None])[0]
        password = query_params.get("password", [None])[0]    
        self.username = username

        game = Partida.objects.filter(id =self.game_name).first() or None
        # Si no existe el juego denegamos el acceso
        if not game:
            print("Error no game")
            self.close()
            return None
        # Si se ha acabado la partida tambien denegamos el acceso
        if game.terminada == True:
            print("Error partida terminada")
            self.close()
            return None
       
        user = Usuario.objects.filter(username=username).first() or None
        # Si no existe el usuario denegamos el acceso
        if not user:
            print("Error not user")
            self.close()
            return None
        # Si el usuario estaba desconectado entonces tengo que enviarselo solo a el
        juega = Juega.objects.filter(id_partida=game,username=user).first() or None

        # Si el que estaba jugando se ha desconectado y ha vuelto a entrar, entonces solo se lo envio a el
        async_to_sync(self.channel_layer.group_add)(
                self.game_group_name, self.channel_name
            )

        self.tematica = game.tematica
        self.accept()
        
        if(juega and not juega.activo):
            print("Volvemos a activar a : ", self.username)
            print("El orden de los jugadores es: " + str(game.orden_jugadores))
            juega.activo = True
            juega.save()
            datos_cargar_partida = cargar_datos_partida(self,False)
            self.send(text_data=json.dumps(datos_cargar_partida))
        else:

            # Si estan los jugadores que se necesitan para iniciar la partida, entocnes le enviamos a todos los usuarios la informacion
            if len(self.channel_layer.groups.get(self.game_group_name, {}).items()) == calcular_jugadores(self.game_name):
                datos_cargar_partida = cargar_datos_partida(self,True)
                print("Empieza la partida")
                print("El orden de los jugadores es: " + str(game.orden_jugadores))
                # Envio a todos los jugadores el mensaje 
                async_to_sync(self.channel_layer.group_send)(
                    self.game_group_name, {"type": "enviar_datos", "datos": datos_cargar_partida}
                )
        
    def enviar_datos(self, event):
        datos = event['datos']
        self.send(text_data=json.dumps(datos))


    def disconnect(self, close_code):
        # Hacemos que el usuario no este activo

        juega = Juega.objects.filter(id_partida=self.game_name,username=self.username).first() or None
        game = Partida.objects.filter(id =self.game_name).first() or None
        juega.activo = False
        juega.save()
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name, self.channel_name
        )
        # Si no hay jugadores en la partida la damos por terminada
        if len(self.channel_layer.groups.get(self.game_group_name, {}).items()) == 1:
            
            response = {
                'OK':"",
                'error': "",
                'jugador':"",
                'type':"",
                'subtype': "",
                'valor_dado': "",
                'casilla_elegida': "",
                'casillas_nuevas': "",
                'enunciado': "",
                'r1': "",
                'r2': "",
                'r3': "",
                'r4': "",
                'rc': "",
                'quesito': "",
                'tematica': "",
                'esCorrecta': "",
                'moneda_ganador': "",
                'moneda_resto': "",
                'mensage_chat': "",
            }
            response['OK'] = "true"
            response['type'] = "Fin"
            response['jugador'] = calcular_sig_jugador(self.game_name)
            response['moneda_ganador'] = "5"
            response['moneda_resto'] = "2" #Se puede hacer funcion para calcular monedas TODO
            
            if game.terminada == False:
                game.terminada = True
                game.ganador = calcular_sig_jugador(self.game_name)
                game.save()
                actualizar_estadisticas_partida(game.ganador, game.orden_jugadores)
            
            async_to_sync(self.channel_layer.group_send)(
                self.game_group_name, {"type": "enviar_datos", "datos": response}
            )

        self.close()
        
    
    def receive(self, text_data):
        mensaje = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name, {"type": "gestionar.mensaje", "mensaje": mensaje}
        )

    def gestionar_mensaje(self, event):
        
        response = {
            'OK':"",
            'error': "",
            'jugador':"",
            'type':"",
            'subtype': "",
            'valor_dado': "",
            'casilla_elegida': "",
            'casillas_nuevas': "",
            'enunciado': "",
            'r1': "",
            'r2': "",
            'r3': "",
            'r4': "",
            'rc': "",
            'quesito': "",
            'tematica': "",
            'esCorrecta': "",
            'moneda_ganador': "",
            'moneda_resto': "",
            'mensage_chat': "",
        }

        fin = False
        mensaje = event['mensaje']
        user = Usuario.objects.filter(username=self.username).first() or None

        # Hay que hacer que el mensaje del chat sea antes, ya que este se puede hacer aunque no sea el turno
        # Si no es su turno le denegamos la accion
        #print(jugador_con_turno(self.game_name))

        if mensaje['jugador'] != self.username:
            # Si el mensaje es de tipo Fin_pregunta o CHAT no quieren que le enviemos respuesta aqui, se hace abajo
            self.send(text_data=json.dumps(mensaje))
            return None
        
        if mensaje['OK'] == "true":
            if mensaje['type'] == "Peticion":
                if mensaje['subtype'] == "Tirar_dado":
                    tirada = tirar_dado()
                    print("Tirar dado: " + str(tirada))
                    casillas_posibles = calcular_siguiente_movimiento(tirada, mensaje['jugador'], self.game_name)
                    response['valor_dado'] = tirada
                    response['jugador'] = mensaje['jugador']
                    response['casillas_nuevas'] = casillas_posibles
                    response['type'] = "Respuesta"
                    response['subtype'] = "Dado_casillas"

                elif mensaje['subtype'] == "Movimiento_casilla":
                    pregunta = elegir_pregunta(mensaje['casilla_elegida'], mensaje['jugador'], self.game_name, self.tematica)
                    
                    # Vuelve a tirar si cae en la casilla de repetir
                    if pregunta['enunciado'] == 'repetir':
                        response['type'] = "Accion"
                        response['subtype'] = "Dados"
                        response['jugador'] = mensaje['jugador']
                    
                    else: # Cargamos la pregunta
                        response['enunciado'] = pregunta['enunciado']
                        response['r1'] = pregunta['r1']
                        response['r2'] = pregunta['r2']
                        response['r3'] = pregunta['r3']
                        response['r4'] = pregunta['r4']
                        response['rc'] = pregunta['rc']
                        response['quesito'] = pregunta['quesito']
                        response['tematica'] = pregunta['tematica']
                        response['jugador'] = mensaje['jugador']
                        response['type'] = "Respuesta"
                        response['subtype'] = "Pregunta"
                
            elif mensaje['type'] == "Actualizacion":
                if mensaje['subtype'] == "Fin_pregunta":
                    # Si el usuario acierta la pregunta
                    if mensaje['esCorrecta'] == "true":
                        print("Ha acertado la pregunta el usuario: " + self.username)
                        if mensaje['quesito'] == True:
                            fin = marcar_queso(mensaje['tematica'], mensaje['jugador'], self.game_name)
                            actualizar_estadisticas(user,mensaje['tematica'],True,True)
                        else:
                            actualizar_estadisticas(user,mensaje['tematica'],True,False)

                        response['jugador'] = mensaje['jugador']
                        if fin == True:
                            response['type'] = "Fin"
                            game = Partida.objects.filter(id =self.game_name).first() or None
                            game.terminada = True
                            game.ganador = mensaje['jugador']
                            response['moneda_ganador'] = "5"
                            response['moneda_resto'] = "2" #Se puede hacer funcion para calcular monedas TODO
                            game.save()

                            actualizar_estadisticas_partida(game.ganador, game.orden_jugadores) 
                        else:
                            response['type'] = "Accion"
                            response['subtype'] = "Dados"
                    elif mensaje['esCorrecta'] == "false":
                        actualizar_estadisticas(user,mensaje['tematica'],False,False)
                        response['jugador'] = calcular_sig_jugador(self.game_name)
                        print("El siguiete jugador a tirar es: " + response['jugador'])
                        response['type'] = "Accion"
                        response['subtype'] = "Dados"
                elif mensaje['subtype'] == "Contestar_pregunta":
                    print("Esperando el timer del front")
                    return None
                else:
                    print("Error al actualizar")
                    
            elif mensaje['type'] == "Chat":
                #response = mensaje
                print(mensaje['jugador'] + ": " + mensaje['mensage_chat'])
                return None
            else:
                #Error el backend solo recive Peticiones y Actualizaciones
                print("")
            
            response['OK'] = "true"
        else:
            response['OK'] = "false"
            response['error'] = mensaje['error']

        
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name, {"type": "enviar_datos", "datos": response}
        )
    




















class GameConsumersEquipo(WebsocketConsumer):
    def connect(self):
        self.game_name = self.scope["url_route"]["kwargs"]["game_name"]
        self.game_group_name = "game_%s" % self.game_name

        # Get the query parameters from the URL
        query_params = parse_qs(self.scope["query_string"].decode())
        
        # Get the token and password parameters from the query parameters
        username = query_params.get("username", [None])[0]
        password = query_params.get("password", [None])[0]    
        self.username = username

        game = Partida.objects.filter(id =self.game_name).first() or None
        # Si no existe el juego denegamos el acceso
        if not game:
            print("Error no game")
            self.close()
            return None
        # Si se ha acabado la partida tambien denegamos el acceso
        if game.terminada == True:
            print("Error partida terminada")
            self.close()
            return None
       
        user = Usuario.objects.filter(username=username).first() or None
        # Si no existe el usuario denegamos el acceso
        if not user:
            print("Error not user")
            self.close()
            return None
        # Si el usuario estaba desconectado entonces tengo que enviarselo solo a el
        juega = Juega.objects.filter(id_partida=game,username=user).first() or None

        # Si el que estaba jugando se ha desconectado y ha vuelto a entrar, entonces solo se lo envio a el
        async_to_sync(self.channel_layer.group_add)(
                self.game_group_name, self.channel_name
            )

        self.accept()
        
        if(juega and not juega.activo):
            print("Volvemos a activar a : ", self.username)
            print("El orden de los jugadores es: " + str(game.orden_jugadores))
            juega.activo = True
            juega.save()
            datos_cargar_partida = cargar_datos_partida(self,False)
            self.send(text_data=json.dumps(datos_cargar_partida))
        else:

            # Si estan los jugadores que se necesitan para iniciar la partida, entocnes le enviamos a todos los usuarios la informacion
            if len(self.channel_layer.groups.get(self.game_group_name, {}).items()) == calcular_jugadores(self.game_name):
                datos_cargar_partida = cargar_datos_partida(self,True)
                print("Empieza la partida")
                print("El orden de los jugadores es: " + str(game.orden_jugadores))
                # Envio a todos los jugadores el mensaje 
                async_to_sync(self.channel_layer.group_send)(
                    self.game_group_name, {"type": "enviar_datos", "datos": datos_cargar_partida}
                )
        
    def enviar_datos(self, event):
        datos = event['datos']
        self.send(text_data=json.dumps(datos))


    def disconnect(self, close_code):
        # Hacemos que el usuario no este activo

        juega = Juega.objects.filter(id_partida=self.game_name,username=self.username).first() or None
        game = Partida.objects.filter(id =self.game_name).first() or None
        juega.activo = False
        juega.save()
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name, self.channel_name
        )

                    
        # Comprobamos que si quedan dos no son del mismo equipo, si lo son acabo la partida.
        acabo_partida = False
        if len(self.channel_layer.groups.get(self.game_group_name, {}).items()) == 2:
            lista_equipos = game.orden_jugadores
            lista_equipos = lista_equipos.split(';')
            for i in lista_equipos:
                lista_j = i.split(',')
                juega = Juega.objects.filter(id_partida=self.game_name,username=lista_j[0],activo=True).first() or None
                juega1 = Juega.objects.filter(id_partida=self.game_name,username=lista_j[1],activo=True).first() or None
                if(juega and juega1):
                    acabo_partida = True
                    break

        # Si no hay jugadores en la partida la damos por terminada, o si los dos que estan son del mismo equipo
        if len(self.channel_layer.groups.get(self.game_group_name, {}).items()) == 1 or acabo_partida:
            
            response = {
                'OK':"",
                'error': "",
                'jugador':"",
                'type':"",
                'subtype': "",
                'valor_dado': "",
                'casilla_elegida': "",
                'casillas_nuevas': "",
                'enunciado': "",
                'r1': "",
                'r2': "",
                'r3': "",
                'r4': "",
                'rc': "",
                'quesito': "",
                'tematica': "",
                'esCorrecta': "",
                'moneda_ganador': "",
                'moneda_resto': "",
                'mensage_chat': "",
            }
            nombre_jugador1, nombre_jugador2 = obtener_jugadores_equipo(self.game_name)
            response['OK'] = "true"
            response['type'] = "Fin"
            response['jugador'] = nombre_jugador1 + "," +  nombre_jugador2
            response['moneda_ganador'] = "5"
            response['moneda_resto'] = "2" #Se puede hacer funcion para calcular monedas TODO
            if game.terminada == False:
                game.terminada = True
                game.ganador = nombre_jugador1 + "," +  nombre_jugador2
                game.save()
                actualizar_estadisticas_partida_equipo(nombre_jugador1, nombre_jugador2, game.orden_jugadores)
            
            async_to_sync(self.channel_layer.group_send)(
                self.game_group_name, {"type": "enviar_datos", "datos": response}
            )

        self.close()
    
    def receive(self, text_data):
        mensaje = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name, {"type": "gestionar.mensaje", "mensaje": mensaje}
        )
        

    def gestionar_mensaje(self, event):
        
        response = {
            'OK':"",
            'error': "",
            'jugador':"",
            'type':"",
            'subtype': "",
            'valor_dado': "",
            'casilla_elegida': "",
            'casillas_nuevas': "",
            'enunciado': "",
            'r1': "",
            'r2': "",
            'r3': "",
            'r4': "",
            'rc': "",
            'quesito': "",
            'tematica': "",
            'esCorrecta': "",
            'moneda_ganador': "",
            'moneda_resto': "",
            'mensage_chat': "",
        }

        fin = False
        mensaje = event['mensaje']
        user = Usuario.objects.filter(username=self.username).first() or None

        # Hay que hacer que el mensaje del chat sea antes, ya que este se puede hacer aunque no sea el turno
        # Si no es su turno le denegamos la accion
        #print(jugador_con_turno(self.game_name))

        if mensaje['jugador'] != self.username:
            # Si el mensaje es de tipo Fin_pregunta o CHAT no quieren que le enviemos respuesta aqui, se hace abajo
            self.send(text_data=json.dumps(mensaje))
            return None
        
        if mensaje['OK'] == "true":
            if mensaje['type'] == "Peticion":
                if mensaje['subtype'] == "Tirar_dado":
                    tirada = tirar_dado()
                    print("Tirar dado: " + str(tirada))
                    casillas_posibles = calcular_siguiente_movimiento(tirada, mensaje['jugador'], self.game_name)
                    response['valor_dado'] = tirada
                    response['jugador'] = mensaje['jugador']
                    response['casillas_nuevas'] = casillas_posibles
                    response['type'] = "Respuesta"
                    response['subtype'] = "Dado_casillas"

                elif mensaje['subtype'] == "Movimiento_casilla":
                    pregunta = elegir_pregunta(mensaje['casilla_elegida'], mensaje['jugador'], self.game_name)
                    
                    # Vuelve a tirar si cae en la casilla de repetir
                    if pregunta['enunciado'] == 'repetir':
                        response['type'] = "Accion"
                        response['subtype'] = "Dados"
                        response['jugador'] = mensaje['jugador']
                    
                    else: # Cargamos la pregunta
                        response['enunciado'] = pregunta['enunciado']
                        response['r1'] = pregunta['r1']
                        response['r2'] = pregunta['r2']
                        response['r3'] = pregunta['r3']
                        response['r4'] = pregunta['r4']
                        response['rc'] = pregunta['rc']
                        response['quesito'] = pregunta['quesito']
                        response['tematica'] = pregunta['tematica']
                        response['jugador'] = mensaje['jugador']
                        response['type'] = "Respuesta"
                        response['subtype'] = "Pregunta"
                
            elif mensaje['type'] == "Actualizacion":
                if mensaje['subtype'] == "Fin_pregunta":
                    # Si el usuario acierta la pregunta
                    if mensaje['esCorrecta'] == "true":
                        print("Ha acertado la pregunta el usuario: " + self.username)
                        
                        nombre_jugador1, nombre_jugador2 = obtener_jugadores_equipo(self.game_name)
                        print("Van juntos: " + nombre_jugador1 + " - "+ nombre_jugador2)
                        if mensaje['quesito'] == True:
                            fin = marcar_queso(mensaje['tematica'], nombre_jugador1, self.game_name)
                            fin = marcar_queso(mensaje['tematica'], nombre_jugador2, self.game_name)
                            actualizar_estadisticas(user,mensaje['tematica'],True,True)
                        else:
                            actualizar_estadisticas(user,mensaje['tematica'],True,False)
                        
                        response['jugador'] = calcular_sig_jugador_equipo(self.game_name)
                        print("Ha acertado, Modo equipos siguiente: " + response['jugador'])
                                                
                        if fin == True:
                            response['type'] = "Fin"
                            game = Partida.objects.filter(id =self.game_name).first() or None
                            game.terminada = True
                            game.ganador = nombre_jugador1 + ',' + nombre_jugador2
                            response['moneda_ganador'] = "5"
                            response['moneda_resto'] = "2" #Se puede hacer funcion para calcular monedas TODO
                            game.save()
                            actualizar_estadisticas_partida_equipo(nombre_jugador1,nombre_jugador2,game.orden_jugadores) 
                        else:
                            response['type'] = "Accion"
                            response['subtype'] = "Dados"

                    elif mensaje['esCorrecta'] == "false":
                        actualizar_estadisticas(user,mensaje['tematica'],False,False)
                        response['jugador'] = calcular_sig_jugador(self.game_name, True)
                        print("Ha Fallado, Modo equipos siguiente: " + response['jugador'])
                        response['type'] = "Accion"
                        response['subtype'] = "Dados"
                elif mensaje['subtype'] == "Contestar_pregunta":
                    print("Esperando el timer del front")
                    return None
                else:
                    print("Error al actualizar")
                    
            elif mensaje['type'] == "Chat":
                #response = mensaje
                print(mensaje['jugador'] + ": " + mensaje['mensage_chat'])
                return None
            else:
                #Error el backend solo recive Peticiones y Actualizaciones
                print("")
            
            response['OK'] = "true"
        else:
            response['OK'] = "false"
            response['error'] = mensaje['error']

        
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name, {"type": "enviar_datos", "datos": response}
        )