import sqlite3


def data_tratado(data):
    data = data.split()
    data = data[0]
    data = data.split("-")
    data = f"{data[2]}/{data[1]}/{data[0]}"

    return data


def contador_menor(impressora, contador_menor_hora):
    conexao = sqlite3.connect('contador.db')
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT contador,datahora FROM contador WHERE ID = (?) AND date(datahora) = date(?) order by datahora asc""",
                   (impressora, contador_menor_hora))

    dados = cursor.fetchall()
    contador_menor_hora = dados[0][0]
    return contador_menor_hora


def contador_maior(impressora, contador_maior_hora):
    conexao = sqlite3.connect('contador.db')
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT contador,datahora FROM contador WHERE ID = (?) AND date(datahora) = date(?) order by datahora desc""",
                   (impressora, contador_maior_hora,))

    dados = cursor.fetchall()
    contador_maior_hora = dados[0][0]
    return contador_maior_hora
