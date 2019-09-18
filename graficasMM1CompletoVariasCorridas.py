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

TIEMPO_SIMULACION = 1000

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
        # Acumulo la demora promedio de clientes en cola para hacer la gráfica de como se llega al tiempo promedio final.
        listaDemoraCola.append(demoraAcumulada / completaronDemora)

    else:
        # Acumulo el tiempo de servicio
        tiempoServicioTotal += (reloj - tiempoUltEvento)

        # Acumulo la utilizacion de cada servidor en t para hacer la grafica de como se llega al promedio de utilización.
        listaUsoServidores.append(tiempoServicioTotal / reloj)

        areaQ += (numCliEnCola * (reloj - tiempoUltEvento))
        numCliEnCola += 1

        # Acumulo el numero promedio de clientes en cola para hacer la gráfica de como se llega al numero promedio final.
        listaNumCliCola.append(areaQ / reloj)

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
        # Acumulo la demora promedio de clientes en cola para hacer la gráfica de como se llega al tiempo promedio final.
        listaDemoraCola.append(demoraAcumulada / completaronDemora)

        # Actualizo el contador de clientes que completaron la demora
        completaronDemora += 1

        # Acumulo el tiempo de servicio
        tiempoServicioTotal += (reloj - tiempoUltEvento)

        # Acumulo la utilizacion de cada servidor en t para hacer la grafica de como se llega al promedio de utilización.
        listaUsoServidores.append(tiempoServicioTotal/reloj)

        # Calculo el Área bajo Q(t) del período anterior (Reloj - TiempoUltimoEvento)
        areaQ += (numCliEnCola * (reloj - tiempoUltEvento))
        numCliEnCola -= 1
        # Acumulo en numero promedio de clientes en cola para hacer la gráfica de como se llega al numero promedio final.
        listaNumCliCola.append(areaQ / reloj)



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

def generarTiempoExponencial(tiempoEA): 
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
listaCorridas1 = []
listaCorridas2 = []
listaCorridas3 = []
listaUsoServidores = []
listaNumCliCola = []
listaDemoraCola = []

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

listaCorridas1.append(listaUsoServidores)
listaCorridas2.append(listaNumCliCola)
listaCorridas3.append(listaDemoraCola)

# 22222222222 ************************************************************************************************************

# Inicializacion de variables
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
listaNumCliCola = []
listaDemoraCola = []

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

    if reloj >= TIEMPO_SIMULACION:  # and numCliEnCola == 0 and estadoServ == 0:
        break

listaCorridas1.append(listaUsoServidores)
listaCorridas2.append(listaNumCliCola)
listaCorridas3.append(listaDemoraCola)

# 3333333333 ************************************************************************************************************

# Inicializacion de variables
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
listaNumCliCola = []
listaDemoraCola = []

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

    if reloj >= TIEMPO_SIMULACION:  # and numCliEnCola == 0 and estadoServ == 0:
        break

listaCorridas1.append(listaUsoServidores)
listaCorridas2.append(listaNumCliCola)
listaCorridas3.append(listaDemoraCola)

# 4444444444 ************************************************************************************************************

# Inicializacion de variables
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
listaNumCliCola = []
listaDemoraCola = []

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

    if reloj >= TIEMPO_SIMULACION:  # and numCliEnCola == 0 and estadoServ == 0:
        break

listaCorridas1.append(listaUsoServidores)
listaCorridas2.append(listaNumCliCola)
listaCorridas3.append(listaDemoraCola)

# 55555555 ************************************************************************************************************

# Inicializacion de variables
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
listaNumCliCola = []
listaDemoraCola = []

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

    if reloj >= TIEMPO_SIMULACION:  # and numCliEnCola == 0 and estadoServ == 0:
        break

listaCorridas1.append(listaUsoServidores)
listaCorridas2.append(listaNumCliCola)
listaCorridas3.append(listaDemoraCola)

# ****************************************************************************************

