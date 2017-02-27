#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 05:14:28 2017

@author: Santiago Prego
"""
import logging
import telebot #API para controlar el bot de telegram https://github.com/eternnoir/pyTelegramBotAPI 

"""Introducimos el token del bot que habremos creado previamente.
Lo creamos con @BotFather http://botsfortelegram.com/project/the-bot-father/
Ahora esta en el mismo fichero pero tenemos planeado usar un fichero 
de configuración externo para este dato"""
TOKEN = "328665347:AAFEeZk8yp0u7hOpuE8fDJB3B1BPZq4smc4"

#Activamos el log en modo debug para ver lo que recibe el bot.
telebot.logger.setLevel(logging.DEBUG)

#El bot con el que gestionaremos las interacciones con el usuario.
kbot = telebot.TeleBot(TOKEN)


@kbot.message_handler(commands=['get'])
def enviar(message):
    """ Enviamos el fichero que nos pidan y si no existe devuelve un error."""
    try:
        file = open(message.text[len("/get "):].replace(" ", ""), 'rb')
        kbot.send_document(message.chat.id, file)
    except:
        kbot.send_message(message.chat.id, "Fichero no encontrado.")

@kbot.message_handler(func=lambda message: True)
def echo(message):
    """Responde con el mismo mensaje que recibe. """    
    kbot.reply_to(message, message.text)
    kbot.send_message(message.chat.id, "Tu id de chat es: " + str(message.chat.id))


kbot.polling()
