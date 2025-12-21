def valname(name:str):
    val1 = name.strip().split()
    val2 = ' '.join(val1).title()
    return val2


def valcpf(cpf:str):
    length = len(cpf)
    if length != 11:
        return False
    else:
        return True


def valpassword(pswd:str):
    val1 = pswd.strip()
    length = len(val1)
    if val1.count(' ') >= 1 or length < 8:
        return False
    else:
        return True


