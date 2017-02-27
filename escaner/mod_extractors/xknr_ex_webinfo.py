"""
==== XKNR - EXTRACTOR - WEB Info ====

Módulo para la extracción de información basica de páginas web.
"""

import urllib.request, urllib.error, html5lib
from bs4 import BeautifulSoup
import re

def parse(ip,timeout=5):
    """
    :param ip: IP a parsear
    :param timeout: Timeout de a conexion
    :return: Valores de configuración del terminal
    """

    lstData = []
    lstErrores = []
    msgResult = ''

    # URL a escanear
    url = "http://" + str(ip) # Pagina principal

    # ==== Datos de pagina principal (si falla esta pagina no se procesan el resto) ====
    try:
        req = urllib.request.urlopen(url,timeout=timeout)
        html = req.read()
        soup = BeautifulSoup(html,'html5lib')

        # La informacion esta en la tabla 3
        hdrInfo = soup.find_all('header')
        hdrInfo = hdrInfo[0] if len(hdrInfo) > 0 else None

        if not hdrInfo is None and len(hdrInfo) > 0:

            lstData.append(("modulo","webinfo"))
            lstData.append(("ip",str(ip)))

            # Funciones para la busqueda de textos en las llamadas a beutifulsoup
            f1 = lambda val,elt: val in elt.string.strip()
            f2 = lambda val,elt: val in elt.string.strip().lower()

            # Lista de pares (nombre a dar al campo en los resultados, funcion de busqueda de cadena de texto para beautifulsoup)
            lstMapeo = [("titulo", lambda x: f1("title",x))]

            for elt in lstMapeo:
                f = elt[1]
                v="titulo"
                #v = hdrInfo.find_all(string=f)
                #v = v[0].parent.parent.next_sibling.next_sibling.string.strip() if len(v) > 0 else '---'
                lstData.append((elt[0], v))

            msgResult =  'OK'

        else:
            msgResult =  'NO INFO [{0}: {1}]'.format("Pagina Base", url)

    except urllib.error.URLError as exc:
        # print("[%s] %s" % (ip, str(exc.reason)))
        msgResult = 'ERROR_URL [{0}: {1}]'.format("Pagina Base", url)
        lstErrores.append(exc)
        return (lstData, msgResult, lstErrores)
    except Exception as exc:
        msgResult = 'ERROR [{0}: {1}]'.format("Pagina Base", url)
        lstErrores.append(exc)
        return (lstData, msgResult, lstErrores)

    else:
        # Si no se recuperan datos se devuelve unna lista vacía
        if len(lstData) == 0: # Equivalente a PROBLEMA DATOS
            return (lstData, msgResult, lstErrores)


    return lstData, msgResult, lstErrores


def buscarTexto(patron,txt):

    res = ''
    p = re.compile(patron)
    matches = p.search(txt)

    if not matches is None:
        grupos = matches.groups()
        if len(grupos)>0:
            res = grupos[0]

    return res


if __name__ == "__main__":

    pass