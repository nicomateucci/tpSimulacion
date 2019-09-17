# Simulador de sistema  M/M/1.
#
# Variables de respuesta:
# - Demora promedio por cliente
# - Número promedio de clientes en cola
# - Utilización promedio de cliente
#
# Funciones:
#     arribo()
#     partida()
#     nuevoEvento()
#     medidasDesempeño()
#     generarTiempoExponencial(t)
#     generarHisotgrama(lista)

TIEMPO_SIMULACION = 500
import numpy as np
import random
import math
import matplotlib.pyplot as plt

def arribo():

    global reloj
    global tiempoUltEvento
    global estadoServ
    global tiempoServicioTotal
    global areaQ
    global numCliEnCola
    global cola
    global tiempoLibre
    global completaronDemora

    # Siguiente arribo
    listaEventos[0] = reloj + generarTiempoExponencial(tiempoEntreArribos)


    if estadoServ == 0:
        # Servidor pasa a 1, ocupado
        estadoServ = 1
        tiempoLibre += reloj - tiempoUltEvento
        # Programo el próximo evento partida
        listaEventos[1] = reloj + generarTiempoExponencial(tiempoDeServicio)

        # Actualizo la cantidad de clientes que completaron la demora
        completaronDemora += 1

    else:
        # Acumulo el tiempo de servicio
        tiempoServicioTotal += (reloj - tiempoUltEvento)

        # Acumulo la utilizacion de cada servidor en t para hacer la grafica de como se llega al promedio de utilización.
        listaUsoServidores.append(tiempoServicioTotal / reloj)

        areaQ += (numCliEnCola * (reloj - tiempoUltEvento))
        numCliEnCola += 1

        # Agrego el cliente a la cola
        cola.append(reloj)

def partida():

    global numCliEnCola
    global tiempoServicioTotal
    global areaQ
    global demoraAcumulada
    global completaronDemora
    global estadoServ
    global listaUsoServidores

    if numCliEnCola > 0:



        # Proxima partida
        listaEventos[1] = reloj + generarTiempoExponencial(tiempoDeServicio)
        # Acumulo la demora acumulada como el valor actual del reloj
        # menos el valor del reloj cuando el cliente ingresó a la cola

        demoraAcumulada += reloj - cola[0]

        # Actualizo el contador de clientes que completaron la demora
        completaronDemora += 1

        # Acumulo el tiempo de servicio
        tiempoServicioTotal += (reloj - tiempoUltEvento)

        # Acumulo la utilizacion de cada servidor en t para hacer la grafica de como se llega al promedio de utilización.
        listaUsoServidores.append(tiempoServicioTotal/reloj)

        # Calculo el Área bajo Q(t) del período anterior (Reloj - TiempoUltimoEvento)
        areaQ += (numCliEnCola * (reloj - tiempoUltEvento))
        numCliEnCola -= 1

        # Desplazo  todos los valores una posición hacia adelante
        cola.pop(0)
    else:
        # Al no haber clientes en cola, establezco el estado del servidor en "Desocupado"
        estadoServ = 0
        # Acumulo el tiempo de servicio
        tiempoServicioTotal += (reloj - tiempoUltEvento)

        # Acumulo la utilizacion de cada servidor en t para hacer la grafica de como se llega al promedio de utilización.
        listaUsoServidores.append(tiempoServicioTotal / reloj)
        listaEventos[1] = 9999999.0





def medidasDesempeño():
    global listaUsoServidores
    global reloj
    global tiempoLibre
    global areaQ
    global tiempoServicioTotal
    global demoraAcumulada
    global completaronDemora

    print("Medidas de desempeño de la simulación: ")
    print("TIEMPO LIBRE DEL SERVIDOR %s" % tiempoLibre)
    print("PORCENTAJE DE TIEMPO LIBRE %s" % (tiempoLibre / reloj))
    print()
    print("El reloj quedo en ", reloj)

    var1 = areaQ / reloj
    print("Nro promedio de cli en cola:", var1)

    var2 = tiempoServicioTotal / reloj
    print("Utilización promedio de los servidores:", var2)

    var3 = demoraAcumulada / completaronDemora
    print("Demora promedio por cliente:", var3)
    graficarPromedio(listaUsoServidores, var2)

def generarTiempoExponencial(tiempoEA):
    # return np.random.exponential(media)
    return -(1 / tiempoEA) * math.log(random.random())


def nuevoEvento():

    global reloj
    global proximoEvento
    global listaEventos

    if listaEventos[0] <= listaEventos[1]:
        reloj = listaEventos[0]
        proximoEvento = "ARRIBO"
    else:
        reloj = listaEventos[1]
        proximoEvento = "PARTIDA"

#Inicio del programa principal
#Tiempo de arribo y servicio del modelo:
tiempoEntreArribos = 7
tiempoDeServicio = 9

#Inicializacion de variables
reloj = 0.0
estadoServ = 0
tiempoServicioTotal = 0.0
tiempoLibre = 0.0
demoraAcumulada = 0.0
proximoEvento = ""
listaEventos = []
cola = []
numCliEnCola = 0
areaQ = 0.0
tiempoUltEvento = 0.0
completaronDemora = 0
listaUsoServidores = []
listaCorridas = []

