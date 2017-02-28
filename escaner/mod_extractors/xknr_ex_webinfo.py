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

        # Se extrae la info de la pagina
        title_tag = soup.title

        lstData.append(("modulo", "webinfo"))
        lstData.append(("ip", str(ip)))

        if not title_tag is None:
            title_tag_str= title_tag.string if len(title_tag.string) > 0 else '---'
            lstData.append(("titulo", title_tag_str))
            lstData.append(('info_txt', title_tag_str))
            msgResult =  'OK'

        else:
            msgResult =  'INFO: NO INFO [{0}: {1}]'.format("Pagina Base", url)

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


if __name__ == "__main__":

    pass