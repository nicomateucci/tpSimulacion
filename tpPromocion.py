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
INFINITO = 90000000000000.0  # 90 BILLONES DE PESOS O 1.45 BILLONES DE DOLARES
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
        self.lista_eventos = [INFINITO, INFINITO]
        self.cola = []
        self.num_cli_cola = 0
        self.demora_acumulada = 0.0
        self.completaron_demora = 0
        self.tiempo_ultimo_evento = 0.0
        self.area_qt = 0.0
        self.tiempo_servicio_total = 0

    def arribo_cola_intermedia(self, reloj):

        self.tiempo_ultimo_evento = reloj
        self.reloj = reloj
        self.lista_eventos[1] = reloj + generarTiempoExponencial(self.tiempo_entre_servicios)
        self.estadoServ = 1
        Simulador.Cola_intermedia.pop(0)
        if len(Simulador.Cola_intermedia) > 0:
            self.lista_eventos[0] = Simulador.Cola_intermedia[0]
            Simulador.Cola_intermedia.pop(0)

        Simulador.Completaron_demora += 1
        Simulador.actualizar_lista_eventos(self._id, self.lista_eventos)

    def partida_cola_intermedia(self, reloj):

        self.reloj = reloj
        if len(Simulador.Cola_intermedia) > 0:
            self.demora_acumulada += self.reloj - Simulador.Cola_intermedia[0]
            Simulador.Completaron_demora += 1
            Simulador.Demora_acumulada += self.reloj - Simulador.Cola_intermedia[0]
            self.tiempo_servicio_total += (self.reloj - self.tiempo_ultimo_evento)
            self.area_qt += (len(Simulador.Cola_intermedia) * (self.reloj - self.lista_eventos[0]))
            self.arribo_cola_intermedia(reloj)
        else:
            self.estadoServ = 0
            self.tiempo_servicio_total += (self.reloj - self.tiempo_ultimo_evento)
            self.lista_eventos[0] = INFINITO
            self.lista_eventos[1] = INFINITO

        Simulador.Cantidad_clientes_en_sistema += 1
        Simulador.actualizar_lista_eventos(self._id, self.lista_eventos)

    def arribo(self):

        self.lista_eventos[0] = self.reloj + generarTiempoExponencial(self.tiempoEntreArribos)

        if self.estadoServ == 0:
            self.estadoServ = 1
            self.lista_eventos[1] = self.reloj + generarTiempoExponencial(self.tiempo_entre_servicios)
            self.completaron_demora += 1
        else:
            self.tiempo_servicio_total += (self.reloj - self.tiempo_ultimo_evento)
            self.area_qt += (self.num_cli_cola * (self.reloj - self.tiempo_ultimo_evento))
            self.num_cli_cola += 1
            self.cola.append(self.reloj)

    def partida(self):

        Simulador.Cola_intermedia.append(self.lista_eventos[1])
        if self.num_cli_cola > 0:

            self.lista_eventos[1] = self.reloj + generarTiempoExponencial(self.tiempo_entre_servicios)
            self.demora_acumulada += self.reloj - self.cola[0]
            self.completaron_demora += 1
            self.tiempo_servicio_total += (self.reloj - self.tiempo_ultimo_evento)

            # Calculo el Área bajo Q(t) del período anterior (Reloj - TiempoUltimoEvento)
            self.area_qt += (self.num_cli_cola * (self.reloj - self.tiempo_ultimo_evento))
            self.num_cli_cola -= 1
            self.cola.pop(0)
        else:

            self.estadoServ = 0
            # Acumulo el tiempo de servicio
            self.tiempo_servicio_total += (self.reloj - self.tiempo_ultimo_evento)
            self.lista_eventos[1] = INFINITO

    def nuevoEvento(self, lista_eventos):

        self.tiempo_ultimo_evento = self.reloj
        self.lista_eventos = lista_eventos

        if self.lista_eventos[0] <= self.lista_eventos[1]:
            self.reloj = self.lista_eventos[0]
            self.arribo()
        else:
            self.reloj = self.lista_eventos[1]
            self.partida()

        Simulador.actualizar_lista_eventos(self._id, self.lista_eventos)

    def medidasDesempeño(self):
        print("Medidas de desempeño del servidor: ", self._id)
        print("---------------------------------------------------")
        var2 = self.tiempo_servicio_total / self.reloj
        print("Tiempo de servicio ", self.tiempo_servicio_total, " Reloj", self.reloj)
        print("Utilización promedio del servidors:", var2)
        if self._id == 1 or self._id == 2:
            var1 = self.area_qt / self.reloj
            print("Nro promedio de cli en cola:", var1)
            var3 = self.demora_acumulada / self.completaron_demora
            print("Demora promedio por cliente:", var3)
        print("---------------------------------------------------")


