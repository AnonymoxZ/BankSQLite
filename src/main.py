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
                case '0':
                    painel_client.end_session()
                    break
                case '1':
                    name_register = input('Enter your name: ')
                    cpf_register = input('Enter your CPF: ')
                    password_register = input('Enter an password(8 characters): ')
                    cr.register(name_register, cpf_register, password_register)
                case '2':
                    cpf_client = input('Enter with CPF: ')
                    password_client = input('Enter with password: ')
                    client_logged = log_in.login_client(cpf_client, password_client)
                    if type(client_logged) == tuple:
                        client_on = True
                        register_on = False
                    else:
                        tools.wait(1)
                        continue
                case '3':
                    print(tools.br)
                    cs.show_users()
                    print(tools.br)
                    tools.wait(1)
                case _:
                    tools.clear()
                    # ^_^
        # CLIENT
        elif client_on:                 # CPF             # PASSWORD
            painel_client.screen_client(client_logged[0], client_logged[1])
            com = tools.filter_input(input('> '))
            match com:
                case '0':
                    tools.clear()
                    print('Exit...')
                    tools.wait(1)
                    client_on = False
                    register_on = True
                case '1':
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
                case '2':
                    '''
                    view currency balance
                    '''
                    cs.balance_inquiry(cpf_client)
                case '3':
                    '''
                    transfers
                    '''
                    cpf_addresses = input('Enter the CPF to tranfer: ')
                    value_to = float(input('Enter the value to tranfer: '))
                    cs.tranfers_money(cpf_client, cpf_addresses, value_to)
                case '4':
                    '''
                    print history client amounts receiveds
                    '''
                    cs.print_history_receiveds(cpf_client)
                case '5':
                    '''
                    print history client actions | transfers and deposits
                    '''
                    cs.print_history_actions(cpf_client)
                case _:
                    tools.clear()
        tools.wait(2)
    except Exception as e:
        print("Please, try again, verify datas.")
        print(f'{tools.br}{e}{tools.br}')

