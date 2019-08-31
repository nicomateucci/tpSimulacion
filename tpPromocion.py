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

TIEMPO_ENTRE_ARRIBOS = 9.0
import numpy as np
import time
import sys

# class Evento:
#     """# Los eventos pueden ser ARRIBO o PARTIDA y tienen el tiempo en que se producen"""
#     def __init__(self, tipo, tiempo, opc = ''):
#         self.tipo = tipo # Los eventos pueden ser ARRIBO o PARTIDA
#         self.tiempo = tiempo
#         self.tiempo_fin
#         self.tiempo_inicio_cola2
#         self.tiempo_fin_cola2
#         self.opcional = opc
#     # self.optional = optional
#
#     # def __lt__(self, e):
#     #     return self.tiempo < e.tiempo

class Servidor(object):

    def __init__(self, id, tiempo_entre_servicio):

        self._id = id
        self.tiempo_entre_servicios = tiempo_entre_servicio

        # Tiempo entre arribos depende de la Simulacion no del Sevidor, pero para simplificar el
        #     problema, le agregue el atributo tambien a servidor.
        self.tiempoEntreArribos = TIEMPO_ENTRE_ARRIBOS
        self.reloj = 0
        self.estadoServ = 0
        self.lista_eventos = []
        self.cola = []
        self.num_cli_cola = 0
        self.demora_acumulada = 0.0
        self.completaron_demora = 0
        self.tiempo_ultimo_evento = 0.0
        self.area_qt = 0.0
        self.tiempo_servicio_total = 0

    def nuevo_evento(self):

        self.tiempo_ultimo_evento = self.reloj

        if self.lista_eventos[0] <= self.lista_eventos[1]:
            self.reloj = self.lista_eventos[0]
            self.arribo()
            return self.reloj, False
        else:
            self.reloj = self.lista_eventos[1]
            self.partida()
            return self.reloj, True

    def agregar_tiempo_arribo(self, t):
        self.lista_eventos.insert(0, t)

    def agregar_tiempo_partida(self, t):
        self.lista_eventos.insert(1, t)

    def arribo(self):

        # Siguiente arribo
        if self._id == 1 or self._id == 2:
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
            self.tiempo_servicio_total += (
            (self.reloj - self.tiempo_ultimo_evento))  # Obtengo el valor exponencial generado en la linea anterior

            # Agrego el cliente a la cola
            self.cola.append(self.reloj)

    def partida(self):

        if self.num_cli_cola > 0:

            # Proxima partida
            self.lista_eventos[1] = self.reloj + generarTiempoExponencial(self.tiempo_entre_servicios)
            # Acumulo la demora acumulada como el valor actual del reloj
            # menos el valor del reloj cuando el cliente ingresó a la cola

            self.demora_acumulada += self.reloj - self.cola[0]

            # Actualizo el contador de clientes que completaron la demora
            self.completaron_demora+= 1

            # Acumulo el tiempo de servicio
            self.tiempo_servicio_total += ((self.reloj - self.tiempo_ultimo_evento))

            # Calculo el Área bajo Q(t) del período anterior (Reloj - TiempoUltimoEvento)
            self.area_qt += (self.num_cli_cola * (self.reloj - self.tiempo_ultimo_evento))
            self.num_cli_cola -= 1

            # Desplazo  todos los valores una posición hacia adelante
            self.cola.pop(0)
        else:
            # 'Al no haber clientes en cola, establezco el estado del servidor en "Desocupado"

            # Acumulo el tiempo de servicio
            self.tiempo_servicio_total += ((self.reloj - self.tiempo_ultimo_evento))
            self.estadoServ = 0
            self.lista_eventos[1] = 99999.0
            print("Servidor numero" + str(self._id) + " quedo en estado " + str(self.estadoServ))


    def medidasDesempeño(self):
        print("Medidas de desempeño de la simulación: ")
        print()
        print("El reloj quedo en ", self.reloj)

        var1 = self.area_qt / self.reloj
        print("Nro promedio de cli en cola:", var1)

        print("Tiempo de servicio  total", self.tiempo_servicio_total)
        var2 = self.tiempo_servicio_total / self.reloj
        print("Utilización promedio de los servidores:", var2)

        var3 = self.demora_acumulada / self.completaron_demora
        print("Demora promedio por cliente:", var3)


