#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 05:14:28 2017

@author: Santiago Prego
"""
import subprocess
import logging
import telebot #API para controlar el bot de telegram https://github.com/eternnoir/pyTelegramBotAPI 
import configparser 

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

@kbot.message_handler(commands=['exec'])
def run(message):
    kbot.send_message(message.chat.id, message.text[len("/exec"):])
    cmd = message.text[len("/exec"):]
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = p.stdout.readlines()

    for l in out:
        kbot.send_message(message.chat.id, l.decode("utf-8"))
        


@kbot.message_handler(commands=['get'])
def send(message):
    """ Enviamos el fichero que nos pidan y si no existe devuelve un error."""
    try:
        file = open(message.text[len("/get "):].replace(" ", ""), 'rb')
        kbot.send_document(message.chat.id, file)
    except:
        kbot.send_message(message.chat.id, "Fichero no encontrado.")

@kbot.message_handler(func=lambda message: True)
def echo(message):
    """Responde con el mismo mensaje que recibe."""    
    kbot.reply_to(message, message.text)
    kbot.send_message(message.chat.id, "Tu id de chat es: " + str(message.chat.id))
    
    
@kbot.message_handler(func=lambda message: True, content_types=['document', 'text'])
def get(message):
    """Gestionamos el resto de mensajes, en principio recepción de ficheros."""
    try:
        message_dir = ""
        for m in dir(message.document):
            message_dir = message_dir + " | " + m
        kbot.send_message(message.chat.id, "Recibido: " +
                                         message.document.file_id +
                                         ", " + message.document.file_name +
                                         ", " + str(round(message.document.file_size / 1024)) + "KB" +
                                         ", " + message.document.mime_type)

        file_info = kbot.get_file(message.document.file_id)
        file = kbot.download_file(file_info.file_path)

        with open(message.document.file_name, 'wb') as new_file:
            new_file.write(file)
    except:
        kbot.send_message(message.chat_id, "Ha ocurrido un error con la recepción del fichero. No se ha podido guardar.")       


kbot.polling()
