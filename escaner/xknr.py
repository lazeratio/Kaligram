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

from mod_scanners import xknr_scanner
from mod_extractors import xknr_ex_webinfo
from mod_extractors import xknr_ex_cisco78xx
from mod_output import xknr_out_csv

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
    (modulo_escaneo, modulo_extraccion, modulo_salida, lstIPs, argumentos) = procesar_argumentos()

    if argumentos.verbose:
        print("Lista de IPs que se van a escanear:")
        pprint([str(x) for x in lstIPs])

        if argumentos.limit > 0:
            print("  Rango  limitado a {} IPs".format(argumentos.limit))

    return (modulo_escaneo, modulo_extraccion, modulo_salida, lstIPs, argumentos)



def procesar_argumentos():
    "Configura y obtiene los parametros de ejecucion"
    parser = argparse.ArgumentParser(description='Parseo de rango de IPs para extracción de información')
    groupOpt = parser.add_argument_group('Opciones')
    groupInfo = parser.add_argument_group('Info')
    parser.add_argument('-ip', action='append', dest='ip', help='IP (a.b.c.d) o rango de IPs (a.b.c.d/m) a escanear')
    groupOpt.add_argument('-t','--timeout', action='store', dest='timeout', help='Timeout de las conexiones en segundos (por defecto 3s)', type=int, default=3)
    groupOpt.add_argument('-c','--concurrent', action='store', dest='concurrent', help='Número de IPs a escanear en paralelo (por defecto 5)', type=int, default=5)
    groupOpt.add_argument('-mx','--modulo_ext', action='store', dest='modulo_ext', help='Módulo de escaneo a aplicar (ver disponibles con opción -lm)')
    groupOpt.add_argument('-me','--modulo_esc', action='store', dest='modulo_esc', help='Módulo de extracción a aplicar al escaneo (ver disponibles con opción -lm)')
    groupOpt.add_argument('-mo','--modulo_out', action='store', dest='modulo_out', help='Módulo de salida a aplicar a lso datos escaneados (ver disponibles con opción -lm)')
    groupInfo.add_argument('-lm','--listmodules', action='store_true', dest='listmodules', help='Listar módulos disponibles')
    groupOpt.add_argument('-li','--limit', action='store', dest='limit', help='Limite de número de IPs a escanear', type=int, default=0)
    groupOpt.add_argument('-n','--nofiles', action='store_true', dest='nofile', help='No generar ficheros de salida')
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
    f_modulo_escaneo = obtener_funcion_modulo(argumentos.modulo_esc, 'esc')
    f_modulo_extraccion = obtener_funcion_modulo(argumentos.modulo_ext, 'ext')
    f_modulo_salida = obtener_funcion_modulo(argumentos.modulo_out, 'out')

    if (f_modulo_escaneo is None or f_modulo_salida is None or f_modulo_extraccion is None) and len(sys.argv) > 1:
        print('Módulos no válidos, ver modulos disponibles con opción -lm')
        sys.exit(0)

    lst_ips = obtener_lista_ips(argumentos)

    if len(lst_ips)==0:
        print('No hay IPs a escanear')
        sys.exit(0)

    # Devuelve el modulo de escaneo, la lista de IPs y los parametros de ejecucion
    return (f_modulo_escaneo, f_modulo_extraccion, f_modulo_salida, lst_ips, argumentos)


def obtener_lista_ips(args):
    "Obtiene la lista de IPs a procesar"
    lst_ips = []

    # Preparacion de rango de IPs
    for x in args.ip :

        lst_ips_aux = []

        try:
            ip = ipaddress.ip_address(x)
            lst_ips_aux.append(ip)
        except ValueError:
            pass

        if (len(lst_ips_aux ) == 0):
            try:
                ip = ipaddress.ip_network(x, strict=False)
                lst_ips_aux = list(ip.hosts())
            except ValueError:
                print('Error: IP no válida: {0}'.format(x))
                sys.exit(0)

        lst_ips = lst_ips + lst_ips_aux

    lst_ips = sorted(list(set(lst_ips))) # Eliminacion de posibles duplicados

    if args.limit > 0: # Aplica el limite al numero de IPs
        del lst_ips[args.limit:]

    return lst_ips

def mostrar_info_modulos():
    "Muestra info de los modulos de extraccion disponibles"

    print('Módulos de escaneo disponibles:' )
    print(' {0}basic{1}: Escaneo simple con peticiones concurrentes'.format(colorama.Fore.YELLOW, colorama.Fore.RESET))
    print('Módulos de extraccion disponibles:' )
    print(' {0}webinfo{1}: Info basica de página web '.format(colorama.Fore.YELLOW, colorama.Fore.RESET))
    print(' {0}cisco78xx{1}: Telefonos IP Cisco 78xx'.format(colorama.Fore.YELLOW, colorama.Fore.RESET) )
    print('Módulos de salida disponibles:' )
    print(' {0}csv{1}: Salida a fichero CSV'.format(colorama.Fore.YELLOW, colorama.Fore.RESET))


def obtener_funcion_modulo(modulo, tipo):
    "Valida que los valores de los modulos sean correctos, devolviendo el modulo que corresponda"

    modulos_ex = {
        'webinfo': xknr_ex_webinfo.parse,
        'cisco78xx': xknr_ex_cisco78xx.parse,
    }

    modulos_esc = {
        'basic': xknr_scanner.escanear_rango
    }

    modulos_out = {
        'csv': xknr_out_csv.procesar_datos
    }

    tipos_modulo = {
        "ex": modulos_ex,
        "esc": modulos_esc,
        "out": modulos_out
    }

    tipo_modulo =  tipos_modulo.get(tipo, None)

    if (tipo_modulo is None):
        return None

    return tipo_modulo.get(modulo, None)



# ===========================================
# RUTINA PRINCIPAL
# ===========================================

def main():

    # Obtencion de parametros para la ejecución
    (f_modulo_escaneo, f_modulo_extraccion, f_modulo_salida, lst_ips, argumentos) = inicializar()

    print(" ")

    (lst_results,num_errores) = f_modulo_escaneo(lst_ips, f_modulo_extraccion, timeout=argumentos.timeout, num_hilos=argumentos.concurrent, verbose=True)

    print(" ")

    if len(lst_results)==1:
        print("==== [{0}DATOS EXTRAIDOS] ====".format(colorama.Fore.WHITE))
        for x in lst_results[0]:
            print("  {0}{1}: {2}{3}".format(colorama.Fore.CYAN,x[0],colorama.Fore.YELLOW,x[1]))
        print(" ")

    # Resultado del escaneo
    print("==== [RESUMEN DE ESCANEO] ====".format(colorama.Fore.CYAN))
    print('  IPs escaneadas: {0}'.format(len(lst_ips)))
    print('  IPs con respuesta: {0}{1}'.format(colorama.Fore.GREEN, len(lst_results)))
    print('  IPs sin respuesta: {0}{1}'.format(colorama.Fore.YELLOW, num_errores))

    if len(lst_results)>0 and not argumentos.nofile :
        f_modulo_salida(lst_results)


if __name__ == "__main__":

    #Process(target=main).start()

    main()