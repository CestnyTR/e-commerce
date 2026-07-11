# extensions.py
import pymysql
pymysql.install_as_MySQLdb()  # flask_mysqldb, derleme gerektiren mysqlclient yerine PyMySQL kullansın

from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()  # MySQL nesnesini burada oluştur
