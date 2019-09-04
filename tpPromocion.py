# Simulador de sistema  M/M/1.
#
# Variables de respuesta:
# - Demora promedio por cliente
# - Número promedio de clientes en cola
# - Utilización promedio de cliente
#
# Funciones:
#     arribo
#     partida
#     nuevoEvento
#     medidasDesempeño
#     generarTiempoExponencial
from asynchat import simple_producer
from asyncore import file_dispatcher

TIEMPO_ENTRE_ARRIBOS = 10
import numpy as np
import time
import sys


# class Evento:
#     """# Los eventos pueden ser ARRIBO o PARTIDA y tienen el tiempo en que se producen"""
#     def _init_(self, tipo, tiempo, opc = ''):
#         self.tipo = tipo # Los eventos pueden ser ARRIBO o PARTIDA
#         self.tiempo = tiempo
#         self.tiempo_fin
#         self.tiempo_inicio_cola2
#         self.tiempo_fin_cola2
#         self.opcional = opc
#     # self.optional = optional
#
#     # def _lt_(self, e):
#     #     return self.tiempo < e.tiempo

class Servidor(object):

    def __init__(self, id, tiempo_entre_servicio):
        self._id = id
        self.tiempo_entre_servicios = tiempo_entre_servicio
        # Tiempo entre arribos depende de la Simulacion no del Sevidor, pero para simplificar el
        #     problema, le agregue el atributo tambien a servidor.
        self.tiempoEntreArribos = TIEMPO_ENTRE_ARRIBOS
        self.reloj = 0.0
        self.estadoServ = 0
        self.lista_eventos = []
        self.cola = []
        self.num_cli_cola = 0
        self.demora_acumulada = 0.0
        self.completaron_demora = 0
        self.tiempo_ultimo_evento = 0.0
        self.area_qt = 0.0
        self.tiempo_servicio_total = 0

    def nuevoEvento(self, lista_eventos):

        self.tiempo_ultimo_evento = self.reloj
        self.lista_eventos = lista_eventos

        if self.lista_eventos[0] <= self.lista_eventos[1]:
            self.reloj = lista_eventos[0]
            self.arribo()
        else:
            self.reloj = lista_eventos[1]
            self.partida()
        Simulador.actualizar_lista_eventos(self._id, self.lista_eventos)

    def arribo_cola_intermedia(self, servidor, reloj):
        self.cola_intermedia.pop(0)
        # Servidor pasa
        # a 1, ocupado
        servidor.estadoServ = 1
        tiempo_servicio = generarTiempoExponencial(self.tiempo_entre_servicios)
        servidor.tiempo_servicio_total += tiempo_servicio

        # Retorna el tiempo en el que el servidor vuelve a estar disponible
        return reloj + tiempo_servicio

    def partida_cola_intermedia(self, servidor, reloj):
        pass

    def arribo(self):

        # Siguiente arribo
        self.lista_eventos[0] = self.reloj + generarTiempoExponencial(self.tiempoEntreArribos)

        if self.estadoServ == 0:
            # Servidor pasa a 1, ocupado
            self.estadoServ = 1

            # Programo el próximo evento partida
            self.lista_eventos[1] = self.reloj + generarTiempoExponencial(self.tiempo_entre_servicios)

            # Actualizo la cantidad de clientes que completaron la demora
            self.completaron_demora += 1
        else:
            # Calculo el Área bajo Q(t)
            self.area_qt += (self.num_cli_cola * (self.reloj - self.tiempo_ultimo_evento))
            self.num_cli_cola += 1

            # Acumulo el tiempo de servicio
            self.tiempo_servicio_total += (self.reloj - self.tiempo_ultimo_evento)

            # Agrego el cliente a la cola
            self.cola.append(self.reloj)
            print("Numero de clientes en cola", self.num_cli_cola)

    def partida(self):

        if self.num_cli_cola > 0:

            # Proxima partida
            self.lista_eventos[1] = self.reloj + generarTiempoExponencial(self.tiempo_entre_servicios)
            # Acumulo la demora acumulada como el valor actual del reloj
            # menos el valor del reloj cuando el cliente ingresó a la cola

            self.demora_acumulada += self.reloj - self.cola[0]

            # Actualizo el contador de clientes que completaron la demora
            self.completaron_demora += 1

            # Acumulo el tiempo de servicio
            self.tiempo_servicio_total += (self.reloj - self.tiempo_ultimo_evento)

            # Calculo el Área bajo Q(t) del período anterior (Reloj - TiempoUltimoEvento)
            self.area_qt += (self.num_cli_cola * (self.reloj - self.tiempo_ultimo_evento))
            self.num_cli_cola -= 1

            # Desplazo  todos los valores una posición hacia adelante
            self.cola.pop(0)
        else:

            # Acumulo el tiempo de servicio
            self.tiempo_servicio_total += (self.reloj - self.tiempo_ultimo_evento)
            self.estadoServ = 0
            self.lista_eventos[1] = 999999.0

    def medidasDesempeño(self):
        print("Medidas de desempeño de la simulación: ")
        print()
        print("El reloj quedo en ", self.reloj)

        var1 = self.area_qt / self.reloj
        print("Area q de t",self.area_qt)
        print("Nro promedio de cli en cola:", var1)

        print("Tiempo de servicio  total", self.tiempo_servicio_total)
        var2 = self.tiempo_servicio_total / self.reloj
        print("Utilización promedio de los servidores:", var2)

        print("Demora acumulada",self.demora_acumulada)
        print("Completaron demora",self.completaron_demora)
        var3 = self.demora_acumulada / self.completaron_demora
        print("Demora promedio por cliente:", var3)


