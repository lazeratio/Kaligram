"""
========================================
===== KALIGRAM XNKR - SCANNER BASE =====
========================================

Escaner de IPs simple que ejecuta un módulo de escaneo en un rango de IPs de forma concurrente.
"""
import concurrent.futures
import colorama

def escanear_rango(lista_ips, modulo_extraccion, timeout=3, num_hilos=5, verbose=False):
    """Escanea un rango de IPs con un modulo determinado.

    + Parametros:

        - lista_ips: lista de IPs a parsear
        - modulo_escaneo: Modulo de extraccion de informacion
        - timeout: Timeout de las peticiones
        - num_hilos: Numero de peticiones concurrentes
        - verbose: Habilitar modo verbose

    + Return:
        - Lista de resultados por IP
        - Lista de errores por IP
    """

    lstResults = []
    numErrores = 0

    # Ejecucion en paralelo de peticiones
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_hilos) as executor:

        futures = {executor.submit(modulo_extraccion, ip, timeout): ip for ip in lista_ips}

        for future in concurrent.futures.as_completed(futures):

            ipval = futures[future]

            try:
                (data, msg, lstExc) = future.result()

            except Exception as exc:
                print('ERROR EN PETICION [{0}: {1}]'.format(ipval, exc))
                continue

            else:
                # Si la respuesta trae algun dato se muestra un resumen
                if not data is None and len(data) > 0:

                    info_txt = dict(data).get('info_txt', '---') # Mostrar info resumen
                    colorMsg = colorama.Fore.WHITE
                    if not msg.startswith("OK"):
                        numErrores = numErrores + 1
                        colorMsg = colorama.Fore.YELLOW

                    if verbose: print('{0}IP {1:16s} {2:8s} {3} {4}'.format(colorama.Fore.GREEN, str(ipval), info_txt, colorMsg, msg))

                    # Se añade el resultado al listado
                    lstResults.append(data)

                # IP sin respuesta
                elif msg.startswith("ERROR_URL") or msg.startswith("KO"):

                    if verbose: print(colorama.Fore.RED +'IP {0:16s} SIN RESPUESTA'.format(str(ipval)))

                # IP sin infomacion valida
                elif msg.startswith("INFO"):

                    if verbose: print(colorama.Fore.YELLOW +'IP {0:16s} SIN INFO VALIDA'.format(str(ipval)))

                # Error generico
                else:

                    if verbose: print(colorama.Fore.RED +'IP {0:16s} ERROR NO GESTIONADO'.format(str(ipval)))

    return lstResults, numErrores



if __name__ == "__main__":

    pass