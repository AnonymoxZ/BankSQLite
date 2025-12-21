# copyright (c) 2025 AnonymoxZ
# this file register clients in db
import sqlite3 as db
from modules_system import validators as val, tools
from random import randint


def register(name, cpf, password):
    if (not val.valcpf(cpf)) or (not val.valpassword(password)):
        tools.clear()
        msg_error = 'Invalid data! Check your CPF or make sure your password has 8 characters.'
        br = f"\n{'-'*len(msg_error)}\n"
        print(f'{br}{msg_error}{br}')
        tools.wait(0)
        return
    with db.connect(tools.pathdb()) as connect:
        cursor = connect.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            cpf TEXT UNIQUE,
            password TEXT,
            balance REAL
        );
        ''')
        connect.commit()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS actions_client (
            nameUser TEXT,
            typeAction TEXT,
            keyClient TEXT,
            toClient TEXT,
            value REAL,
            dateAction TEXT
        );
        ''')
        connect.commit()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cash_history(
            userNameAdress TEXT,
            receivedLog TEXT
        );
        ''')
        connect.commit()
        try:
            balance_currenty = balance = 0
            cursor.execute('INSERT INTO users(name, cpf, password, balance) VALUES (?,?,?,?)',
            (val.valname(name), cpf, password, balance))
            print(f"{tools.br}Register with sucess!{tools.br}")
            tools.wait(0)
            connect.commit()
        except db.IntegrityError:
            tools.clear()
            print(f'{tools.br}CPF has been register.\nTry other CPF or create an new account.{tools.br}')
            tools.wait()

