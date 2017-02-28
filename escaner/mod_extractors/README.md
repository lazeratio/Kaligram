== Directorio con módulos de extracción de información de direcciones IP ==

Los módulos deben implementar un método con la siguiente firma:

    parse(ip, timeout)

    donde,

    - ip: IP a la que se aplicará el módulo de extracción de información
    - timeout: tiempo de espera de respuesta de las peticiones

    el método devolverá la información en las siguientes variables:

    - un diccionario con la información extraida
    - un mensaje con el resultado del proceso de extracción, empezará por OK o ERRROR en función de si el proceso fue o no exitoso.
    - una lista de errores o warnings que se produzcan durante el proceso