class Simulador(object):
    Cantidad_clientes_en_sistema = 0
    Tiempo_clientes_en_sistema = 0.0
    Lista_eventos = []
    Cola_intermedia = []
    Completaron_demora = 0
    Demora_acumulada = 0.0

    def __init__(self):
        self.tiempoEntreArribos = TIEMPO_ENTRE_ARRIBOS
        self.reloj_simulacion = 0.0
        self.servidor_evento = 0
        self.servidor_lista_evento = []
        self.proximo_evento = ""

    def inicializar(self):

        self.servidor1 = Servidor(1, 7)
        self.servidor2 = Servidor(2, 5)
        self.servidor3 = Servidor(3, 5)
        self.servidor4 = Servidor(4, 5)
        self.servidor5 = Servidor(5, 6)

        Simulador.Lista_eventos = [[INFINITO, INFINITO], [generarTiempoExponencial(self.tiempoEntreArribos), INFINITO],
                                   [generarTiempoExponencial(self.tiempoEntreArribos), INFINITO]
            , [INFINITO, INFINITO], [INFINITO, INFINITO], [INFINITO, INFINITO]]

    def minimo(self, lista):
        minimo = INFINITO
        i_minimo = 1
        for i in range(1,6):
            for j in range(0,2):
                if lista[i][j] < minimo:
                    minimo = lista[i][j]
                    i_minimo = i
        return i_minimo

    def nuevo_evento(self):

        # Busco el servidor que tiene el evento mas proximo.
        # Ejemplo [ ["Arribos", "Partidas"], [4, 5], [6, 8], [9, 6], [1, 6], [4, 8]]
        #
        # Va a devolver el servidor 4, que tiene el evento arribo en 1

        self.servidor_evento = self.minimo(Simulador.Lista_eventos)
        self.servidor_lista_evento = Simulador.Lista_eventos[self.servidor_evento]

        if self.servidor_lista_evento[0] <= self.servidor_lista_evento[1]:
            self.reloj_simulacion = self.servidor_lista_evento[0]
            self.proximo_evento = "ARRIBO"
        else:
            self.reloj_simulacion = self.servidor_lista_evento[1]
            self.proximo_evento = "PARTIDA"

    @classmethod
    def actualizar_lista_eventos(cls, id_servidor, lista_eventos):
        Simulador.Lista_eventos[id_servidor] = lista_eventos

    def correr_simulacion(self):

        self.inicializar()
        while True:

            # Generar un nuevo evento. Bajo el supuesto de que nunca va a haber dos eventos en el mismo instante,
            #   ya que la funcion np.random.exponential(media) retorna un numero aleatorio de 16 decimales.
            self.nuevo_evento()
            # print("En tiempo",self.reloj_simulacion)
            # print("En servidor", self.servidor_evento," evento ", self.proximo_evento, "la lista de eventos es ", self.servidor_lista_evento)
            if self.servidor_evento == 1:
                self.servidor1.nuevoEvento(self.servidor_lista_evento)

            if self.servidor_evento == 2:
                self.servidor2.nuevoEvento(self.servidor_lista_evento)

            if len(Simulador.Cola_intermedia) > 0:

                if len(Simulador.Cola_intermedia) > 1:
                    print(Simulador.Lista_eventos)
                    print(len(Simulador.Cola_intermedia))
                if self.servidor3.estadoServ == 0:
                    self.servidor3.arribo_cola_intermedia(self.reloj_simulacion)
                elif self.servidor4.estadoServ == 0:
                    self.servidor4.arribo_cola_intermedia(self.reloj_simulacion)
                elif self.servidor5.estadoServ == 0:
                    self.servidor5.arribo_cola_intermedia(self.reloj_simulacion)



            if self.servidor_evento == 3 and self.servidor3.lista_eventos[1] != INFINITO:
                self.servidor3.partida_cola_intermedia(self.reloj_simulacion)
            if self.servidor_evento == 4 and self.servidor4.lista_eventos[1] != INFINITO:
                self.servidor4.partida_cola_intermedia(self.reloj_simulacion)
            if self.servidor_evento == 5 and self.servidor5.lista_eventos[1] != INFINITO:
                self.servidor5.partida_cola_intermedia(self.reloj_simulacion)

            if self.reloj_simulacion >= 150000:
                break
        # print(self.cola_intermedia)
        self.servidor1.medidasDesempeño()
        self.servidor2.medidasDesempeño()
        self.servidor3.medidasDesempeño()
        self.servidor4.medidasDesempeño()
        self.servidor5.medidasDesempeño()
        var1 = Simulador.Demora_acumulada / Simulador.Completaron_demora
        print("Tiempo promedio de cliente en cola intermedia %s" % var1)
        print("Completaron demora ", Simulador.Completaron_demora)
        print("Demora acumulada", Simulador.Demora_acumulada)


# ---------------------------------------------
# Funciones
# ---------------------------------------------
def generarTiempoExponencial(media):
    # return -(media) * math.log(random.random())
    return np.random.exponential(media)

# ---------------------------------------------
# Ejecución del modelo
# ---------------------------------------------
sim1 = Simulador()
sim1.correr_simulacion()
