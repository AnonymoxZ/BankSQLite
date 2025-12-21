# screens terminal
from modules_system import tools



def screen_register():
    header_title = 'WELCOME TO MATTRESS $'
    BR = (len(header_title)+len(header_title))*"="
    print(f'''{BR}\n\t{header_title}\n{BR}
    [ 1 ] Register Account
    [ 2 ] Login Account
    [ 0 ] Exit
''')


def screen_client(login_true, name):
    '''
    :login_true [arg] bool;
    :name [arg] string;
    :Return interface if logged;
    '''
    if login_true:
        name_client = f'WELCOME {str(name).capitalize()}!'
        BR = (len(name_client)+len(name_client))*"="
        print(f'''{BR}\n\t{name_client}\n{BR}
    ( 1 ) Deposit
    ( 2 ) Balance Inquiry
    ( 3 ) Transfer 
    ( 4 ) History Receiveds
    ( 5 ) History Actions
    ( 0 ) Exit account 
    ''')


def end_session():
    tools.clear()
    BR = 30*"="
    print(BR)
    print('Thanks for used the Mattres!')
    print(BR)
