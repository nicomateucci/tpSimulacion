<h1 align="center">
  <img src="assets/img/UTN.png" alt="logo_utn">
</h1>
<h5 align="center">Universidad Tecnologica Nacional</h5>

# Trabajo practico integrador


## Simulación de Red de Colas

**Materia: Simulación**
**Profesor: Juan Ignacio Torres**

#### Programar en Pyhton un simulador de un sistema de res de colas como se  describe en la siguiente imagen:
_Imagen del sistema_

![Imagen del Sistema](assets/img/TPSimulacion.png)

~~#### Finalizado el primer punto, se le aplico una mejora al sistema, agregandole una cola intermedia mas  rapida, a la que se le asigna el 30% de los clientes que salen de los dos primeros servidores.~~

### Comparacion de resultados

| Medidas | Sistema inicial | Sistema con mejora|
| :------- | :------: | -----: |
| Utilizacion servidor 1   | 70.9| 69.9|
| N° Prom clientes cola 1  | 1.79| 1.72|
| Utilizacion servidor 2   | 51.1| 50.66|
| N° Prom clientes cola 2  | 0.53 | 0.49|
| Utilizacion servidor 3   | 50.98| 53.2|
| Utilizacion servidor 4   | 30.51 | 33.61|
| Utilizacion servidor 5   | 17.5 | 19.6   |
| N° Prom clientes cola intermedia  | 0.16 | 0.08|
| N° Prom clientes cola rapida  | -- | 0.04|
| Tiempo Prom en el sistema  | 13.26| 12.48|


## Simulador Online

[M/M/C Supositorio.com](https://www.supositorio.com/rcalc/rcalclite_esp.htm)

## Funcionamiento del programa: redesColasFIFO.py

El programa consta de dos clases con sus respsectivos atributos:

**Servidor**

* arribo
* partida
* arribo_grupo2
* partida_grupo2
* nuevoEvento
* medidasDesempeño
	
**Simulacion**

* minimo
* nuevo_evento_global
* correr_simulacion (Metodo principal)
* estadisticas_simulacion

**Metodos de clase**

* actualizar_lista_eventos
* actualizar_tiempo_en_sistema(cls, t)
 
 **Variables de clase**
 
* Cantidad_clientes_en_sistema
* Tiempo_clientes_en_sistema
* Lista_eventos
* Cola_intermedia 
* Completaron_demora
* Demora_acumulada
* AreaQ

El programa funciona a partir de una lista de eventos general, la cual almacena el proximo evento que ecurre en cada servidor. Estos son: arribos y partidas en cada uno de los 5 servidor, donde los arribos de los ultimos 3 se generan solo si se produce una partida en uno de los dos primeros servidores y ademas, alguno de los servidores 3, 4 o 5 estan libres.
La funcionalidad de los servidores 1 y 2 es la misma que se presento en el trabajo practico de cola simple, ya que cada uno de estos es un sistema de colas simple independiente.
Para la cola intermedia se utilizo una variable de clase, en la clase Simulacion, a la que los servidores tiene acceso para agregar o sacar clientes.

**Ejecucion del programa**

Cuando se ejecuta el metodo **correr_simulacion**, se inicializan las variables y se ingresa a un bucle while que termina cuando llega al tiempo definido de la simulacion.
Dentro del bucle, primero se llama al metodo **nuevo_evento**, que a partir del metodo **minimo**( Que generar un nuevo evento bajo el supuesto de que nunca va a haber dos eventos en el mismo instante,   ya que la funcion que retorna los numeros aleatorios de 16 decimales. ), devuelve el número servidor en el que se produce el proximo evento.
Luego, en caso de que el servidor invlucrado sea el 1 o el 2, se llama a sus respectivos metodos para procesar un nuevo evento. Estos al finalizar, modifican la variable de clase del objeto Simulacion que contiene las lista de eventos global.
En caso de producirse un partida, automaticamente se agrega a la cola intermedia para que, en caso de que algunos de los servidores 3, 4 o 5 esten libres, se encarguen de procesar el esa partida como un nuevo arribo.
Por ultimo, se llama al metodo **estadisticas_simulacion**, que muestra el valor de los estadisticos obtenidos y ademas llema a los metodos respectivos para mostrar sus estadisticas de los servidores 1 y 2 (Que consisten en sistemas M/M/1 independientes).

## Clonar archivos con Git

_En caso de no tener instalado Git, descargar desde 
[aca (Descargar Git Windows)](https://git-scm.com/download/win) - Link a [pagina oficial](https://git-scm.com/downloads) de Git_

**Para instalar dejar todo por DEFAULT y poner todo "Siguiente".**

_Para Linux:_
```
 sudo apt-get install git
```

### Comando para clonar la carpeta en PC:

```
git clone https://github.com/nicomateucci/tpSimulacion
```
_Se puede hacer desde la consola de Pycharm._