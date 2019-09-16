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
        print("Servidor quedo en cero")
        # Acumulo el tiempo de servicio
        tiempoServicioTotal += (reloj - tiempoUltEvento)
        listaEventos[1] = 9999999.0


def generarHisotgrama(lista):
    plt.title('Utilizacion promedio del servidor')
    plt.plot(lista)
    plt.xlabel("tiempo")
    plt.ylabel("Utilizacion promedio")
    plt.axhline(0.7, color='k', ls="dotted", xmax=3)  # Comando para linea horizontal constante
    plt.ylim(0, 1)  # Limites para el eje Y
    plt.xlim(0, 1000)  # Limites para el eje X
    plt.show()


def medidasDesempeño():
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
    generarHisotgrama(listaUsoServidores)

def generarTiempoExponencial(media):
    # return np.random.exponential(media)
    return -(1/media) * math.log(random.random())


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
tiempoEntreArribos = 1/10
tiempoDeServicio = 1/7

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
        # print(reloj)

    tiempoUltEvento = reloj

    print(len(cola))
    if reloj >= 15000 :
        break
medidasDesempeño()

