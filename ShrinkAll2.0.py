from asyncio.windows_events import NULL
from math import exp
from multiprocessing import connection
from sqlite3 import Cursor
from time import sleep
from turtle import position, setposition
from typing import Counter, Iterator
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



sg.theme('dark')
janelamenu = True

driver_name = ''
driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
if driver_names:
    driver_name = driver_names[0]
if driver_name:
    conn_str = 'DRIVER={}; ...'.format(driver_name)
else:
    sg.Popup("Driver SQL nao encontrado na maquina")

while janelamenu:

    verifica_pasta = os.path.exists('log')
    if verifica_pasta == False:
        os.mkdir('log')

    #LEITURA DO ARQUIVO#
    config_object = ConfigParser()
    config_object.read("config.ini")
    userinfo = config_object["USERINFO"]
    USER_SQL = (userinfo["login"])
    PWD_SQL = (userinfo["password"])
    Server_SQL = (userinfo["server"])

    #LAYOUT MENU#
    layout = [
    [sg.Text('======================================')],
    [sg.Text('ShrinkAll - SQL')],
    [sg.Text('======================================')],
    [sg.Text("Versao: 221123")],
    ]

    windowMenu = sg.Window('Shrink SQL', layout, finalize=True, disable_close=True,element_justification='c')
    #values = windowMenu.read()

    windowMenu.Refresh()

    config_object = ConfigParser()
    config_object.read("config.ini")
    userinfo = config_object["USERINFO"]
    USER_SQL = (userinfo["login"])
    PWD_SQL = (userinfo["password"])
    Server_SQL = (userinfo["server"])
    try:
        conn = pyodbc.connect(f'DRIVER={{{driver_name}}};'
                                'Server='+Server_SQL+';'
                                'Database=master;'
                                'UID='+USER_SQL+';'
                                'PWD='+PWD_SQL+';'
                                'autocommit=True')
        cursor = conn.cursor()

        cursor.commit()
        sql = ('''
SET NOCOUNT ON
SELECT
'USE [' 
+ d.name + N']' 
+ CHAR(13) 
+ CHAR(10)
+ 'ALTER DATABASE ['
+ d.name + N']'
+ 'SET RECOVERY SIMPLE'
+ CHAR(13) 
+ CHAR(10)  
+ 'DBCC SHRINKFILE (N\'\'\'
+ mf.name 
+ N\'\'\', 0, TRUNCATEONLY)' 
+ CHAR(13) 
+ CHAR(10) 
+ CHAR(13) 
+ CHAR(10)                                                                  
AS sqlCommand
INTO
#shrinkCommands

FROM 
        sys.master_files mf 
JOIN sys.databases d 
    ON mf.database_id = d.database_id and d.name like 'SQL%'
WHERE d.database_id > 4 and mf.type_desc = 'LOG'


DECLARE iterationCursor CURSOR

FOR
SELECT 
    sqlCommand 
FROM 
    #shrinkCommands

OPEN iterationCursor

DECLARE @sqlStatement varchar(max)

FETCH NEXT FROM iterationCursor INTO @sqlStatement

WHILE (@@FETCH_STATUS = 0)
BEGIN
EXEC(@sqlStatement)
FETCH NEXT FROM iterationCursor INTO @sqlStatement
END

CLOSE iterationCursor
DEALLOCATE iterationCursor
DROP TABLE #shrinkCommands
        ''')
        conn.autocommit = True
        cursor.execute(sql)
        while cursor.nextset():
            pass 
        conn.close()
        sys.stdout = open("log\log.txt", "a")
        print("--Disparo de limpeza nos log's realizado\nData: ",datetime.datetime.now(),'\n')
        sys.stdout.close()
        sleep(5)
        windowMenu.Close()
        break
    except Exception as e:
        sys.stdout = open("log\log.txt", "a")
        print("--**Erro**\nData: ",datetime.datetime.now(),'\n',e,'\n')
        sys.stdout.close()
        sg.Popup(e)
        windowMenu.Close()
        break


windowMenu.Close()
