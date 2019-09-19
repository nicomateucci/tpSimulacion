'''
Simulador de red de colas

    ESQUEMA

 2 colas -> 2 servidores -> 1 cola -> 3 servidores

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
import matplotlib.pyplot as plt

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
        self.listaUsoServ = []
        self.listaNumCliCola = []

    def arribo_grupo2(self, reloj):

        self.reloj = reloj
        self.lista_eventos[1] = reloj + generarExp(self.tiempo_entre_servicios)

        if self.estadoServ == 0:
            self.estadoServ = 1

        Simulador.Cola_intermedia.pop(0)
        if len(Simulador.Cola_intermedia) > 0:
            Simulador.AreaQ += (len(Simulador.Cola_intermedia)*(self.reloj - self.tiempo_ultimo_evento))
            Simulador.ListaNumCliColaIntermedia.append(Simulador.AreaQ / Simulador.Reloj)
            Simulador.actualizar_tiempo_en_sistema(len(Simulador.Cola_intermedia)*(self.reloj - self.tiempo_ultimo_evento))
            self.lista_eventos[0] = Simulador.Cola_intermedia[0]
            Simulador.Cola_intermedia.pop(0)

        Simulador.Completaron_demora += 1

        self.tiempo_ultimo_evento = reloj
        Simulador.actualizar_lista_eventos(self._id, self.lista_eventos)

    def partida_grupo2(self, reloj):

        self.reloj = reloj
        if len(Simulador.Cola_intermedia) > 0:
            self.demora_acumulada += self.reloj - Simulador.Cola_intermedia[0]
            Simulador.Completaron_demora += 1
            Simulador.Demora_acumulada += self.reloj - Simulador.Cola_intermedia[0]

            self.tiempo_servicio_total += (self.reloj - self.tiempo_ultimo_evento)
            Simulador.AreaQ += (len(Simulador.Cola_intermedia) * (self.reloj - self.tiempo_ultimo_evento))
            Simulador.ListaNumCliColaIntermedia.append(Simulador.AreaQ / Simulador.Reloj)
            self.arribo_grupo2(reloj)
        else:
            self.estadoServ = 0
            self.tiempo_servicio_total += (self.reloj - self.tiempo_ultimo_evento)
            self.lista_eventos[0] = INFINITO
            self.lista_eventos[1] = INFINITO

        Simulador.actualizar_tiempo_en_sistema(self.reloj - self.tiempo_ultimo_evento)
        Simulador.Cantidad_clientes_en_sistema += 1

        self.listaUsoServ.append(self.tiempo_servicio_total / self.reloj)
        Simulador.ListaTiempoSistema.append(Simulador.Tiempo_clientes_en_sistema / Simulador.Cantidad_clientes_en_sistema)
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
            self.listaUsoServ.append(self.tiempo_servicio_total / self.reloj)
            self.area_qt += (self.num_cli_cola * (self.reloj - self.tiempo_ultimo_evento))
            self.listaNumCliCola.append(self.area_qt/ self.reloj)
            Simulador.actualizar_tiempo_en_sistema(self.num_cli_cola * (self.reloj - self.tiempo_ultimo_evento))
            self.num_cli_cola += 1
            self.cola.append(self.reloj)

    def partida(self):

        Simulador.Cola_intermedia.append(self.lista_eventos[1])
        if self.num_cli_cola > 0:

            self.lista_eventos[1] = self.reloj + generarExp(self.tiempo_entre_servicios)
            self.demora_acumulada += self.reloj - self.cola[0]
            self.completaron_demora += 1
            self.tiempo_servicio_total += (self.reloj - self.tiempo_ultimo_evento)
            self.listaUsoServ.append(self.tiempo_servicio_total / self.reloj)
            Simulador.actualizar_tiempo_en_sistema(self.reloj - self.tiempo_ultimo_evento)
            self.area_qt += (self.num_cli_cola * (self.reloj - self.tiempo_ultimo_evento))
            self.listaNumCliCola.append(self.area_qt / self.reloj)
            self.num_cli_cola -= 1
            self.cola.pop(0)
        else:
            self.estadoServ = 0
            print("Servidor quedo en cero en reloj", self.reloj)
            self.tiempo_servicio_total += (self.reloj - self.tiempo_ultimo_evento)
            self.listaUsoServ.append(self.tiempo_servicio_total / self.reloj)
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
        print("    Utilización promedio del servidor:", var2)
        if self._id == 1 or self._id == 2:
            var1 = self.area_qt / self.reloj
            print("    Nro promedio de cli en cola: %.2f" % var1)
            var3 = self.demora_acumulada / self.completaron_demora
            print("    Demora promedio por cliente: %.2f" % var3)


class Simulador(object):
    Cantidad_clientes_en_sistema = 0
    Tiempo_clientes_en_sistema = 0.0
    Lista_eventos = []
    Cola_intermedia = []
    Completaron_demora = 0
    Demora_acumulada = 0.0
    AreaQ = 0.0
    ListaTiempoSistema = []
    ListaNumCliColaIntermedia = []
    Reloj = 0.0

    def __init__(self):
        self.tiempoEntreArribos = TIEMPO_ENTRE_ARRIBOS
        self.relojSIM = 0.0
        self.servidor_evento = 0
        self.servidor_lista_evento = []
        self.proximo_evento = ""

    @classmethod
    def actualizar_lista_eventos(cls, id_servidor, lista_eventos):
        Simulador.Lista_eventos[id_servidor] = lista_eventos

    @classmethod
    def actualizar_tiempo_en_sistema(cls, t):
        cls.Tiempo_clientes_en_sistema += t

    @classmethod
    def inicializarClase(cls):
        cls.Cantidad_clientes_en_sistema = 0
        cls.Tiempo_clientes_en_sistema = 0.0
        cls.Lista_eventos = []
        cls.Cola_intermedia = []
        cls.Completaron_demora = 0
        cls.Demora_acumulada = 0.0
        cls.AreaQ = 0.0
        cls.ListaTiempoSistema = []

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
        print("Tiempo promedio en el sistema %s" % (Simulador.Tiempo_clientes_en_sistema / Simulador.Cantidad_clientes_en_sistema))

    def graficarPromedioUtilServidor(self, lista, utilizacionProm=0.77, text = ''):
        plt.figure().patch.set_facecolor('silver')
        plt.title('Utilizacion promedio del servidor: ' + text)
        plt.plot(lista)
        plt.xlabel("tiempo")
        plt.ylabel("Utilizacion promedio")
        # Banda horizontal de y=0 a y=2 de color azul
        # y 30% de transparencia (alpha=0.3)
        plt.axhspan(utilizacionProm - (utilizacionProm * 0.03), utilizacionProm + utilizacionProm * 0.03, alpha=0.8,
                    color='cornflowerblue')
        plt.text(0.2 * len(lista), 0.6, 'Utilizacion promedio: %.2f' % utilizacionProm, color="b", style='italic',
                 bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
        plt.axhline(utilizacionProm, color='b', ls="-.", xmax=3)  # Comando para linea horizontal constante
        plt.ylim(0, 1)  # Limites para el eje Y
        plt.xlim(0, 0.5*len(lista))  # Limites para el eje X
        plt.show()

    def graficarPromediosNumCola(self, lista, promedioNumCola = 2.4, text = ''):
        plt.figure().patch.set_facecolor('silver')
        plt.title('Número promedio de clientes en cola en: ' + text)
        plt.plot(lista, color='r')
        plt.xlabel("tiempo")
        plt.ylabel("Número promedio en cola")
        # Banda horizontal de y=0 a y=2 de color azul
        # y 30% de transparencia (alpha=0.3)
        plt.axhspan(promedioNumCola - (promedioNumCola * 0.03), promedioNumCola + promedioNumCola * 0.03, alpha=0.8,
                    color='cornflowerblue')
        plt.text(0.1 * len(lista), 0.7 * max(lista),
                 'Número promedio de clientes en cola: %.2f' % promedioNumCola, color="r", style='italic',
                 bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
        plt.axhline(promedioNumCola, color='r', ls="-.", xmax=3)  # Comando para linea horizontal constante
        plt.ylim(0, max(lista) + 0.2)  # Limites para el eje Y
        plt.xlim(0, 0.5*len(lista))  # Limites para el eje X
        plt.show()

    def graficarTiempoSistema(self, lista, tprom = 2.4):
        plt.figure().patch.set_facecolor('silver')
        plt.title('Tiempo promedio de clientes en sistema: ')
        plt.plot(lista, color='r')
        plt.xlabel("tiempo")
        plt.ylabel("Tiempo promedio en sistema")
        plt.axhspan(tprom - (tprom* 0.03), tprom+ tprom * 0.03, alpha=0.8, color='cornflowerblue')
        plt.text(0.1 * len(lista), 0.35* (max(lista) + 1), 'Tiempo promedio de clientes en sistema: %.2f' % tprom, color="r", style='italic',
                 bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
        plt.axhline(tprom, color='r', ls="-.", xmax=3)  # Comando para linea horizontal constante
        plt.ylim(0, max(lista) + 1.5)  # Limites para el eje Y
        plt.xlim(0, 0.5*len(lista))  # Limites para el eje X
        plt.show()


    def correr_simulacion(self):


        self.inicializar()
        while True:

            # Generar un nuevo evento. Bajo el supuesto de que nunca va a haber dos eventos en el mismo instante,
            #   ya que la funcion np.random.exponential(media) retorna un numero aleatorio de 16 decimales.
            self.nuevo_evento_global()
            Simulador.Reloj = self.relojSIM
            if self.servidor_evento == 1:
                self.ser1.nuevoEvento(self.servidor_lista_evento)

            if self.servidor_evento == 2:
                self.ser2.nuevoEvento(self.servidor_lista_evento)

            if len(Simulador.Cola_intermedia) > 0:

                if self.ser3.estadoServ == 0:
                    self.ser3.arribo_grupo2(self.relojSIM)
                elif self.ser4.estadoServ == 0:
                    self.ser4.arribo_grupo2(self.relojSIM)
                elif self.ser5.estadoServ == 0:
                    self.ser5.arribo_grupo2(self.relojSIM)

            if self.servidor_evento == 3 :
                self.ser3.partida_grupo2(self.relojSIM)
            if self.servidor_evento == 4 :
                self.ser4.partida_grupo2(self.relojSIM)
            if self.servidor_evento == 5 :
                self.ser5.partida_grupo2(self.relojSIM)

            if self.relojSIM >= 20000:
                break
        self.estadisticas_simulacion()
        var1 = self.ser1.tiempo_servicio_total/self.ser1.reloj
        var2 = self.ser1.area_qt/self.ser1.reloj
        self.graficarPromedioUtilServidor(self.ser1.listaUsoServ, var1, "Servidor 1")
        self.graficarPromediosNumCola(self.ser1.listaNumCliCola, var2, "Servidor 1")

        var1 = self.ser2.tiempo_servicio_total / self.ser2.reloj
        var2 = self.ser2.area_qt / self.ser2.reloj
        self.graficarPromedioUtilServidor(self.ser2.listaUsoServ, var1, "Servidor 2")
        self.graficarPromediosNumCola(self.ser2.listaNumCliCola, var2, "Servidor 2")

        var1 = self.ser4.tiempo_servicio_total / self.ser4.reloj
        self.graficarPromedioUtilServidor(self.ser4.listaUsoServ, var1, "Servidor 4")

        self.graficarTiempoSistema(Simulador.ListaTiempoSistema, Simulador.Tiempo_clientes_en_sistema/Simulador.Cantidad_clientes_en_sistema)
        var1 = Simulador.AreaQ / self.relojSIM
        self.graficarPromediosNumCola(Simulador.ListaNumCliColaIntermedia, var1, "Cola Intermedia")


# ---------------------------------------------
# Funciones
# ---------------------------------------------
def generarExp(media):
    return -(1/media) * math.log(random.random())

def graficarPromedio(ll, utilizacionProm = 0.77):
    plt.figure().patch.set_facecolor('silver')
    plt.title('Utilizacion promedio del servidor en 5 corridas distintas')
    plt.plot(ll[0], 'r', ll[1], 'deeppink', ll[2], 'b', ll[3], 'yellow', ll[4], 'aqua')
    plt.xlabel("tiempo")
    plt.ylabel("Utilizacion promedio por servidor")
    plt.axhspan(utilizacionProm - (utilizacionProm * 0.03), utilizacionProm + utilizacionProm * 0.03, alpha=0.8, color='cornflowerblue')
    plt.axvspan(4000, len(min(ll)), alpha=0.5, color='y')
    plt.axhline(utilizacionProm, color='k', ls="-.", lw="1.5", xmax=1)  # Comando para linea horizontal interlineada

    plt.ylim(0, 1)  # Limites para el eje Y
    plt.xlim(0, len(min(ll)))  # Limites para el eje X

    plt.show()



    var = input("Ingrese el tiempo en el que es sistema pasa a estado estacionario ")

    # Color de fondo de la brode de la imagen
    plt.figure().patch.set_facecolor('silver')
    plt.title('Utilizacion promedio del servidor en 5 simulaciones')
    plt.plot(ll[0], 'r', ll[1], 'deeppink', ll[2], 'b', ll[3], 'yellow', ll[4], 'aqua')
    # plt.plot(ll[0], 'lightcoral', ll[1], 'y', ll[2], 'steelblue', ll[3], 'goldenrod', ll[4], 'chocolate')
    plt.xlabel("tiempo")
    plt.ylabel("Utilizacion promedio por servidor")

    # Banda horizontal de y=0 a y=2 de color azul
    # y 30% de transparencia (alpha=0.3)
    plt.axhspan(utilizacionProm - (utilizacionProm * 0.03), utilizacionProm + utilizacionProm * 0.03, alpha=0.8, color='cornflowerblue')

    # Banda vertical de x=0 a x=4 de color amarillo
    # y 30% de transparencia
    plt.axvspan(int(var), len(min(ll)), alpha=0.5, color='y')

    plt.axhline(utilizacionProm, color='k', ls="-.", lw="1.5", xmax=1)  # Comando para linea horizontal interlineada '-.'

    plt.ylim(0, 1)  # Limites para el eje Y

    # Calculo el tamaño minimo de los arreglos para graficar
    minimo = len(ll[0])
    for i in range(1,5):
        x = len(ll[i])
        if x < minimo:
            minimo= x
    plt.xlim(0, minimo)  # Limites para el eje X

    ## Graficos de abajo
    plt.text(200, 0.05, 'Estado transiente', color="k", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
    plt.text(3500, 0.05, 'Estado estacionario', color="b", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})

    #Graficos de cada simulacion
    plt.text(5000, 0.63, 'Corrida 1', color="r", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
    plt.text(5000, 0.56, 'Corrida 2', color="deeppink", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
    plt.text(5000, 0.49, 'Corrida 3', color="b", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
    plt.text(5000, 0.42, 'Corrida 4', color="yellow", style='italic', bbox={'facecolor': 'white', 'alpha': 0.99, 'pad': 5})
    plt.text(5000, 0.35, 'Corrida 5', color="aqua", style='italic', bbox={'facecolor': 'white', 'alpha': 0.99, 'pad': 5})
    plt.show()

def graficarNumCola(ll, utilizacionProm = 0.77):
    plt.figure().patch.set_facecolor('silver')
    plt.title('Utilizacion promedio del servidor en 5 corridas distintas')
    plt.plot(ll[0], 'r', ll[1], 'deeppink', ll[2], 'b', ll[3], 'yellow', ll[4], 'aqua')
    plt.xlabel("tiempo")
    plt.ylabel("Utilizacion promedio por servidor")
    plt.axhspan(utilizacionProm - (utilizacionProm * 0.03), utilizacionProm + utilizacionProm * 0.03, alpha=0.8, color='cornflowerblue')
    plt.axvspan(4000, len(min(ll)), alpha=0.5, color='y')
    plt.axhline(utilizacionProm, color='k', ls="-.", lw="1.5", xmax=1)  # Comando para linea horizontal interlineada

    plt.ylim(0, max(ll[0]) + 1)  # Limites para el eje Y
    plt.xlim(0, len(min(ll)))  # Limites para el eje X

    plt.show()



    var = input("Ingrese el tiempo en el que es sistema pasa a estado estacionario ")

    # Color de fondo de la brode de la imagen
    plt.figure().patch.set_facecolor('silver')
    plt.title('Utilizacion promedio del servidor en 5 simulaciones')
    plt.plot(ll[0], 'r', ll[1], 'deeppink', ll[2], 'b', ll[3], 'yellow', ll[4], 'aqua')
    # plt.plot(ll[0], 'lightcoral', ll[1], 'y', ll[2], 'steelblue', ll[3], 'goldenrod', ll[4], 'chocolate')
    plt.xlabel("tiempo")
    plt.ylabel("Utilizacion promedio por servidor")

    # Banda horizontal de y=0 a y=2 de color azul
    # y 30% de transparencia (alpha=0.3)
    plt.axhspan(utilizacionProm - (utilizacionProm * 0.03), utilizacionProm + utilizacionProm * 0.03, alpha=0.8, color='cornflowerblue')

    # Banda vertical de x=0 a x=4 de color amarillo
    # y 30% de transparencia
    plt.axvspan(int(var), len(min(ll)), alpha=0.5, color='y')

    plt.axhline(utilizacionProm, color='k', ls="-.", lw="1.5", xmax=1)  # Comando para linea horizontal interlineada '-.'

    plt.ylim(0, max(ll[0]) + 1)  # Limites para el eje Y

    # Calculo el tamaño minimo de los arreglos para graficar
    minimo = len(ll[0])
    for i in range(1,5):
        x = len(ll[i])
        if x < minimo:
            minimo= x
    plt.xlim(0, minimo)  # Limites para el eje X

    ## Graficos de abajo
    plt.text(200, 0.05, 'Estado transiente', color="k", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
    plt.text(3500, 0.05, 'Estado estacionario', color="b", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})

    #Graficos de cada simulacion
    plt.text(5000, 0.63, 'Corrida 1', color="r", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
    plt.text(5000, 0.56, 'Corrida 2', color="deeppink", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
    plt.text(5000, 0.49, 'Corrida 3', color="b", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
    plt.text(5000, 0.42, 'Corrida 4', color="yellow", style='italic', bbox={'facecolor': 'white', 'alpha': 0.99, 'pad': 5})
    plt.text(5000, 0.35, 'Corrida 5', color="aqua", style='italic', bbox={'facecolor': 'white', 'alpha': 0.99, 'pad': 5})
    plt.show()

def graficarTiempoSistema(ll, utilizacionProm = 0.77):
    plt.figure().patch.set_facecolor('silver')
    plt.title('Tiempo promedio en sistema en 5 simulaciones')
    plt.plot(ll[0], 'r', ll[1], 'deeppink', ll[2], 'b', ll[3], 'yellow', ll[4], 'aqua')
    plt.xlabel("tiempo")
    plt.ylabel("Tiempo promedio en sistema")
    plt.axhspan(utilizacionProm - (utilizacionProm * 0.03), utilizacionProm + utilizacionProm * 0.03, alpha=0.8, color='cornflowerblue')
    plt.axvspan(4000, len(min(ll)), alpha=0.5, color='y')
    plt.axhline(utilizacionProm, color='k', ls="-.", lw="1.5", xmax=1)  # Comando para linea horizontal interlineada

    plt.ylim(0, max(ll[0]) + 1)  # Limites para el eje Y
    minimo = len(ll[0])
    for i in range(1, 5):
        x = len(ll[i])
        if x < minimo:
            minimo = x
    plt.xlim(0, minimo)  # Limites para el eje X

    plt.show()



    var = input("Ingrese el tiempo en el que es sistema pasa a estado estacionario ")

    # Color de fondo de la brode de la imagen
    plt.figure().patch.set_facecolor('silver')
    plt.title('Tiempo promedio en sistema en 5 simulaciones')
    plt.plot(ll[0], 'r', ll[1], 'deeppink', ll[2], 'b', ll[3], 'yellow', ll[4], 'aqua')
    # plt.plot(ll[0], 'lightcoral', ll[1], 'y', ll[2], 'steelblue', ll[3], 'goldenrod', ll[4], 'chocolate')
    plt.xlabel("tiempo")
    plt.ylabel("Tiempo promedio en sistema")

    # Banda horizontal de y=0 a y=2 de color azul
    # y 30% de transparencia (alpha=0.3)
    plt.axhspan(utilizacionProm - (utilizacionProm * 0.03), utilizacionProm + utilizacionProm * 0.03, alpha=0.8, color='cornflowerblue')

    # Banda vertical de x=0 a x=4 de color amarillo
    # y 30% de transparencia
    plt.axvspan(int(var), len(min(ll)), alpha=0.5, color='y')

    plt.axhline(utilizacionProm, color='k', ls="-.", lw="1.5", xmax=1)  # Comando para linea horizontal interlineada '-.'

    plt.ylim(0, max(ll[0]) + 1)  # Limites para el eje Y

    # Calculo el tamaño minimo de los arreglos para graficar
    minimo = len(ll[0])
    for i in range(1,5):
        x = len(ll[i])
        if x < minimo:
            minimo= x
    plt.xlim(0, minimo)  # Limites para el eje X

    ## Graficos de abajo
    plt.text(3000, 1, 'Estado transiente', color="k", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
    plt.text(13000, 1, 'Estado estacionario', color="b", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})

    #Graficos de cada simulacion
    y = 2
    plt.text(15000, y + 1.5, 'Corrida 1', color="r", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
    plt.text(15000, y + 3, 'Corrida 2', color="deeppink", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
    plt.text(15000, y + 4.5, 'Corrida 3', color="b", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
    plt.text(15000, y + 6, 'Corrida 4', color="yellow", style='italic', bbox={'facecolor': 'white', 'alpha': 0.99, 'pad': 5})
    plt.text(15000, y + 7.5, 'Corrida 5', color="aqua", style='italic', bbox={'facecolor': 'white', 'alpha': 0.99, 'pad': 5})
    plt.show()


# ---------------------------------------------
# Ejecución del modelo
# ---------------------------------------------


sim1 = Simulador()
sim1.correr_simulacion()
