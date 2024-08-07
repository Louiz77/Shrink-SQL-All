from asyncio.windows_events import NULL
from math import exp
from multiprocessing import connection
from sqlite3 import Cursor
from time import sleep
from turtle import position, setposition
import PySimpleGUI as sg
import ctypes
import sys
import os
ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 )
import pyodbc
from configparser import ConfigParser
import re
from datetime import timedelta, date
import datetime
from time import daylight


sg.theme('DarkPurple7')

janelamenu = True

verifica_pasta = os.path.exists('log')
if verifica_pasta == False:
    os.mkdir('log')

while janelamenu:

    config_object = ConfigParser()
    config_object.read("config.ini")
    userinfo = config_object["USERINFO"]
    USER_SQL = (userinfo["login"])
    PWD_SQL = (userinfo["password"])
    Server_SQL = (userinfo["server"])

    layout = [
    [sg.Text('========================================================================\n                                                       Configurar - ShrinkAll\n========================================================================')],
    [sg.Text('Usuario SQL: '), sg.InputText(''+USER_SQL)],
    [sg.Text('Senha SQL: '), sg.InputText(''+PWD_SQL)],
    [sg.Text('Server SQL: '), sg.InputText(''+Server_SQL)],
    [sg.Button('Salvar',size=(20,5),pad=(50,5)), sg.Button('Cancelar',size=(20,5),pad=(70,5))],
    ]

    windowconf = sg.Window('ShrinkAll - Apontamento', layout, finalize=True, disable_close=True, element_justification='c')
    event, values = windowconf.read()

    USER_SQL = (values[0])
    PWD_SQL = (values[1])
    Server_SQL = (values[2])


    if event == 'Salvar':
        event, values = windowconf.read()

        config_object = ConfigParser()
        config_object.read("config.ini")

        userinfo = config_object["USERINFO"]

        userinfo["server"] = Server_SQL
        userinfo["login"] = USER_SQL
        userinfo["password"] = PWD_SQL



    with open('config.ini', 'w') as conf:
        config_object.write(conf)
    if event == 'Cancelar': 
        janelamenu = False
        break
    windowconf.Close()
