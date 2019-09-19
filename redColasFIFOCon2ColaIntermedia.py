'''
Simulador de red de colas con mejora

La mejora implementada fue agregar una cola intermedia mas, a la que el cliente ingresara
con una probabilidad del 30% (Sera una cola rapida). El 70% de los clientes ingresaran a la
cola ya existente.

    ESQUEMA

 2 colas -> 2 servidores -> 2 colas -> 3 servidores

    VARIABLES DE RESPEUSTA

-  Utilizacion promedio de servidores
-  Número promedio de clientes en colas
-  Tiempo promedio de un cliente en el sistema

Funciones globales:
    generarExp

    CLASES

Servidor:
    arribo
    partida
    arribo_grupo2
    partida_grupo2
    nuevoEvento
    medidasDesempeño

Simulador
    minimo
    nuevo_evento_global
    correr_simulacion
    estadisticas_simulacion

  Metodos de clase

    actualizar_lista_eventos
    actualizar_tiempo_en_sistema(cls, t):

    CONSTANTES

INFINITO
TIEMPO_ENTRE_ARRIBOS
'''

TIEMPO_ENTRE_ARRIBOS = 1/10
INFINITO = 90000000000000.0  # 90 BILLONES DE PESOS O 1.45 BILLONES DE DOLARES
import math
import random

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
        self.tiempo_libre = 0.0

    def arribo_grupo2(self, reloj, opc = True):

        self.reloj = reloj
        self.lista_eventos[1] = reloj + generarExp(self.tiempo_entre_servicios)

        if self.estadoServ == 0:
            self.estadoServ = 1

        if opc:
            Simulador.Cola2.pop(0)
        else:
            Simulador.Cola1.pop(0)
        if len(Simulador.Cola2) > 0:
            Simulador.AreaQ2 += (len(Simulador.Cola2) * (self.reloj - self.tiempo_ultimo_evento))
            Simulador.actualizar_tiempo_en_sistema(len(Simulador.Cola2) * (self.reloj - self.tiempo_ultimo_evento))
            self.lista_eventos[0] = Simulador.Cola2[0]
            Simulador.Cola2.pop(0)

        elif len(Simulador.Cola1) > 0:
            Simulador.AreaQ += (len(Simulador.Cola1) * (self.reloj - self.tiempo_ultimo_evento))
            Simulador.actualizar_tiempo_en_sistema(len(Simulador.Cola1) * (self.reloj - self.tiempo_ultimo_evento))
            self.lista_eventos[0] = Simulador.Cola1[0]
            Simulador.Cola1.pop(0)

        Simulador.Completaron_demora += 1

        self.tiempo_ultimo_evento = reloj
        Simulador.actualizar_lista_eventos(self._id, self.lista_eventos)

    def partida_grupo2(self, reloj):

        self.reloj = reloj
        if len(Simulador.Cola2) > 0:
            self.demora_acumulada += self.reloj - Simulador.Cola2[0]
            Simulador.Completaron_demora2 += 1
            Simulador.Demora_acumulada2 += self.reloj - Simulador.Cola2[0]

            self.tiempo_servicio_total += (self.reloj - self.tiempo_ultimo_evento)
            Simulador.AreaQ2 += (len(Simulador.Cola2) * (self.reloj - self.tiempo_ultimo_evento))
            self.arribo_grupo2(reloj, Simulador.Cola2)
        elif len(Simulador.Cola1) > 0:
            self.demora_acumulada += self.reloj - Simulador.Cola1[0]
            Simulador.Completaron_demora += 1
            Simulador.Demora_acumulada += self.reloj - Simulador.Cola1[0]

            self.tiempo_servicio_total += (self.reloj - self.tiempo_ultimo_evento)
            Simulador.AreaQ += (len(Simulador.Cola1) * (self.reloj - self.tiempo_ultimo_evento))
            self.arribo_grupo2(reloj, opc = False)
        else:
            self.estadoServ = 0
            self.tiempo_servicio_total += (self.reloj - self.tiempo_ultimo_evento)
            self.lista_eventos[0] = INFINITO
            self.lista_eventos[1] = INFINITO

        Simulador.actualizar_tiempo_en_sistema(self.reloj - self.tiempo_ultimo_evento)
        Simulador.Cantidad_clientes_en_sistema += 1
        Simulador.actualizar_lista_eventos(self._id, self.lista_eventos)

    def arribo(self):

        self.lista_eventos[0] = self.reloj + generarExp(self.tiempoEntreArribos)

        if self.estadoServ == 0:
            self.tiempo_libre += self.reloj - self.tiempo_ultimo_evento
            self.estadoServ = 1
            self.lista_eventos[1] = self.reloj + generarExp(self.tiempo_entre_servicios)
            self.completaron_demora += 1
        else:
            self.tiempo_servicio_total += (self.reloj - self.tiempo_ultimo_evento)
            self.area_qt += (self.num_cli_cola * (self.reloj - self.tiempo_ultimo_evento))
            Simulador.actualizar_tiempo_en_sistema(self.num_cli_cola * (self.reloj - self.tiempo_ultimo_evento))
            self.num_cli_cola += 1
            self.cola.append(self.reloj)

    def partida(self):

        if random.random() > 0.3:
            Simulador.Cola1.append(self.lista_eventos[1])
        else:
            Simulador.Cola2.append(self.lista_eventos[1])

        if self.num_cli_cola > 0:

            self.lista_eventos[1] = self.reloj + generarExp(self.tiempo_entre_servicios)
            self.demora_acumulada += self.reloj - self.cola[0]
            self.completaron_demora += 1
            self.tiempo_servicio_total += (self.reloj - self.tiempo_ultimo_evento)
            Simulador.actualizar_tiempo_en_sistema(self.reloj - self.tiempo_ultimo_evento)
            # Calculo el Área bajo Q(t) del período anterior (Reloj - TiempoUltimoEvento)
            self.area_qt += (self.num_cli_cola * (self.reloj - self.tiempo_ultimo_evento))
            self.num_cli_cola -= 1
            self.cola.pop(0)
        else:
            self.estadoServ = 0
            print("Servidor quedo en cero en reloj", self.reloj)
            self.tiempo_servicio_total += (self.reloj - self.tiempo_ultimo_evento)
            Simulador.actualizar_tiempo_en_sistema(self.reloj - self.tiempo_ultimo_evento)
            self.lista_eventos[1] = INFINITO

    def nuevoEvento(self, lista_eventos):


        self.lista_eventos = lista_eventos

        if self.lista_eventos[0] <= self.lista_eventos[1]:
            self.reloj = self.lista_eventos[0]
            self.arribo()
        else:
            self.reloj = self.lista_eventos[1]
            self.partida()

        self.tiempo_ultimo_evento = self.reloj
        Simulador.actualizar_lista_eventos(self._id, self.lista_eventos)

    def medidasDesempeño(self):
        print("---------------------------------------------------")
        print("Medidas de desempeño del servidor: ", self._id)
        var2 = self.tiempo_servicio_total / self.reloj
        var2 = round(var2 * 100, 2)
        # print("Tiempo de servicio ", self.tiempo_servicio_total, " Reloj", self.reloj)
        print("    Utilización promedio del servidor:", var2)
        if self._id == 1 or self._id == 2:
            var1 = self.area_qt / self.reloj
            # var1 = math.trunc(var1, 2)
            print("    Nro promedio de cli en cola: %.2f" % var1)
            var3 = self.demora_acumulada / self.completaron_demora
            # var3 = math.trunc( 2)
            print("    Demora promedio por cliente: %.2f" % var3)
        # print("---------------------------------------------------")


