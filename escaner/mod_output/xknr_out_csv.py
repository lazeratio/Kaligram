"""
==== XKNR - OUTPUT - CSV ====

Módulo para genearció de CSV con datos extraidos por un módulo de extracción.
"""

import datetime
import csv
import colorama

def procesar_datos(datos):
    "Grabacion en un fichero csv de los datos"
    fecha = datetime.datetime.now().date()
    hora = datetime.datetime.now().time()

    # Se obtienen los distintos modulos de los que hay informacion
    modulos = set([dict(s)["modulo"] for s in datos])

    # Para cada modulo se genera un fichero
    for modulo in modulos:

        # Se filtran y ordenan por IP los registros correspondientes al modulo actual
        lstInfoModulo = list(filter(lambda x: dict(x)["modulo"] == modulo, datos))
        #lstInfoModulo.sort(key=lambda t: t[])

        f = None

        try:
            fname = "{0}_{1:02d}{2:02d}{3:02d}_{4:02d}{5:02d}{6:02d}.csv".format(modulo,fecha.year, fecha.month, fecha.day,hora.hour, hora.minute, hora.second)
            f = open(fname , 'wt', newline='')

            # Se obtienen las cabeceras para el CSV, en el orden en el que se generan en el modulo
            cabeceras = [x[0] for x in lstInfoModulo[0]]
            writer = csv.DictWriter(f, delimiter=';', fieldnames=cabeceras)
            writer.writeheader()
            writer.writerows([dict(x) for x in lstInfoModulo])
            print("\nGenerado el fichero {0}{1}{2} con el resultado del escaneo".format(colorama.Fore.MAGENTA,fname,colorama.Fore.RESET))

            return True

        except IOError as err:
                print("I/O error: {0}".format(err))
                return False
        except Exception as err:
                print("Error: {0}".format(err))
                return False
        finally:
            if not f is None:
                f.close()


if __name__ == "__main__":

    pass