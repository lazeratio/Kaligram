"""
==== XKNR - EXTRACTOR - Telefonos IP Cisco ====

Módulo para la extracción de información de las páginas de gestión de lo terminales IP Cisco de la familia 78xx.
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

    # La informacion esta en varias paginas
    url = "http://" + str(ip) # Pagina principal
    url2 = url + "/CGI/Java/Serviceability?adapter=device.statistics.port.network" # Datos de estadisticas de red


    # ==== Datos de pagina principal (si falla esta pagina no se procesan el resto) ====
    try:
        req = urllib.request.urlopen(url,timeout=timeout)
        html = req.read()
        soup = BeautifulSoup(html,'html5lib')

        # La informacion esta en la tabla 3
        tblInfo = soup.find_all('table')
        tblInfo = tblInfo[2] if len(tblInfo) == 3 else None

        if not tblInfo is None and len(tblInfo) > 0:

            lstData.append(("modulo","cisco78xx"))
            lstData.append(("ip",str(ip)))

            # Funciones para la busqueda de textos en las llamadas a beutifulsoup
            f1 = lambda val,elt: val in elt.string.strip()
            f2 = lambda val,elt: val in elt.string.strip().lower()

            # Lista de pares (nombre a dar al campo en los resultados, funcion de busqueda de cadena de texto para beautifulsoup)
            lstMapeo = [("mac", lambda x: f1("MAC",x)),
                       ("numero",lambda x: f2("directorio",x)),
                       ("modelo",lambda x: f2("modelo",x)),
                       ("num_serie",lambda x: f2("de serie",x)),
                       ("firmware",lambda x: f2("versión",x))]

            for elt in lstMapeo:
                f = elt[1]
                v = tblInfo.find_all(string=f)
                v = v[0].parent.parent.next_sibling.next_sibling.string.strip() if len(v) > 0 else '---'
                if (elt[0]=="numero"):
                    lstData.append(('info_txt', v))
                lstData.append((elt[0], v))



            msgResult =  'OK'

        else:
            msgResult =  'INFO: FORMATO NO VALIDO [{0}: {1}]'.format("Pagina Base", url)

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


    # ==== Datos de pagina de Configuracion de red ====
    try:
        req2 = urllib.request.urlopen(url2, timeout=timeout)
        html2 = req2.read()
        soup3 = BeautifulSoup(html2,'html5lib')

        tblInfo2 = soup3.find_all('table')
        tblInfo2 = tblInfo2[2] if len(tblInfo2) == 3 else None

        if not tblInfo2 is None and len(tblInfo2) > 0:

            f = lambda elt: "lldp id dispositivo vecino" in elt.string.strip().lower() or "lldp id de dispositivo vecino" in elt.string.strip().lower() # CAdenas distintas segun modelo
            v = tblInfo2.find_all(string=f)[0].parent.parent.next_sibling.next_sibling.string if tblInfo2 is not None else ''
            v = v.strip() if v is not None else ''
            lstData.append(("switch", v))

            f = lambda elt: "lldp puerto vecino" in elt.string.strip().lower()
            v = tblInfo2.find_all(string=f)[0].parent.parent.next_sibling.next_sibling.string if tblInfo2 is not None else ''
            v = v.strip() if v is not None else ''
            lstData.append(("puerto", v))

            f = lambda elt: "lldp dirección ip vecino" in elt.string.strip().lower()
            v = tblInfo2.find_all(string=f)[0].parent.parent.next_sibling.next_sibling.string if tblInfo2 is not None else ''
            v = v.strip() if v is not None else ''
            lstData.append(("switch_ip", v))

        else:
            msgResult = 'INFO: FORMATO NO VALIDO [{0}: {1}]'.format("Pagina Red", url2)

    except urllib.error.URLError as exc:
        # print("[%s] %s" % (ip, str(exc.reason)))
        msgResult = 'ERROR_URL [{0}: {1}]'.format("Pagina Red", url2)
        lstErrores.append(exc)
    except Exception as exc:
        msgResult = 'ERROR [{0}: {1}]'.format("Pagina Red", url2)
        lstErrores.append(exc)

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