class Simulador(object):
    Cantidad_clientes_en_sistema = 0
    Tiempo_clientes_en_sistema = 0.0
    Lista_eventos = []
    Cola1 = []
    Cola2 = []
    Completaron_demora = 0
    Completaron_demora2 = 0
    Demora_acumulada = 0.0
    Demora_acumulada2 = 0.0
    AreaQ = 0.0
    AreaQ2 = 0.0

    def __init__(self):
        self.tiempoEntreArribos = TIEMPO_ENTRE_ARRIBOS
        self.relojSIM = 0.0
        self.servidor_evento = 0
        self.servidor_lista_evento = []
        self.proximo_evento = ""

    def inicializar(self):

        self.ser1 = Servidor(1, 1 / 7)
        self.ser2 = Servidor(2, 1 / 5)
        self.ser3 = Servidor(3, 1 / 5)
        self.ser4 = Servidor(4, 1 / 5)
        self.ser5 = Servidor(5, 1 / 6)

        Simulador.Lista_eventos = [[INFINITO, INFINITO], [generarExp(self.tiempoEntreArribos), INFINITO],
                                   [generarExp(self.tiempoEntreArribos), INFINITO]
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

    def nuevo_evento_global(self):

        # Busco el servidor que tiene el evento mas proximo.
        # Ejemplo [ ["Arribos", "Partidas"], [4, 5], [6, 8], [9, 6], [1, 6], [4, 8]]
        #
        # Va a devolver el servidor 4, que tiene el evento arribo en 1

        self.servidor_evento = self.minimo(Simulador.Lista_eventos)
        self.servidor_lista_evento = Simulador.Lista_eventos[self.servidor_evento]

        if self.servidor_lista_evento[0] <= self.servidor_lista_evento[1]:
            self.relojSIM = self.servidor_lista_evento[0]
            self.proximo_evento = "ARRIBO"
        else:
            self.relojSIM = self.servidor_lista_evento[1]
            self.proximo_evento = "PARTIDA"

    @classmethod
    def actualizar_lista_eventos(cls, id_servidor, lista_eventos):
        Simulador.Lista_eventos[id_servidor] = lista_eventos

    @classmethod
    def actualizar_tiempo_en_sistema(cls, t):
        cls.Tiempo_clientes_en_sistema += t


    def estadisticas_simulacion(self):
        self.ser1.medidasDesempeño()
        self.ser2.medidasDesempeño()
        self.ser3.medidasDesempeño()
        self.ser4.medidasDesempeño()
        self.ser5.medidasDesempeño()
        var2 = Simulador.AreaQ / self.relojSIM
        print("--------------------------------------------------------")
        print("Medidas desempeño Cola Intermedia")
        print("    Numero promedio de clientes en cola intermedia %.2f"% var2)
        var3 = Simulador.AreaQ2 / self.relojSIM
        print("--------------------------------------------------------")
        print("Medidas desempeño Cola Rapida")
        print("    Numero promedio de clientes en cola rapida %.2f"% var3)
        print("    Area Q(t) Cola Intermedia %.3f" % Simulador.AreaQ)
        print("    Area Q(t) Cola rapida%.3f" % Simulador.AreaQ2)
        print("Tiempo promedio en el sistema %s" % (Simulador.Tiempo_clientes_en_sistema / Simulador.Cantidad_clientes_en_sistema))

    def correr_simulacion(self):

        self.inicializar()
        while True:

            # Generar un nuevo evento. Bajo el supuesto de que nunca va a haber dos eventos en el mismo instante,
            #   ya que la funcion np.random.exponential(media) retorna un numero aleatorio de 16 decimales.
            self.nuevo_evento_global()
            if self.servidor_evento == 1:
                self.ser1.nuevoEvento(self.servidor_lista_evento)

            if self.servidor_evento == 2:
                self.ser2.nuevoEvento(self.servidor_lista_evento)


            # En caso de que ocurra un evento partida en el servidor 1 o el servidor 2,
            #     le agrego el evento a la una de las colas intermedias.
            if len(Simulador.Cola2) > 0:
                if self.ser3.estadoServ == 0:
                    self.ser3.arribo_grupo2(self.relojSIM)
                elif self.ser4.estadoServ == 0:
                    self.ser4.arribo_grupo2(self.relojSIM)
                elif self.ser5.estadoServ == 0:
                    self.ser5.arribo_grupo2(self.relojSIM)
            elif len(Simulador.Cola1) > 0:
                if self.ser3.estadoServ == 0:
                    self.ser3.arribo_grupo2(self.relojSIM, opc = False)
                elif self.ser4.estadoServ == 0:
                    self.ser4.arribo_grupo2(self.relojSIM, opc = False)
                elif self.ser5.estadoServ == 0:
                    self.ser5.arribo_grupo2(self.relojSIM, opc = False)


            # Si el evento se produce en uno de los 3 servidores finales, genero las partidas, ya que los arribos
            #    se generan automaticamente cada vez que hay partidas en los dos primeros servidores.
            if self.servidor_evento == 3 :
                self.ser3.partida_grupo2(self.relojSIM)
            if self.servidor_evento == 4 :
                self.ser4.partida_grupo2(self.relojSIM)
            if self.servidor_evento == 5 :
                self.ser5.partida_grupo2(self.relojSIM)

            if self.relojSIM >= 1000000:
                break
        self.estadisticas_simulacion()



# ---------------------------------------------
# Funciones
# ---------------------------------------------
def generarExp(media):
    return -(1/media) * math.log(random.random())
    # return np.random.exponential(media)

# ---------------------------------------------
# Ejecución del modelo
# ---------------------------------------------
sim1 = Simulador()
sim1.correr_simulacion()
