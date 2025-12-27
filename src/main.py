# copyright (c) 2025 AnonymoxZ
# This file is part of the AnonymoxZ project, licensed under the MIT.
# See the LICENSE file in the project root for more information.
from modules_system import painel_client, tools
import client_register as cr
import custom_services as cs
import auth_login as log_in


# interfaces on
register_on = True
client_on = False
program_on = True
# ***************#


while program_on:
    try:
        tools.clear()
        if register_on:
            painel_client.screen_register()
            com = tools.filter_input(input('> '))
            match com:
                case 'e':
                    painel_client.end_session()
                    break
                case 'r':
                    '''
                    register a new user
                    '''
                    name_register = input('Enter your name: ')
                    cpf_register = input('Enter your CPF: ')
                    password_register = input('Enter an password(8 characters): ')
                    cr.register(name_register, cpf_register, password_register)
                case 'l':
                    cpf_client = input('Enter with CPF: ')
                    password_client = input('Enter with password: ')
                    client_logged = log_in.login_client(cpf_client, password_client)
                    if type(client_logged) == tuple:
                        tools.clear()
                        print('Logging...')
                        tools.wait(1)
                        client_on = True
                        register_on = False
                    else:
                        tools.wait(1)
                        continue
                case _:
                    tools.clear()
                    # ^_^
        # CLIENT
        elif client_on:                 # CPF             # PASSWORD
            painel_client.screen_client(client_logged[0], client_logged[1])
            com = tools.filter_input(input('> '))
            match com:
                case 'e':
                    confirm_exit = tools.filter_input(input('Confirm to exit: [y] or [n]: '))
                    if confirm_exit == 'y':
                        tools.clear()
                        print('Exit...')
                        tools.wait(1)
                        client_on = False
                        register_on = True
                    else:
                        continue
                case 'd':
                    '''
                    Deposit
                    '''
                    value_drop = float(input('Enter a value to drop: '))
                    if value_drop <= 0:
                        print(f'{tools.br}Invalid value to deposit!{tools.br}')
                    else:
                        cpf_adress = cpf_client
                        print(f'>> You drop R$ {value_drop:.2f}')
                        cs.deposit(cpf_adress, value_drop)
                case 'q':
                    '''
                    view currency balance
                    '''
                    cs.balance_query(cpf_client)
                case 't':
                    '''
                    transfers
                    '''
                    cpf_addresses = input('Enter the CPF to tranfer: ')
                    value_to = float(input('Enter the value to tranfer: '))
                    cs.tranfers_money(cpf_client, cpf_addresses, value_to)
                case 'r':
                    '''
                    print history client amounts receiveds
                    '''
                    cs.print_history_receiveds(cpf_client)
                case 'a':
                    '''
                    print history client actions | transfers and deposits
                    '''
                    cs.print_history_actions(cpf_client)
                case 's':
                    print(f'{tools.br}Change password{tools.br}')
                    new_password = input('Enter your new password (8 characters): ')
                    confirme_password = input('Confirme your password: ')
                    cs.change_password(cpf_client, new_password, confirme_password)
                case _:
                    tools.clear()
        tools.wait(2)
    except Exception as e:
        print("Please, try again, verify datas.")
        print(f'{tools.br}{e}{tools.br}')
        tools.wait(2)
