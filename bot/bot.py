#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Santiago Prego
"""
import subprocess
import logging
import telebot #API para controlar el bot de telegram https://github.com/eternnoir/pyTelegramBotAPI 
import configparser 
import ast

"""Introducimos el token del bot que habremos creado previamente.
Lo creamos con @BotFather http://botsfortelegram.com/project/the-bot-father/
Ahora esta en el mismo fichero pero tenemos planeado usar un fichero 
de configuración externo para este dato"""


config = configparser.ConfigParser()
config.sections()
config.read('config.ini')
TOKEN = config['DEFAULT']['TOKEN']


#Activamos el log en modo debug para ver lo que recibe el bot.
telebot.logger.setLevel(logging.DEBUG)

#El bot con el que gestionaremos las interacciones con el usuario.
kbot = telebot.TeleBot(TOKEN)


@kbot.message_handler(commands=['start'])
def bienvenida(message):
    """Mensaje de bienvenida al iniciar el bot"""
    cid = message.chat.id
    kbot.send_message(cid, "Bienvenido a Kaligram, tu chat id es " + str(cid))
    kbot.send_message(cid, """
Este bot es solo para usuarios autorizados.
Para ayuda escriba /help""")
    
    if isuser(cid) == True:
        kbot.send_message(cid, "Tu usuario esta autorizado.")
    else:
        kbot.send_message(cid, "Tu usuario no esta autorizado.")


@kbot.message_handler(commands=['help'])
def ayuda(message):
    """Muestra la ayuda del bot, con sus comandos"""
    cid = message.chat.id
    kbot.send_message(cid, """\
Los siguientes comandos estan disponibles:
    /start Muestra el mensaje de bienvenida.
    /help  Muestra esta ayuda.
    /get    Recibes el fichero que has solicidado.
    /exec  Ejecutas un comando y te muestra el resultado.
    /ls     Muestra los ficheros disponibles.
""")


@kbot.message_handler(commands=['exec'])
def run(message):
    """Ejecuta el comando enviado y devuelve el resultado linea a linea."""
    cid = message.chat.id
    if isadmin(cid) == True:
        kbot.send_message(cid, message.text[len("/exec"):])
        cmd = message.text[len("/exec"):]
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        out = p.stdout.readlines()
    
        for l in out:
            kbot.send_message(cid, l.decode("utf-8"))
        
    else:
        kbot.send_message(cid, "No estás autorizado a usar este comando. \U0000274c") #\U0000274c es el emoticono de error.
        
        
@kbot.message_handler(commands=['ls'])
def ls(message):
    """Muestra los ficheros del directorio desde donde se esta ejecutando."""
    cid = message.chat.id
    if isuser(cid) == True:
        cmd = "ls -l"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        out = p.stdout.readlines()
    
        for l in out:
            kbot.send_message(cid, l.decode("utf-8"))
        
    else:
        kbot.send_message(cid, "No estás autorizado a usar este comando. \U0000274c") #\U0000274c es el emoticono de error.
        

@kbot.message_handler(commands=['get'])
def send(message):
    """ Enviamos el fichero que nos pidan y si no existe devuelve un error."""
    cid = message.chat.id
    if isuser(cid) == True:
        try:
            file = open(message.text[len("/get "):].replace(" ", ""), 'rb')
            kbot.send_document(cid, file)
        except:
            kbot.send_message(cid, "Fichero no encontrado.")
        
    else:
        kbot.send_message(cid, "No estás autorizado a usar este bot. \U0000274c") #\U0000274c es el emoticono de error.
        

@kbot.message_handler(func=lambda message: True)
def echo(message):
    """Responde con el mismo mensaje que recibe."""
    cid = message.chat.id
    if isuser(cid) == True:
        kbot.send_message(cid, "Escriba /help para ayuda.")
    else:
        kbot.send_message(cid, "No estás autorizado a usar este bot. \U0000274c") #\U0000274c es el emoticono de error.
    
    
@kbot.message_handler(func=lambda message: True, content_types=['document', 'text'])
def get(message):
    """Gestionamos el resto de mensajes, en principio recepción de ficheros."""
    cid = message.chat.id
    if isuser(cid) == True:
        try:
            message_dir = ""
            for m in dir(message.document):
                message_dir = message_dir + " | " + m
            kbot.send_message(cid, "Recibido: " +
                                    message.document.file_id +
                                    ", " + message.document.file_name +
                                    ", " + str(round(message.document.file_size / 1024)) + "KB" +
                                    ", " + message.document.mime_type)
    
            file_info = kbot.get_file(message.document.file_id)
            file = kbot.download_file(file_info.file_path)
    
            with open(message.document.file_name, 'wb') as new_file:
                new_file.write(file)
        except:
            kbot.send_message(cid, "Ha ocurrido un error con la recepción del fichero. No se ha podido guardar.") 
        
    else:
        kbot.send_message(cid, "No estás autorizado a usar este bot. \U0000274c") #\U0000274c es el emoticono de error.
        
        
def isuser(chat_id):
    """Comprueba si el usuario esta autorizado"""
    USERS = ast.literal_eval(config.get('DEFAULT', 'USERS'))
    for u, cid in USERS.items():
        if int(cid) == int(chat_id):
            return True
        else:
            return False
        
        
def isadmin(chat_id):
    """Comprueba si el usuario es administrador."""
    ADMINS = ast.literal_eval(config.get('DEFAULT', 'ADMINS'))
    for u, cid in ADMINS.items():
        if int(cid) == int(chat_id):
            return True
        else:
            return False        
        


kbot.polling()