class SimuladorMM1(object):

    def __init__(self):
        #Tiempo de arribos a las colas
        self.tiempoEntreArribos = TIEMPO_ENTRE_ARRIBOS
        #Inicializacion de variables
        self.reloj_simulacion = 0.0
        self.proximoEvento = ""
        self.cola_intermedia = []

    def inicializar(self):

        self.servidor1 = Servidor(1, 7)
        self.servidor2 = Servidor(2, 5)
        self.servidor3 = Servidor(3, 5)
        self.servidor4 = Servidor(4, 5)
        self.servidor5 = Servidor(5, 6)

        # Primeros arribos en ambos servidores
        self.servidor1.agregar_tiempo_arribo(generarTiempoExponencial(self.tiempoEntreArribos))
        self.servidor2.agregar_tiempo_arribo(generarTiempoExponencial(self.tiempoEntreArribos))
        self.servidor3.agregar_tiempo_arribo(0)
        self.servidor4.agregar_tiempo_arribo(0)
        self.servidor5.agregar_tiempo_arribo(0)

        self.servidor1.agregar_tiempo_partida(99999.0)
        self.servidor2.agregar_tiempo_partida(99999.0)
        self.servidor3.agregar_tiempo_partida(99999.0)
        self.servidor4.agregar_tiempo_partida(99999.0)
        self.servidor5.agregar_tiempo_partida(99999.0)

    def correr_simulacion(self):

        self.inicializar()
        while True:

            # Generar un nuevo evento para cada servidor
            self.reloj1, self.es_partida1 = self.servidor1.nuevo_evento()
            self.reloj2, self.es_partida2 = self.servidor2.nuevo_evento()


            # Considero que el reloj de la simulacion es el mayor de los servidores 1 y 2.
            if self.reloj1 >= self.reloj2:
                self.reloj_simulacion = self.reloj1
            else:
                self.reloj_simulacion = self.reloj2


            # if self.es_partida1:
            #     self.cola_intermedia.append(self.reloj1)
            # if self.es_partida2:
            #     self.cola_intermedia.append(self.reloj2)

            # La cantidad de tiempos en la cola intermedia puede ser:
            #    1 Igual a la cantidad de servidores, cola queda vacia
            #    2 Menor a la cantidad de servidores, cola queda vacia
            #    3 Mayor a la cantidad, en este caso la cola no queda vacia

            # En caso de que halla alguna partida en los servidores (1 o 2), los agrego a la cola intermedia
            #     y si alguno de los otros servidores esta libre agrego el arribo (En 3, 4 o 5)

            if self.es_partida1:
                if self.cola_intermedia:
                    if self.servidor3.estadoServ == 0:
                        self.cola_intermedia.pop(0)
                        self.servidor3.agregar_tiempo_arribo(self.reloj1)
                        self.servidor3.nuevo_evento()
                    elif self.servidor4.estadoServ == 0:
                         self.cola_intermedia.pop(0)
                         self.servidor4.agregar_tiempo_arribo(self.reloj1)
                         self.servidor4.nuevo_evento()
                    elif self.servidor5.estadoServ == 0:
                         self.cola_intermedia.pop(0)
                         self.servidor5.agregar_tiempo_arribo(self.reloj1)
                         self.servidor5.nuevo_evento()
                    else:
                         self.cola_intermedia.append(self.reloj1)
                         print("En not cola_int reloj esta en " + str(self.reloj_simulacion))
                else:
                    self.cola_intermedia.append(self.reloj1)
                    print("En self.es_partida1 reloj esta en " + str(self.reloj_simulacion))

            if self.es_partida2:
                if self.cola_intermedia:
                    if self.servidor3.estadoServ == 0:
                        self.cola_intermedia.pop(0)
                        self.servidor3.agregar_tiempo_arribo(self.reloj2)
                        self.servidor3.nuevo_evento()
                    elif self.servidor4.estadoServ == 0:
                        self.cola_intermedia.pop(0)
                        self.servidor4.agregar_tiempo_arribo(self.reloj2)
                        self.servidor4.nuevo_evento()
                    elif self.servidor5.estadoServ == 0:
                        self.cola_intermedia.pop(0)
                        self.servidor5.agregar_tiempo_arribo(self.reloj2)
                        self.servidor5.nuevo_evento()
                    else:
                        self.cola_intermedia.append(self.reloj2)
                        print("En not cola_int reloj esta en " + str(self.reloj_simulacion))
                else:
                    self.cola_intermedia.append(self.reloj2)
                    print("En self.es_partida2 reloj esta en " + str(self.reloj_simulacion))

            print("En tiempo " + str(self.reloj_simulacion) + " Tamaño cola " + str(len(self.cola_intermedia))+ " Cola: " + str(self.cola_intermedia))

            if self.reloj_simulacion >= 20:
                break
        # print(self.cola_intermedia)
        # self.servidor2.medidasDesempeño()
        # self.servidor1.medidasDesempeño()



# ---------------------------------------------
# Funciones
# ---------------------------------------------
def generarTiempoExponencial(media):
       return np.random.exponential(1/media)


# ---------------------------------------------
# Ejecución del modelo
# ---------------------------------------------

sim1 = SimuladorMM1()
sim1.correr_simulacion()