def graficarPromedio(ll, utilizacionProm = 0.77, titulo = 'Utilizacion promedio del servidor en 5 simulaciones',
                     ejey = "Utilizacion promedio por servidor", ylim = 1, xlim = 0):
    plt.figure().patch.set_facecolor('silver')
    plt.title(titulo)
    plt.plot(ll[0], 'r', ll[1], 'deeppink', ll[2], 'b', ll[3], 'yellow', ll[4], 'aqua')
    plt.xlabel("tiempo")
    plt.ylabel(ejey)
    plt.axhspan(utilizacionProm-(utilizacionProm*0.10), utilizacionProm+utilizacionProm*0.10, alpha=0.8, color='cornflowerblue')
    plt.axvspan(4000, len(min(ll)), alpha=0.5, color='y')
    plt.axhline(utilizacionProm, color='k', ls="-.", lw="1.5", xmax=1)  # Comando para linea horizontal interlineada
    minimo = len(ll[0])
    for i in range(1, 5):
        x = len(ll[i])
        if x < minimo:
            minimo = x
    plt.ylim(0, 4)  # Limites para el eje Y
    plt.xlim(0, minimo)  # Limites para el eje X

    plt.show()



    var = input("Ingrese el tiempo ")

    # Color de fondo de la borde de la imagen
    plt.figure().patch.set_facecolor('silver')
    plt.title(titulo)
    plt.plot(ll[0], 'r', ll[1], 'deeppink', ll[2], 'b', ll[3], 'yellow', ll[4], 'aqua')
    # plt.plot(ll[0], 'lightcoral', ll[1], 'y', ll[2], 'steelblue', ll[3], 'goldenrod', ll[4], 'chocolate')
    plt.xlabel("tiempo")
    plt.ylabel(ejey)

    # Banda horizontal de y=0 a y=2 de color azul
    # y 30% de transparencia (alpha=0.3)
    plt.axhspan(utilizacionProm-(utilizacionProm*0.10), utilizacionProm+utilizacionProm*0.10, alpha=0.8, color='cornflowerblue')

    # Banda vertical de x=0 a x=4 de color amarillo
    # y 30% de transparencia

    plt.axhline(utilizacionProm, color='k', ls="-.", lw="1.5", xmax=1)  # Comando para linea horizontal interlineada '-.'


    # Calculo el tamaño minimo de los arreglos para graficar
    minimo = len(ll[0])
    for i in range(1,5):
        x = len(ll[i])
        if x < minimo:
            minimo= x
    plt.xlim(0, minimo)  # Limites para el eje X
    plt.ylim(0, 4)  # Limites para el eje Y

    plt.axvspan(int(var), (minimo + 2000), alpha=0.5, color='y')

    ## Graficos de abajo
    plt.text(600, 0.2, 'Estado transiente', color="k", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
    plt.text(6500, 0.2, 'Estado estacionario', color="b", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})

    #Graficos de cada simulacion
    plt.text(800, 1.1, 'Corrida 1', color="r", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
    plt.text(3000, 1.1, 'Corrida 2', color="deeppink", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
    plt.text(5000, 1.1, 'Corrida 3', color="b", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
    plt.text(800, 0.65, 'Corrida 4', color="yellow", style='italic', bbox={'facecolor': 'white', 'alpha': 0.99, 'pad': 5})
    plt.text(3000, 0.65, 'Corrida 5', color="aqua", style='italic', bbox={'facecolor': 'white', 'alpha': 0.99, 'pad': 5})
    plt.show()


# var1 = tiempoServicioTotal/reloj
var2 = demoraAcumulada / completaronDemora
var3 = areaQ/reloj
#
# print("Promedio de utilizacion del serivdor: " + str(var1))
# graficarPromedio(listaCorridas1, var1)

# print("Promedio de tiempo en cola: " + str(var2))
# t1 = 'Tiempo promedio de clientes en cola en 5 simulaciones'
# t2 = "Tiempo clientes en promedio en cola"
# graficarPromedio(listaCorridas3, var2, t1,t2)
#
#
#
t4 = "Cantidad de clientes promedio en cola"
t3 = 'Número promedio de clientes en cola en 5 simulaciones'
print("Promedio de numero de clientes en cola: " + str(var3))
graficarPromedio(listaCorridas2, var3, t3, t4, 3, 21000)

def graficarPromediosNumCola(lista, promedioNumCola = 0.77):
    plt.figure().patch.set_facecolor('silver')
    plt.title('Número promedio de clientes en cola')
    plt.plot(lista, color='r')
    plt.xlabel("tiempo")
    plt.ylabel("Número promedio en cola")
    plt.text(0.3 * len(lista), 0.83*(max(lista) + 1), 'Número promedio de clientes en cola: %.2f' % promedioNumCola, color="r", style='italic', bbox={'facecolor': 'white', 'alpha': 0.90, 'pad': 5})
    plt.axhline(promedioNumCola, color='r', ls="-.", xmax=3)  # Comando para linea horizontal constante
    plt.ylim(0, max(lista) + 1)  # Limites para el eje Y
    plt.xlim(0, len(lista) + 2000)  # Limites para el eje X
    plt.show()


# graficarPromediosNumCola(listaCorridas2[0], var3)
# graficarPromediosNumCola(listaCorridas2[1], var3)
# graficarPromediosNumCola(listaCorridas2[2], var3)
# graficarPromediosNumCola(listaCorridas2[3], var3)
# graficarPromediosNumCola(listaCorridas2[4], var3)
