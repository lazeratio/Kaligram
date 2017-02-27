"""
===== KALIGRAM XNKR =====

Descripcion: Escaner de IPs con extracción de informacion mediante modulos personalizados para diferentes tipos de
informacion a extraer.
"""

import argparse
import sys
from pprint import pprint

import colorama

def inicializar():
    """
    Funcion de inicializacion del programa:
     - Inicializa los modulos que lo requieran
     - Procesa los parametros de entrada y devuelve al metodo llamante los objetos de ejecucion
    """

    #  === INICIALIZACION DE MODULOS ===

    # Inicializacion del modulo colorama para salida formateada
    colorama.init(autoreset=True)

    #  === PARAMETROS  DE ENTRADA ===
    # Procesamiento de argumentos de entrada
    (modulo_escaneo, lstIPs, argumentos) = procesar_argumentos()

    if argumentos.verbose:
        print("Lista de IPs que se van a escanear:")
        pprint([str(x) for x in lstIPs])

        if argumentos.limit > 0:
            print("  Rango  limitado a {} IPs".format(argumentos.limit))

    return (modulo_escaneo, lstIPs, argumentos)



def procesar_argumentos():
    "Configura y obtiene los parametros de ejecucion"
    parser = argparse.ArgumentParser(description='Parseo de rango de IPs para extracción de información')
    groupOpt = parser.add_argument_group('Opciones')
    groupInfo = parser.add_argument_group('Info')
    parser.add_argument('-ip', action='append', dest='ip', help='IP (a.b.c.d) o rango de IPs (a.b.c.d/m) a escanear')
    groupOpt.add_argument('-t','--timeout', action='store', dest='timeout', help='Timeout de las conexiones en segundos (por defecto 3s)', type=int, default=3)
    groupOpt.add_argument('-c','--concurrent', action='store', dest='concurrent', help='Número de IPs a escanear en paralelo (por defecto 5)', type=int, default=5)
    groupOpt.add_argument('-m','--module', action='store', dest='module', help='Módulo a aplicar al escaneo (ver disponibles con opción -lm)')
    groupOpt.add_argument('-li','--limit', action='store', dest='limit', help='Limite de número de IPs a escanear', type=int, default=0)
    groupOpt.add_argument('-n','--nofiles', action='store_true', dest='nofile', help='No generar ficheros de salida')
    groupInfo.add_argument('-lm','--listmodules', action='store_true', dest='listmodules', help='Listar módulos de escaneo disponibles')
    groupInfo.add_argument('-v','--verbose', action='store_true', dest='verbose', help='Mostrar información del proceso de escaneo')
    argumentos = parser.parse_args()

    if argumentos.listmodules:
        mostrar_info_modulos()
        sys.exit(0)

    if argumentos.ip is None or len(argumentos.ip) == 0 :
        parser.print_help()
        sys.exit(0)

    modulo_escaneo = validar_modulo(argumentos.module)

    if modulo_escaneo is None and len(sys.argv) > 1:
        print('Módulo no válido, ver modulos disponibles con opción -lm')
        sys.exit(0)

    #lstIPs = obtener_lista_ips(argumentos)
    lstIPs = []

    if len(lstIPs)==0: sys.exit(0)

    return (modulo_escaneo, lstIPs, argumentos)


def mostrar_info_modulos():
    "Muestra info de los modulos disponibles"
    print('Módulos disponibles:' )
    print(' {0}modulo{1}: Desc modulo'.format(colorama.Fore.YELLOW, colorama.Fore.RESET) )


def validar_modulo(modulo):
    "Valida que los valores de los modulos sean correctos, devolviendo el modulo que corresponda"

    return True


# ===========================================
# RUTINA PRINCIPAL
# ===========================================

def main():

    (modulo_escaneo, lstIPs, argumentos) = inicializar()

    print(" ")





if __name__ == "__main__":

    #Process(target=main).start()

    main()