class Simulador(object):

    Cantidad_clientes_en_sistema = 0
    Tiempo_clientes_en_sistema = 0.0
    Lista_eventos = []
    def __init__(self):
        # Tiempo de arribos a las colas
        self.tiempoEntreArribos = TIEMPO_ENTRE_ARRIBOS
        # Inicializacion de variables
        self.reloj_simulacion = 0.0
        self.proximoEvento = ""
        self.cola_intermedia = []
        self.proximo_evento = ""
        self.servidor_evento = 0
        self.servidor_lista_evento = []

    def inicializar(self):

        self.servidor1 = Servidor(1, 7)
        self.servidor2 = Servidor(2, 5)
        self.servidor3 = Servidor(3, 5)
        self.servidor4 = Servidor(4, 5)
        self.servidor5 = Servidor(5, 6)

        Simulador.Lista_eventos  = [[999999.9, 999999.9] , [generarTiempoExponencial(self.tiempoEntreArribos), 999999.9], [generarTiempoExponencial(self.tiempoEntreArribos), 999999.9]
            , [999999.9, 999999.9] , [999999.9, 999999.9], [999999.9, 999999.9]]


    def nuevo_evento(self):

        # self.tiempo_ultimo_evento = self.reloj_simulacion

        # Busco el servidor que tiene el evento mas proximo.
        # Ejemplo [ ["Arribos", "Partidas"], [4, 5], [6, 8], [9, 6], [1, 6], [4, 8]]
        #
        # Va a devolver el servidor 4, que tiene el evento arribo en 1
        self.servidor_evento = Simulador.Lista_eventos.index(min(Simulador.Lista_eventos))

        # Lista de eventos del servidor encontrado
        self.servidor_lista_evento  = Simulador.Lista_eventos [self.servidor_evento]

        # self.reloj_simulacion = min(self.servidor_lista_evento)
        if self.servidor_lista_evento[0] <= self.servidor_lista_evento[1]:
            self.reloj_simulacion = self.servidor_lista_evento[0]
            self.proximo_evento = "ARRIBO"
        else:
            self.reloj_simulacion = self.servidor_lista_evento[1]
            self.proximo_evento = "PARTIDA"
            # print(self.reloj_simulacion)

    @classmethod
    def actualizar_lista_eventos(cls, id_servidor, lista_eventos):
        Simulador.Lista_eventos[id_servidor] = lista_eventos

    def correr_simulacion(self):

        self.inicializar()
        while True:

            # print(Simulador.Lista_eventos)
            # Generar un nuevo evento. Bajo el supuesto de que nunca va a haber dos eventos en el mismo instante,
            #   ya que la funcion np.random.exponential(media) retorna un numero aleatorio de 16 decimales.
            self.nuevo_evento()
            # print("En tiempo",self.reloj_simulacion)
            # print("En servidor", self.servidor_evento," evento ", self.proximo_evento, "la lista de eventos es ", self.servidor_lista_evento)
            if self.servidor_evento == 1:
                self.servidor1.nuevoEvento(self.servidor_lista_evento)

            if self.servidor_evento == 2:
                self.servidor2.nuevoEvento(self.servidor_lista_evento)

#
            # if self.servidor_evento == 3:
            #     if self.proximo_evento == "ARRIBO":
            #         self.servidor3.arribo_cola_intermedia()
            #     else:
            #         self.servidor3.partida_cola_intermedia()
            # if self.servidor_evento == 4:
            #     if self.proximo_evento == "ARRIBO":
            #         self.servidor4.arribo_cola_intermedia()
            #     else:
            #         self.servidor4.partida_cola_intermedia()
            # if self.servidor_evento == 5:
            #     if self.proximo_evento == "ARRIBO":
            #         self.servidor5.arribo_cola_intermedia()
            #     else:
            #         self.servidor5.partida_cola_intermedia()

            # print("--------------------------------------------------------------------------")
            if self.reloj_simulacion >= 20:
                break
        # print(self.cola_intermedia)
        self.servidor1.medidasDesempeño()
        # self.servidor2.medidasDesempeño()


# ---------------------------------------------
# Funciones
# ---------------------------------------------
def generarTiempoExponencial(media):
    return np.random.exponential(1 / media)


# ---------------------------------------------
# Ejecución del modelo
# ---------------------------------------------

sim1 = Simulador()
sim1.correr_simulacion()