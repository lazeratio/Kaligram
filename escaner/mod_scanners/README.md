== Directorio con módulos de procesamiento de rangos de IPs ==

Los módulos deben implementar un método con la siguiente firma:

    escanear_rango(lista_ips, modulo_escaneo, timeout, num_hilos, verbose)

    donde,

    - lista_ips: lista de IPs a escanear
    - modulo_escaneo: módulo de extracción de información que se aplicará a cada IP
    - timeout: tiempo de espera de respuesta de las peticiones
    - num_hilos: número de hilos de ejecución de las peticiones
    - verbose: habilitar el modo verbose durante la ejecución

    el método devolverá la información como dos listas, una de resultados y otra de errores, con un item en cada lista
    por cada IP.
