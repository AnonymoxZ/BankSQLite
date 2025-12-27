# copyright (c) 2025 AnonymoxZ
import sqlite3 as db
from modules_system import tools, validators as val


# deposit
def deposit(key_client, value_send):
    with db.connect(tools.pathdb()) as con:
        try:
            cursor = con.cursor()
            balance_currenty = cursor.execute('SELECT balance FROM users WHERE cpf=?',(key_client,))
            balance_add = value_send + balance_currenty.fetchone()[0]
            cursor.execute(f'''
            UPDATE users SET balance=? WHERE cpf=?;
            ''',(balance_add, key_client))
            con.commit()
            # log actions
            log_actions('d', key_client, key_client, value_send)
        except Exception as e:
            print(f'''
        OOps! An error ocurred in deposit.
        {tools.br}{e}{tools.br}
        ''')


# balance query
def balance_query(cpf_key):
    with db.connect(tools.pathdb()) as con:
        cursor = con.cursor()
        inquiry = cursor.execute('SELECT balance FROM users WHERE cpf=?',(cpf_key,))
        balance = f'{inquiry.fetchone()[0]:.2f}'
    print(f'Currenty balance: R${balance}')


# tranfers between clients
def tranfers_money(cpf_from, key_addressee, value_send):
    with db.connect(tools.pathdb()) as con:
        try:
            cursor = con.cursor()
            client_sender_query = cursor.execute('SELECT name, balance FROM users WHERE cpf=?', (cpf_from,)).fetchone()
            client_adress_query = cursor.execute('SELECT name, balance FROM users WHERE cpf=?',(key_addressee,)).fetchone()
            if cpf_from == key_addressee:
                print(f'{tools.br}Dont\'s possible to transfer for self-you.{tools.br}')
            else:
                balance_currenty_sender = client_sender_query[1]
                if balance_currenty_sender >= value_send:

                    # subtract of sender balance
                    balance_update = balance_currenty_sender - value_send
                    cursor.execute(
                    '''
                    UPDATE users SET balance=? WHERE cpf=?;
                    ''',(balance_update, cpf_from))
                    
                    # add to balance address
                    data_adress = client_adress_query # (name, balance)
                    name_adress = data_adress[0]
                    balance_adress = data_adress[1]
                    balance_add = balance_adress + value_send
                    cursor.execute(
                    '''
                    UPDATE users SET balance=? WHERE cpf=?;
                    ''',(balance_add, key_addressee))
                    print(f'Transfer ok! You transfer R${value_send:.2f} to {name_adress}.')
                    con.commit()

                    log_actions('t', cpf_from, key_addressee, value_send)
                    log_receiveds(cpf_from, key_addressee, value_send)
                else:
                    print('You no have balance sufficient.')
        except Exception as e:
            print(f'''
OOps! Transfer cancel. Try again.
            {tools.br}{e}{tools.br}
            ''')


# send log for address client history 
def log_receiveds(key_client, key_address, value_received):
    with db.connect(tools.pathdb()) as con:
        cursor = con.cursor()
        name_users_querie_client = cursor.execute('SELECT name FROM users WHERE cpf=?',(key_client,)).fetchone() # save as TRANSFER FROM
        name_users_querie_address = cursor.execute('SELECT name FROM users WHERE cpf=?',(key_address,)).fetchone() # save as TRANSFER TO
        logger = f'[{tools.timecurrency()}] Received R${value_received:.2f} from: {name_users_querie_client[0]}'
        cursor.execute(
        '''
        INSERT INTO cash_history (userNameAdress, receivedLog) VALUES (?,?);
        ''',(name_users_querie_address[0], logger))
        con.commit()


# log actions | transfers and deposits
def log_actions(key_action, key_client, to_client, value_received):
    match key_action:
        case 'd':
            type_action = 'deposit'
        case 't':
            type_action = 'transfer'

    datetime_log = tools.timecurrency()
    with db.connect(tools.pathdb()) as con:
        cursor = con.cursor()
        name_client_sender = cursor.execute('SELECT name FROM users WHERE cpf=?',(key_client,)).fetchone()[0]
        name_client_address = cursor.execute('SELECT name FROM users WHERE cpf=?',(to_client,)).fetchone()[0]
        # logger_actions = f'[{tools.timecurrency()}] Transfer of R${value_received} to {name_client_address}'
        cursor.execute(
        '''
        INSERT INTO actions_client (nameUser, typeAction, keyClient, toClient, value, dateAction) VALUES (?,?,?,?,?,?);
        ''',(name_client_sender, type_action, key_client, name_client_address, value_received, datetime_log))
        con.commit()


def print_history_receiveds(key_client_address):
    with db.connect(tools.pathdb()) as con:
        cursor = con.cursor()
        name_address = cursor.execute('SELECT name FROM users WHERE cpf=?',(key_client_address,)).fetchone()[0]
        datas_history = cursor.execute("SELECT receivedLog FROM cash_history WHERE userNameAdress=?",(name_address,)).fetchall()
        print(f'HISTORY RECEIVEDS:{tools.br}')
        for u in datas_history:
            for i in u:
                print(f'{i}')
        print(tools.br)


def print_history_actions(key_client):
    topics = ['Name:','Type transaction:', 
              'Key:', 'To:', 'Value: R$', 'Log:']
    try:
        with db.connect(tools.pathdb()) as con:
            cursor = con.cursor()
            datas_actions = cursor.execute(
            '''
            SELECT * FROM actions_client WHERE keyClient=?;
            ''',(key_client,)).fetchall()

        print(f'HISTORY ACTIONS:\n{70*"-"}') # aesthetic
        for table in datas_actions:
            for index,topic in enumerate(table):
                if index == 0:
                    print('\n')
                print(f'{topics[index]} {topic}')
        print(tools.br)
    except db.OperationalError:
        print('No logs of actions recents')
        tools.wait(1)


def change_password(key_client:str, new_pass:str, con_pass:str):
    '''
    :ARGS = [cpf client, new password, confirm password]
    '''
    if new_pass == con_pass and val.valpassword(new_pass):
        try:
            with db.connect(tools.pathdb()) as con:
                cursor = con.cursor()
                cursor.execute( # sql code
            '''
                UPDATE users SET password=? WHERE cpf=?
            ''',(new_pass, key_client)) 
        except db.OperationalError as e:
            print(f'{tools.br}It wasn\'t possible to change password. Try again.{tools.br}{e}')
    else:
        print(f'{tools.br}Check if password have security patterns: (8 characters){tools.br}')