# Tiempo primer evento (arribo)
listaEventos.append(generarTiempoExponencial(tiempoEntreArribos))
#
# Infinito, ya que todavia no hay clientes en el sistema
listaEventos.append(9999999.0)

while True:
    nuevoEvento()

    # Llamada a la rutina correspondiente en función del tipo de evento
    if proximoEvento == "ARRIBO":
        arribo()
    else:
        partida()

    tiempoUltEvento = reloj

    if reloj >= TIEMPO_SIMULACION: #and numCliEnCola == 0 and estadoServ == 0:
        break

listaCorridas.append(listaUsoServidores)

reloj = 0.0
estadoServ = 0
tiempoServicioTotal = 0.0
tiempoLibre = 0.0
demoraAcumulada = 0.0
proximoEvento = ""
listaEventos = []
cola = []
numCliEnCola = 0
areaQ = 0.0
tiempoUltEvento = 0.0
completaronDemora = 0
listaUsoServidores = []

# Tiempo primer evento (arribo)
listaEventos.append(generarTiempoExponencial(tiempoEntreArribos))
#
# Infinito, ya que todavia no hay clientes en el sistema
listaEventos.append(9999999.0)

while True:
    nuevoEvento()

    # Llamada a la rutina correspondiente en función del tipo de evento
    if proximoEvento == "ARRIBO":
        arribo()
    else:
        partida()

    tiempoUltEvento = reloj

    if reloj >= TIEMPO_SIMULACION: #and numCliEnCola == 0 and estadoServ == 0:
        break

listaCorridas.append(listaUsoServidores)

reloj = 0.0
estadoServ = 0
tiempoServicioTotal = 0.0
tiempoLibre = 0.0
demoraAcumulada = 0.0
proximoEvento = ""
listaEventos = []
cola = []
numCliEnCola = 0
areaQ = 0.0
tiempoUltEvento = 0.0
completaronDemora = 0
listaUsoServidores = []

# Tiempo primer evento (arribo)
listaEventos.append(generarTiempoExponencial(tiempoEntreArribos))
#
# Infinito, ya que todavia no hay clientes en el sistema
listaEventos.append(9999999.0)

while True:
    nuevoEvento()

    # Llamada a la rutina correspondiente en función del tipo de evento
    if proximoEvento == "ARRIBO":
        arribo()
    else:
        partida()

    tiempoUltEvento = reloj

    if reloj >= TIEMPO_SIMULACION: #and numCliEnCola == 0 and estadoServ == 0:
        break

listaCorridas.append(listaUsoServidores)

reloj = 0.0
estadoServ = 0
tiempoServicioTotal = 0.0
tiempoLibre = 0.0
demoraAcumulada = 0.0
proximoEvento = ""
listaEventos = []
cola = []
numCliEnCola = 0
areaQ = 0.0
tiempoUltEvento = 0.0
completaronDemora = 0
listaUsoServidores = []

# Tiempo primer evento (arribo)
listaEventos.append(generarTiempoExponencial(tiempoEntreArribos))
#
# Infinito, ya que todavia no hay clientes en el sistema
listaEventos.append(9999999.0)

while True:
    nuevoEvento()

    # Llamada a la rutina correspondiente en función del tipo de evento
    if proximoEvento == "ARRIBO":
        arribo()
    else:
        partida()

    tiempoUltEvento = reloj

    if reloj >= TIEMPO_SIMULACION: #and numCliEnCola == 0 and estadoServ == 0:
        break

listaCorridas.append(listaUsoServidores)

reloj = 0.0
estadoServ = 0
tiempoServicioTotal = 0.0
tiempoLibre = 0.0
demoraAcumulada = 0.0
proximoEvento = ""
listaEventos = []
cola = []
numCliEnCola = 0
areaQ = 0.0
tiempoUltEvento = 0.0
completaronDemora = 0
listaUsoServidores = []

# Tiempo primer evento (arribo)
listaEventos.append(generarTiempoExponencial(tiempoEntreArribos))
#
# Infinito, ya que todavia no hay clientes en el sistema
listaEventos.append(9999999.0)

while True:
    nuevoEvento()

    # Llamada a la rutina correspondiente en función del tipo de evento
    if proximoEvento == "ARRIBO":
        arribo()
    else:
        partida()

    tiempoUltEvento = reloj

    if reloj >= TIEMPO_SIMULACION: #and numCliEnCola == 0 and estadoServ == 0:
        break


def graficarPromedio(ll, utilizacionProm = 0.77):
    plt.figure().patch.set_facecolor('silver')
    plt.title('Utilizacion promedio del servidor en 5 corridas distintas')
    plt.plot(ll[0], 'r', ll[1], 'deeppink', ll[2], 'b', ll[3], 'yellow', ll[4], 'aqua')
    plt.xlabel("tiempo")
    plt.ylabel("Utilizacion promedio por servidor")
    plt.axhspan(utilizacionProm-0.03, utilizacionProm+0.03, alpha=0.8, color='cornflowerblue')
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
    plt.axhspan(utilizacionProm - 0.03, utilizacionProm + 0.03, alpha=0.8, color='cornflowerblue')

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


listaCorridas.append(listaUsoServidores)

print("Promedio de utilizacion del serivdor: " + str(tiempoServicioTotal/reloj))
graficarPromedio(listaCorridas, tiempoServicioTotal/reloj)


