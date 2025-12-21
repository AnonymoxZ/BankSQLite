# copyright (c) 2025 AnonymoxZ
# authentication and login system
import sqlite3 as db
from modules_system import tools, validators as val



def login_client(cpf, password):
    logged = False
    msg_error = f'{tools.br}No register in database. Make sure registered as client of Mattres.{tools.br}'
    with db.connect(tools.pathdb()) as con:
        cursor = con.cursor()
        try:
            user_name = cursor.execute('''
                SELECT name FROM users WHERE cpf=? AND password=?
                ''',(cpf, password)).fetchone()
            tools.clear()
            if val.valcpf(cpf) and val.valpassword(password):
                logged = True
                return (logged, user_name[0])
            else:
                print(msg_error)
                return logged
        except:
            print(msg_error)
