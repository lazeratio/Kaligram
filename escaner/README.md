# Kaligram Escaner - xknr

Descripción: Script de escaneo de rangos de IPs modularizable.

Este script permite realizar un escaneo de rangos de IPs aplicando modulos personalizables. De forma resumida su
funcionamiento básico es el siguiente:
 - Obtiene el rango de IPs a escanear
 - Recorre el rango de IPs, aplicando el módulo de procesamiento que se especifique
 - Procesa los datos obtenidos

Cada uno de estos 3 aspectos de funcionamiento son configurables mediante módulos personalizables, que se pueden añadir
en las carpetas de módulos siguientes:

 - *mod_extrators*: módulos de extracción de datos, permiten indicar que acción se realiza en cada IP.
 - *mod_inputs*: módulos de entrada de datos, para poder especificar el origen de los parámetros de ejecución.
 - *mod_output*: módulos de salida o procesamiento de datos, que permiten trabajar con los datos obtenidos.
 - *mod_scanners*: módulos para el proceso de recorrido de los rangos de IPs, que permite especificar el modo en el que
  se hacen las peticiones a las IPs, siendo posible en este punto integrar herramientas externas como NMAP, por ejemplo.

El script principal xknr.py integra los diferentes módulos para realizar el proceso de escaneo completo.

Módulos requeridos para la ejecución del script (Instalar globalmente o en virtualenv con 'pip install <modulo>'):

 - html5lib
 - colorama
 - beautifulsoup4


## EJEMPLO

Escanear rango de IPs 10.66.0.0/24 con los módulos basic, webinfo y csv, con un timeout de 3 seg para cada petición,
sin procesado de salida, una concurrencia de 10 peticiones y modo verbose activado:

```python
 python xknr.py -ip 10.66.0.0/24 -me basic -mx webinfo -mo csv -n -t3 -v -c 10
```
