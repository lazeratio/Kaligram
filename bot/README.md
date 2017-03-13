# Kaligram Bot
Bot creado en python 3.5 que permite gestionar remotamente un equipo.

Requisitos:

API para el control del bot de telegram.
    https://github.com/eternnoir/pyTelegramBotAPI
    
    pip install pyTelegramBotAPI

Los siguientes comandos estan disponibles:

    /start Muestra el mensaje de bienvenida.
    /help  Muestra esta ayuda.
    /get    Recibes el fichero que has solicidado.
    /exec  Ejecuta un comando. Necesita contraseña.
                ej: /exec ls -P=123
    /ls      Muestra los ficheros disponibles.
    
Los datos de configuración del bot estan en el fichero config.ini

    [DEFAULT]
    TOKEN = Token que te dan al crear el bot de Telegram.
    USERS = {'user1':'123', 'user2':'456'} # Usuarios que tienen acceso.
    ADMINS = {'admin1':'123', 'admin2':'456'} # Administradores
    PASSWORD = Hash MD5 de la contraseña que pedira para algunos comandos.
    PWDGPG = Contraseña con la que se cifraran los ficheros que envíe el bot.
    
    
    El acceso de los usuarios y administradores se controla a traves del id
    que tiene telegram para cada usuario.
    
    Para determinados comandos se requerirá un segundo factor de autenticación
    mediante una contraseña, para ello se agregará el parametro -P=contraseña
