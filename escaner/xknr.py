"""
=========================
===== KALIGRAM XNKR =====
=========================

Descripcion: Escaner de IPs con extracción de informacion mediante modulos personalizados para diferentes tipos de
informacion a extraer.
"""

import argparse
import sys
import ipaddress
import colorama
from pprint import pprint

from escaner.mod_scanners import xknr_scanner


# ===========================================
# FUNCIONES AUXILIARES
# ===========================================

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

    # Listar modulos disponibles
    if argumentos.listmodules:
        mostrar_info_modulos()
        sys.exit(0)

    # Sin argumentos
    if argumentos.ip is None or len(argumentos.ip) == 0 :
        parser.print_help()
        sys.exit(0)

    # Validacion
    modulo_escaneo = validar_modulo(argumentos.module)

    if modulo_escaneo is None and len(sys.argv) > 1:
        print('Módulo no válido, ver modulos disponibles con opción -lm')
        sys.exit(0)

    lstIPs = obtener_lista_ips(argumentos)
    lstIPs = []

    if len(lstIPs)==0: sys.exit(0)

    # Devuelve el modulo de escaneo, la lista de IPs y los parametros de ejecucion
    return (modulo_escaneo, lstIPs, argumentos)


def obtener_lista_ips(args):
    "Obtiene la lista de IPs a procesar"
    lstIPs = []

    # Preparacion de rango de IPs
    for x in args.ip :

        lstIPaux = []

        try:
            ip = ipaddress.ip_address(x)
            lstIPaux.append(ip)
        except ValueError:
            pass

        if (len(lstIPaux ) == 0):
            try:
                ip = ipaddress.ip_network(x, strict=False)
                lstIPaux = list(ip.hosts())
            except ValueError:
                print('Error: IP no válida: {0}'.format(x))
                sys.exit(0)

        lstIPs = lstIPs + lstIPaux

    lstIPs = sorted(list(set(lstIPs))) # Eliminacion de posibles duplicados

    if args.limit > 0: # Aplica el limite al numero de IPs
        del lstIPs[args.limit:]

    return lstIPs

def mostrar_info_modulos():
    "Muestra info de los modulos de extraccion disponibles"
    print('Módulos de extraccion disponibles:' )
    print(' {0}modulo{1}: Desc modulo'.format(colorama.Fore.YELLOW, colorama.Fore.RESET) )


def validar_modulo(modulo):
    "Valida que los valores de los modulos sean correctos, devolviendo el modulo que corresponda"

    return True


# ===========================================
# RUTINA PRINCIPAL
# ===========================================

def main():

    # Obtencion de parametros para la ejecución
    (modulo_escaneo, lstIPs, argumentos) = inicializar()

    print(" ")

    (lstResults,numErrores) =  xknr_scanner.escanear_rango(lstIPs, modulo_escaneo, timeout=argumentos.timeout, num_hilos=argumentos.concurrent, verbose=True)

    print(" ")

    if len(lstResults)==1:
        print("==== [{0}DATOS EXTRAIDOS] ====".format(colorama.Fore.WHITE))
        for x in lstResults[0]:
            print("  {0}{1}: {2}{3}".format(colorama.Fore.CYAN,x[0],colorama.Fore.YELLOW,x[1]))
        print(" ")

    # Resultado del escaneo
    print("==== [RESUMEN DE ESCANEO] ====".format(colorama.Fore.CYAN))
    print('  IPs escaneadas: {0}'.format(len(lstIPs)))
    print('  IPs con respuesta: {0}{1}'.format(colorama.Fore.GREEN, len(lstResults)))
    print('  IPs con formato no válido: {0}{1}'.format(colorama.Fore.YELLOW, numErrores))



if __name__ == "__main__":

    #Process(target=main).start()

    main()